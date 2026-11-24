"""Level-up and Snapshots: the table moves a Character up a level, and can go back."""

import sqlite3

import pytest

import database
import snapshots
from characters import Sheet, SheetError, level_up, next_level_preview, seed_sheet


@pytest.fixture
def conn(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE", str(tmp_path / "test.db"))
    database.init_db()
    c = sqlite3.connect(database.DATABASE)
    c.row_factory = sqlite3.Row
    yield c
    c.close()


SHEET = Sheet(
    character={"name": "Testa", "class": "Wizard", "level": 3, "max_hp": 18, "spell_slots_2_max": 2},
    abilities=(
        {"name": "Arcane Recovery", "uses_max": 1, "recharge": "long"},
        {"name": "Sorcery Points", "uses_max": 3, "recharge": "long"},
        {"name": "Spell: Hold Person (2nd)", "type": "spell"},
    ),
    items=({"name": "Staff", "weight": 4.0},),
    levels={
        4: {
            "character": {"max_hp": 23, "spell_slots_2_max": 3},
            "abilities": [
                {"name": "Sorcery Points", "uses_max": 4},
                {"name": "Spell: Earthen Grasp (2nd)", "type": "spell"},
                {"name": "Feat: Lucky", "uses_max": 3, "recharge": "long"},
            ],
            "retire_abilities": ["Spell: Hold Person (2nd)"],
        },
        5: {"character": {"max_hp": 28, "spell_slots_3_max": 2}},
    },
)


def seeded(conn, sheet=SHEET):
    seed_sheet(conn, sheet)
    return conn.execute("SELECT id FROM characters WHERE name=?", (sheet.name,)).fetchone()[0]


def char(conn, cid):
    return conn.execute("SELECT * FROM characters WHERE id=?", (cid,)).fetchone()


def ability(conn, cid, name):
    return conn.execute("SELECT * FROM abilities WHERE character_id=? AND name=?", (cid, name)).fetchone()


def names(conn, cid, table="abilities"):
    return {r[0] for r in conn.execute(f"SELECT name FROM {table} WHERE character_id=?", (cid,))}


def mid_session(conn, cid):
    """Hurt, two slots spent, one Sorcery Point left, one hit die spent."""
    conn.execute(
        "UPDATE characters SET hp=9, spell_slots_2_remaining=0, hit_dice_remaining=2, notes='journal' WHERE id=?",
        (cid,),
    )
    conn.execute("UPDATE abilities SET uses_remaining=1 WHERE name='Sorcery Points'")
    conn.commit()


# ── Levelled Sheet ────────────────────────────────────────────────────────────


def test_sheet_at_a_level_applies_every_block_up_to_it():
    character, abilities, _items = SHEET.at(5)
    assert (character["level"], character["max_hp"], character["spell_slots_2_max"]) == (5, 28, 3)
    by_name = {a["name"]: a for a in abilities}
    assert by_name["Sorcery Points"]["uses_max"] == 4
    assert by_name["Sorcery Points"]["recharge"] == "long"  # changed entries keep their other fields
    assert "Spell: Hold Person (2nd)" not in by_name


def test_levels_must_run_on_from_the_base():
    with pytest.raises(ValueError, match="without gaps"):
        Sheet(character={"name": "X", "level": 3, "max_hp": 1}, levels={5: {}})


def test_a_field_a_level_changes_needs_a_base_value():
    with pytest.raises(ValueError, match="'ac'"):
        Sheet(character={"name": "X", "level": 1, "max_hp": 1}, levels={2: {"character": {"ac": 13}}})
    # spell slot maximums start at 0
    sheet = Sheet(character={"name": "X", "level": 1, "max_hp": 1}, levels={2: {"character": {"spell_slots_3_max": 2}}})
    assert sheet.at(1)[0]["spell_slots_3_max"] == 0


def test_retiring_an_unknown_row_is_rejected():
    with pytest.raises(ValueError, match="Nope"):
        Sheet(character={"name": "X", "level": 1, "max_hp": 1}, levels={2: {"retire_abilities": ["Nope"]}})


def test_seeding_keeps_the_level_the_table_reached(conn):
    cid = seeded(conn)
    level_up(conn, cid, SHEET)

    seeded(conn)

    c = char(conn, cid)
    assert (c["level"], c["max_hp"]) == (4, 23)
    assert "Spell: Hold Person (2nd)" not in names(conn, cid)  # not brought back by the base Sheet


# ── Level-up ──────────────────────────────────────────────────────────────────


def test_level_up_raises_each_counter_by_how_much_its_maximum_rose(conn):
    cid = seeded(conn)
    mid_session(conn, cid)

    level_up(conn, cid, SHEET)

    c = char(conn, cid)
    assert (c["level"], c["hp"], c["max_hp"]) == (4, 14, 23)
    assert (c["spell_slots_2_remaining"], c["spell_slots_2_max"]) == (1, 3)
    assert c["hit_dice_remaining"] == 3
    assert ability(conn, cid, "Sorcery Points")["uses_remaining"] == 2
    assert ability(conn, cid, "Feat: Lucky")["uses_remaining"] == 3  # new abilities arrive full
    assert ability(conn, cid, "Arcane Recovery")["uses_remaining"] == 1


def test_level_up_retires_rows_and_keeps_player_added_ones(conn):
    cid = seeded(conn)
    conn.execute("INSERT INTO abilities (character_id, name) VALUES (?, 'Lucky Coin')", (cid,))
    conn.commit()

    level_up(conn, cid, SHEET)

    assert names(conn, cid) == {
        "Arcane Recovery",
        "Sorcery Points",
        "Spell: Earthen Grasp (2nd)",
        "Feat: Lucky",
        "Lucky Coin",
    }


def test_level_up_takes_a_snapshot_first(conn):
    cid = seeded(conn)
    level_up(conn, cid, SHEET)

    [snap] = snapshots.list_for(conn, cid)
    assert (snap["label"], snap["level"], snap["automatic"]) == ("Before level 4", 3, 1)


def test_preview_matches_the_level_up_and_changes_nothing(conn):
    cid = seeded(conn)
    mid_session(conn, cid)

    preview = next_level_preview(conn, cid, SHEET)

    assert char(conn, cid)["level"] == 3
    assert snapshots.list_for(conn, cid) == []
    assert preview == level_up(conn, cid, SHEET)
    assert {"field": "hp", "before": 9, "after": 14} in preview["character"]
    assert preview["abilities"]["gained"] == ["Feat: Lucky", "Spell: Earthen Grasp (2nd)"]
    assert preview["abilities"]["retired"] == ["Spell: Hold Person (2nd)"]


def test_no_level_up_past_the_last_level_the_sheet_describes(conn):
    cid = seeded(conn)
    level_up(conn, cid, SHEET)
    level_up(conn, cid, SHEET)

    assert next_level_preview(conn, cid, SHEET) is None
    with pytest.raises(SheetError, match="level 6"):
        level_up(conn, cid, SHEET)


# ── Snapshots ─────────────────────────────────────────────────────────────────


def test_restore_puts_play_state_back_but_keeps_notes(conn):
    cid = seeded(conn)
    sid = snapshots.take(conn, cid, "Before the dragon")
    conn.commit()
    mid_session(conn, cid)

    snapshots.restore(conn, sid, SHEET)

    c = char(conn, cid)
    assert (c["hp"], c["spell_slots_2_remaining"], c["hit_dice_remaining"]) == (18, 2, 3)
    assert c["notes"] == "journal"
    assert ability(conn, cid, "Sorcery Points")["uses_remaining"] == 3


def test_restore_makes_rows_match_the_snapshot(conn):
    cid = seeded(conn)
    conn.execute("INSERT INTO inventory (character_id, name, quantity, flavor) VALUES (?, 'Rope', 1, 'frayed')", (cid,))
    conn.commit()
    sid = snapshots.take(conn, cid)
    conn.execute("DELETE FROM inventory WHERE name='Rope'")
    conn.execute("INSERT INTO inventory (character_id, name, quantity) VALUES (?, 'Potion', 2)", (cid,))
    conn.execute("UPDATE inventory SET flavor='carved by grandma' WHERE name='Staff'")
    conn.commit()

    snapshots.restore(conn, sid, SHEET)

    assert names(conn, cid, "inventory") == {"Staff", "Rope"}
    rope = conn.execute("SELECT * FROM inventory WHERE name='Rope'").fetchone()
    assert (rope["flavor"], rope["player_added"]) == ("frayed", 1)
    staff = conn.execute("SELECT * FROM inventory WHERE name='Staff'").fetchone()
    assert staff["flavor"] == "carved by grandma"  # surviving rows keep current flavor


def test_restoring_from_before_a_level_up_goes_back_a_level(conn):
    cid = seeded(conn)
    mid_session(conn, cid)
    level_up(conn, cid, SHEET)
    [before_level_4] = snapshots.list_for(conn, cid)

    snapshots.restore(conn, before_level_4["id"], SHEET)

    c = char(conn, cid)
    assert (c["level"], c["hp"], c["max_hp"], c["spell_slots_2_max"]) == (3, 9, 18, 2)
    assert names(conn, cid) == {"Arcane Recovery", "Sorcery Points", "Spell: Hold Person (2nd)"}
    assert ability(conn, cid, "Sorcery Points")["uses_max"] == 3

    level_up(conn, cid, SHEET)
    level_up(conn, cid, SHEET)  # level 5 adds 3rd-level slots
    snapshots.restore(conn, before_level_4["id"], SHEET)
    assert char(conn, cid)["spell_slots_3_max"] == 0

    level_up(conn, cid, SHEET)  # and can level up again
    assert char(conn, cid)["level"] == 4


def test_restore_takes_a_snapshot_first_so_it_can_be_undone(conn):
    cid = seeded(conn)
    sid = snapshots.take(conn, cid, "Start")
    conn.commit()
    mid_session(conn, cid)

    snapshots.restore(conn, sid, SHEET)
    undo = snapshots.list_for(conn, cid)[0]
    assert (undo["label"], undo["automatic"]) == ("Before restoring “Start”", 1)

    snapshots.restore(conn, undo["id"], SHEET)
    assert char(conn, cid)["hp"] == 9


RENAME_SQL = "UPDATE abilities SET name='Font of Magic' WHERE name='Sorcery Points'"


def test_restore_lets_the_sheet_win_on_what_code_owns(conn):
    cid = seeded(conn)
    sid = snapshots.take(conn, cid)
    conn.commit()

    # Later, code renames an ability (a Seed step) and changes a description
    renamed = Sheet(
        character=SHEET.character,
        abilities=(
            {"name": "Arcane Recovery", "uses_max": 1, "recharge": "long", "description": "new text"},
            {"name": "Font of Magic", "uses_max": 3, "recharge": "long"},
            {"name": "Spell: Hold Person (2nd)", "type": "spell"},
        ),
        items=SHEET.items,
        steps=(("rename", lambda c, i: c.execute(RENAME_SQL)),),
        levels={},
    )
    seeded(conn, renamed)

    snapshots.restore(conn, sid, renamed)

    assert names(conn, cid) == {"Arcane Recovery", "Font of Magic", "Spell: Hold Person (2nd)"}
    assert ability(conn, cid, "Arcane Recovery")["description"] == "new text"


def test_restore_refuses_a_level_the_sheet_no_longer_describes(conn):
    cid = seeded(conn)
    level_up(conn, cid, SHEET)
    sid = snapshots.take(conn, cid)
    conn.commit()
    rebased = Sheet(character={**SHEET.character, "level": 5, "max_hp": 28}, abilities=(), items=())

    with pytest.raises(snapshots.SnapshotError, match="level 4"):
        snapshots.restore(conn, sid, rebased)
    assert char(conn, cid)["level"] == 4
