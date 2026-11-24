"""Seeding: Sheet fields come from code, Play state belongs to the table."""

import sqlite3

import pytest

import database
from characters import seed, seed_all


@pytest.fixture
def conn(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE", str(tmp_path / "test.db"))
    database.init_db()
    c = sqlite3.connect(database.DATABASE)
    c.row_factory = sqlite3.Row
    yield c
    c.close()


def sheet(**overrides):
    character = {
        "name": "Testa",
        "race": "Human",
        "class": "Wizard",
        "level": 3,
        "max_hp": 18,
        "int": 16,
        "spell_slots_1_max": 4,
        "coins_gp": 15,
    }
    return {
        "character": {**character, **overrides.pop("character", {})},
        "abilities": [{"name": "Arcane Recovery", "type": "free_action", "uses_max": 1, "recharge": "long"}],
        "items": [{"name": "Staff", "weight": 4.0, "equipped": 1}],
        **overrides,
    }


def char(conn):
    return conn.execute("SELECT * FROM characters WHERE name='Testa'").fetchone()


def ability(conn, name="Arcane Recovery"):
    return conn.execute("SELECT * FROM abilities WHERE name=?", (name,)).fetchone()


def item(conn, name="Staff"):
    return conn.execute("SELECT * FROM inventory WHERE name=?", (name,)).fetchone()


def test_creates_character_with_initial_play_state(conn):
    seed(conn, **sheet())

    c = char(conn)
    assert (c["level"], c["max_hp"], c["hp"]) == (3, 18, 18)
    assert c["hit_dice_remaining"] == 3
    assert c["spell_slots_1_remaining"] == 4
    assert c["coins_gp"] == 15
    assert ability(conn)["uses_remaining"] == 1
    assert item(conn)["equipped"] == 1


def test_play_state_survives_reseed(conn):
    seed(conn, **sheet())
    cid = char(conn)["id"]
    conn.execute(
        "UPDATE characters SET hp=5, coins_gp=999, hit_dice_remaining=1, spell_slots_1_remaining=0, notes='x' "
        "WHERE id=?",
        (cid,),
    )
    conn.execute("UPDATE abilities SET uses_remaining=0, active=1")
    conn.execute("UPDATE inventory SET equipped=0, quantity=3")
    conn.commit()

    seed(conn, **sheet())

    c = char(conn)
    assert (c["hp"], c["coins_gp"], c["hit_dice_remaining"], c["spell_slots_1_remaining"], c["notes"]) == (
        5,
        999,
        1,
        0,
        "x",
    )
    assert (ability(conn)["uses_remaining"], ability(conn)["active"]) == (0, 1)
    assert (item(conn)["equipped"], item(conn)["quantity"]) == (0, 3)


def test_sheet_changes_in_code_win_on_reseed(conn):
    seed(conn, **sheet())
    conn.execute("UPDATE abilities SET description='edited in UI'")
    conn.commit()

    s = sheet(character={"max_hp": 25, "int": 17})
    s["abilities"][0]["uses_max"] = 2
    seed(conn, **s)

    c = char(conn)
    assert (c["max_hp"], c["int"]) == (25, 17)
    assert ability(conn)["uses_max"] == 2
    assert ability(conn)["description"] == ""  # Sheet default wins over the UI edit


def test_rows_and_fields_outside_the_sheet_are_left_alone(conn):
    seed(conn, **sheet())
    cid = char(conn)["id"]
    conn.execute("INSERT INTO abilities (character_id, name) VALUES (?, 'Homebrew Trick')", (cid,))
    conn.execute("UPDATE inventory SET flavor='carved by grandma'")
    conn.commit()

    seed(conn, **sheet())

    assert ability(conn, "Homebrew Trick") is not None
    assert item(conn)["flavor"] == "carved by grandma"


def test_new_character_records_steps_without_running_them(conn):
    calls = []
    seed(conn, **sheet(steps=[("level-3", lambda c, cid: calls.append(cid))]))

    assert calls == []
    assert conn.execute("SELECT step FROM seed_steps").fetchall()[0]["step"] == "level-3"


def test_step_runs_once_before_sheet_refresh(conn):
    seed(conn, **sheet(character={"level": 2, "max_hp": 12}))

    def level_3(c, cid):
        c.execute("UPDATE characters SET hp=hp+6 WHERE id=? AND level<3", (cid,))

    s = sheet(steps=[("level-3", level_3)])
    seed(conn, **s)
    seed(conn, **s)

    c = char(conn)
    assert (c["level"], c["max_hp"], c["hp"]) == (3, 18, 18)


def test_failing_step_rolls_back_the_whole_seed(conn):
    seed(conn, **sheet())

    def boom(c, cid):
        c.execute("UPDATE characters SET hp=1 WHERE id=?", (cid,))
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        seed(conn, **sheet(character={"max_hp": 99}, steps=[("boom", boom)]))

    c = char(conn)
    assert (c["hp"], c["max_hp"]) == (18, 18)
    assert conn.execute("SELECT COUNT(*) FROM seed_steps").fetchone()[0] == 0


def test_unknown_sheet_field_is_rejected(conn):
    s = sheet()
    s["abilities"][0]["usesmax"] = 3
    with pytest.raises(ValueError, match="usesmax"):
        seed(conn, **s)


def test_real_characters_seed_idempotently(conn):
    seed_all(conn)
    before = [
        [tuple(r) for r in conn.execute(f"SELECT * FROM {t} ORDER BY 1, 2")]
        for t in ("characters", "abilities", "inventory", "seed_steps")
    ]
    seed_all(conn)
    after = [
        [tuple(r) for r in conn.execute(f"SELECT * FROM {t} ORDER BY 1, 2")]
        for t in ("characters", "abilities", "inventory", "seed_steps")
    ]
    assert before == after
    assert {r["name"] for r in conn.execute("SELECT name FROM characters")} == {"Inkwell", "••TOMATO•"}
