"""Seeding: bring each Character in the database up to date with its Sheet.

Every module in this package declares one Character:

    CHARACTER  dict of `characters` columns
    ABILITIES  list of dicts of `abilities` columns
    ITEMS      list of dicts of `inventory` columns
    STEPS      list of (step_id, fn(conn, character_id)) Seed steps

Rules (see GLOSSARY.md for Sheet / Play state / Seed step):

- A Character missing from the database is created from its Sheet, with its
  initial Play state, and all of its Seed steps are recorded as applied.
- An existing Character first runs its unapplied Seed steps in order, then has
  every Sheet field overwritten from code. Play state is never touched after
  the row is created.
- Abilities and items absent from the Sheet are left alone (they may have been
  added in the UI). Removing or renaming one is a Seed step.
- Rows are matched by name: Characters by `name`, abilities/items by
  (character, `name`).
"""

import importlib
import pkgutil
import sqlite3

_SLOT_LEVELS = range(1, 10)

PLAY_FIELDS = {
    "characters": {
        "hp",
        "temp_hp",
        "hit_dice_remaining",
        "death_save_successes",
        "death_save_failures",
        "goodberries",
        "coins_pp",
        "coins_gp",
        "coins_sp",
        "coins_cp",
        "notes",
        *(f"spell_slots_{lvl}_remaining" for lvl in _SLOT_LEVELS),
    },
    "abilities": {"uses_remaining", "active"},
    "inventory": {"quantity", "equipped"},
}

# Sheet fields seeding owns on abilities/items, with the value an entry gets
# when it doesn't mention the field. Columns in neither this nor PLAY_FIELDS
# (e.g. `flavor`) belong to the UI and are never written by seeding.
_SHEET_DEFAULTS = {
    "abilities": {
        "type": "passive",
        "description": "",
        "uses_max": None,
        "recharge": None,
        "die_type": None,
        "ac_bonus": 0,
        "save_bonus": 0,
        "components": "",
        "spell_range": "",
        "duration": "",
        "concentration": 0,
        "spell_level": None,
        "upcastable": 0,
        "sets_base_ac": 0,
        "activatable": 0,
    },
    "inventory": {
        "weight": 0.0,
        "description": "",
        "ac_bonus": 0,
        "save_bonus": 0,
        "sets_base_ac": 0,
        "tool_proficient": 0,
        "damage_dice": "",
        "damage_type": "",
        "damage_notes": "",
        "magic_bonus": 0,
        "is_weapon": 0,
        "is_melee": 1,
        "finesse": 0,
    },
}


def seed_all(conn: sqlite3.Connection) -> None:
    """Seed every Character module in this package."""
    for _finder, modname, _ispkg in pkgutil.iter_modules(__path__):
        mod = importlib.import_module(f"{__name__}.{modname}")
        seed(
            conn,
            character=mod.CHARACTER,
            abilities=getattr(mod, "ABILITIES", ()),
            items=getattr(mod, "ITEMS", ()),
            steps=getattr(mod, "STEPS", ()),
        )


def seed(conn: sqlite3.Connection, *, character, abilities=(), items=(), steps=()) -> None:
    """Seed one Character in a single transaction. Safe to call on every boot."""
    _check_entries("abilities", abilities)
    _check_entries("inventory", items)
    step_ids = [sid for sid, _fn in steps]
    if len(set(step_ids)) != len(step_ids):
        raise ValueError(f"{character['name']}: duplicate Seed step ids")

    name = character["name"]
    conn.commit()
    conn.execute("BEGIN IMMEDIATE")  # serialise concurrent boots (gunicorn workers)
    try:
        row = conn.execute("SELECT id FROM characters WHERE name=?", (name,)).fetchone()
        if row is None:
            cid = _insert(conn, "characters", _initial_character(character))
            conn.executemany(
                "INSERT INTO seed_steps (character, step) VALUES (?, ?)",
                [(name, sid) for sid in step_ids],
            )
        else:
            cid = row[0]
            applied = {r[0] for r in conn.execute("SELECT step FROM seed_steps WHERE character=?", (name,))}
            for sid, fn in steps:
                if sid not in applied:
                    fn(conn, cid)
                    conn.execute("INSERT INTO seed_steps (character, step) VALUES (?, ?)", (name, sid))
            _update(conn, "characters", _sheet_part("characters", character), "id=?", (cid,))

        for table, entries in (("abilities", abilities), ("inventory", items)):
            for entry in entries:
                sheet = {**_SHEET_DEFAULTS[table], **_sheet_part(table, entry)}
                match = conn.execute(
                    f"SELECT id FROM {table} WHERE character_id=? AND name=?", (cid, entry["name"])
                ).fetchone()
                if match is None:
                    _insert(conn, table, {"character_id": cid, **sheet, **_initial_play(table, entry, sheet)})
                else:
                    _update(conn, table, sheet, "id=?", (match[0],))
        conn.commit()
    except BaseException:
        conn.rollback()
        raise


# ── internals ─────────────────────────────────────────────────────────────────


def _sheet_part(table, entry):
    return {k: v for k, v in entry.items() if k not in PLAY_FIELDS[table]}


def _initial_character(character):
    row = dict(character)
    row.setdefault("hp", character["max_hp"])
    row.setdefault("hit_dice_remaining", character.get("level", 1))
    for lvl in _SLOT_LEVELS:
        row.setdefault(f"spell_slots_{lvl}_remaining", character.get(f"spell_slots_{lvl}_max", 0))
    return row


def _initial_play(table, entry, sheet):
    if table == "abilities":
        return {"uses_remaining": entry.get("uses_remaining", sheet["uses_max"]), "active": entry.get("active", 0)}
    return {"quantity": entry.get("quantity", 1), "equipped": entry.get("equipped", 0)}


def _check_entries(table, entries):
    allowed = {"name"} | PLAY_FIELDS[table] | _SHEET_DEFAULTS[table].keys()
    names = set()
    for entry in entries:
        unknown = entry.keys() - allowed
        if unknown:
            raise ValueError(f"{table} entry {entry.get('name')!r}: unknown fields {sorted(unknown)}")
        if entry["name"] in names:
            raise ValueError(f"{table}: duplicate entry {entry['name']!r}")
        names.add(entry["name"])


def _insert(conn, table, row):
    cols = ", ".join(row)
    marks = ", ".join("?" * len(row))
    return conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks})", tuple(row.values())).lastrowid


def _update(conn, table, fields, where, params):
    if fields:
        sets = ", ".join(f"{k}=?" for k in fields)
        conn.execute(f"UPDATE {table} SET {sets} WHERE {where}", (*fields.values(), *params))
