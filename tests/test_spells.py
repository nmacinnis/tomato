"""Spells: a Sheet names a spell; its Rules text and card details come from spells.py."""

import re
import sqlite3

import pytest

import database
from characters import seed, sheets
from spells import SPELLS


@pytest.fixture
def conn(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE", str(tmp_path / "test.db"))
    database.init_db()
    c = sqlite3.connect(database.DATABASE)
    c.row_factory = sqlite3.Row
    yield c
    c.close()


CHARACTER = {"name": "Testa", "race": "Human", "class": "Wizard", "level": 3, "max_hp": 18}


def ability(conn, name):
    return conn.execute("SELECT * FROM abilities WHERE name=?", (name,)).fetchone()


def test_every_sheet_spell_is_in_the_spell_list():
    # Sheets validate every level on load, so this fails for an unknown spell in
    # the base Sheet or in any LEVELS block.
    named = [
        entry["spell"]
        for sheet in sheets().values()
        for entry in [*sheet.abilities, *(a for b in sheet.levels.values() for a in b.get("abilities", ()))]
        if "spell" in entry
    ]
    assert named, "expected the real Sheets to name some spells"
    assert set(named) <= SPELLS.keys()


def test_seeding_fills_rules_text_and_card_details_from_the_spell_list(conn):
    seed(
        conn,
        character=CHARACTER,
        abilities=[{"name": "Spell: Shield (1st)", "spell": "Shield", "type": "reaction", "description": "Summary"}],
    )

    a = ability(conn, "Spell: Shield (1st)")
    assert a["description"] == "Summary"
    assert a["rules_text"] == SPELLS["Shield"]["rules_text"]
    assert a["rules_source"] == "PHB 2024, p. 316 · SRD 5.2"
    assert (a["spell_range"], a["components"], a["duration"]) == ("Self", "V, S", "1 round")
    assert (a["concentration"], a["spell_level"]) == (0, 1)


def test_seeding_overwrites_drifted_spell_details(conn):
    entry = {"name": "Cantrip: Mage Hand", "spell": "Mage Hand", "type": "action"}
    seed(conn, character=CHARACTER, abilities=[entry])
    conn.execute("UPDATE abilities SET concentration=1, rules_text='old'")
    conn.commit()

    seed(conn, character=CHARACTER, abilities=[entry])

    a = ability(conn, "Cantrip: Mage Hand")
    assert (a["concentration"], a["rules_text"]) == (0, SPELLS["Mage Hand"]["rules_text"])


def test_sheet_may_override_spell_level_only():
    with pytest.raises(ValueError, match="come from spells.py"):
        sheets_with(
            {"name": "Spell: Shield (1st)", "spell": "Shield", "spell_range": "Self (homebrew)"},
        )
    _, abilities, _ = sheets_with({"name": "Goodberry", "spell": "Goodberry", "spell_level": None}).at(3)
    assert abilities[0]["spell_level"] is None
    assert abilities[0]["rules_text"] == SPELLS["Goodberry"]["rules_text"]


def test_unknown_spell_is_rejected():
    with pytest.raises(ValueError, match="isn't in spells.py"):
        sheets_with({"name": "Spell: Wish (9th)", "spell": "Wish"})


def test_non_spell_abilities_have_no_rules_text(conn):
    seed(conn, character=CHARACTER, abilities=[{"name": "Arcane Recovery", "description": "Regain slots."}])
    assert ability(conn, "Arcane Recovery")["rules_text"] == ""


@pytest.mark.parametrize("name", sorted(SPELLS))
def test_every_spell_has_rules_text_or_a_link_but_not_both(name):
    spell = SPELLS[name]
    assert bool(spell.get("rules_text")) != bool(spell.get("rules_url"))
    # Only SRD 5.2 wording (CC-BY-4.0) may be stored; everything else is linked to.
    assert bool(spell.get("rules_text")) == spell["rules_source"].endswith("· SRD 5.2")
    if "rules_url" in spell:
        assert spell["rules_url"].startswith("https://5e.tools/spells.html#")


def test_seeding_stores_a_link_for_non_srd_spells(conn):
    seed(conn, character=CHARACTER, abilities=[{"name": "Cantrip: Friends", "spell": "Friends", "type": "action"}])

    a = ability(conn, "Cantrip: Friends")
    assert (a["rules_text"], a["rules_url"]) == ("", "https://5e.tools/spells.html#friends_xphb")


@pytest.mark.parametrize("name", sorted(n for n, s in SPELLS.items() if "rules_text" in s))
def test_rules_text_uses_only_the_supported_markdown(name):
    # The UI (renderRulesText in static/character-utils.js) renders blank-line
    # paragraphs, blocks made only of "- " items, and **bold**. Nothing else.
    text = SPELLS[name]["rules_text"]
    assert "{@" not in text, "5e.tools markup left in"
    assert text.startswith("**Casting Time:** ")
    for block in text.split("\n\n"):
        assert block.strip(), "empty paragraph"
        lines = block.split("\n")
        if len(lines) > 1:
            assert all(line.startswith("- ") for line in lines), f"multi-line block that isn't a list: {block!r}"
        assert block.count("**") % 2 == 0, f"unbalanced bold: {block!r}"
        assert not re.search(r"(?<!\*)\*(?!\*)|_\w", block), f"unsupported emphasis: {block!r}"


def sheets_with(*abilities):
    from characters import Sheet

    return Sheet(character=CHARACTER, abilities=tuple(abilities))
