"""Seeding and Level-up: keep each Character in the database in line with its Sheet.

Every module in this package declares one Character:

    CHARACTER  dict of `characters` columns: the Sheet at its base level
    ABILITIES  list of dicts of `abilities` columns
    ITEMS      list of dicts of `inventory` columns
    LEVELS     {level: block} describing each level above the base (optional)
    STEPS      list of (step_id, fn(conn, character_id)) Seed steps

A LEVELS block lists what changes on reaching that level, every key optional:

    5: {
        "character": {"max_hp": 29, "spell_slots_3_max": 2},  # new Sheet values
        "abilities": [                                        # gained, or changed by name
            {"name": "Sorcery Points", "uses_max": 5},
            {"name": "Spell: Fireball (3rd)", "type": "spell", ...},
        ],
        "items": [...],
        "retire_abilities": ["Spell: Hold Person (2nd)"],
        "retire_items": [],
    }

Levels must run on from the base without gaps. The Sheet at level N is the base
with every block up to N applied.

Rules (see GLOSSARY.md for Sheet / Play state / Level-up / Seed step):

- A Character missing from the database is created from its Sheet at the base
  level, with its initial Play state, and all of its Seed steps are recorded
  as applied.
- An existing Character first runs its unapplied Seed steps in order, then has
  every Sheet field overwritten from the Sheet at its current level. Play state
  (including level) is never touched by Seeding after the row is created.
- Abilities and items the Sheet describes are marked as the Sheet's; any others
  are Player-added and left alone. Removing or renaming one outside a Level-up
  is a Seed step.
- Rows are matched by name: Characters by `name`, abilities/items by
  (character, `name`).
- Level-up moves a Character to the next level: Sheet refresh at the new level,
  retired rows deleted, and each Play state counter raised by however much its
  maximum rose.
"""

import importlib
import pkgutil
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import cache

_SLOT_LEVELS = range(1, 10)

PLAY_FIELDS = {
    "characters": {
        "level",
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

# Play state counters a Level-up raises along with their maximum: (current, max).
_CHARACTER_COUNTERS = [
    ("hp", "max_hp"),
    ("hit_dice_remaining", "level"),
    *((f"spell_slots_{lvl}_remaining", f"spell_slots_{lvl}_max") for lvl in _SLOT_LEVELS),
]

_SLOT_MAXES = {f"spell_slots_{lvl}_max" for lvl in _SLOT_LEVELS}

_BLOCK_KEYS = {"character", "abilities", "items", "retire_abilities", "retire_items"}


class SheetError(Exception):
    """The Sheet can't do what was asked (no next level, unknown level, …)."""


@dataclass(frozen=True)
class Sheet:
    character: dict
    abilities: tuple = ()
    items: tuple = ()
    steps: tuple = ()
    levels: dict = field(default_factory=dict)

    def __post_init__(self):
        name = self.character["name"]
        step_ids = [sid for sid, _fn in self.steps]
        if len(set(step_ids)) != len(step_ids):
            raise ValueError(f"{name}: duplicate Seed step ids")
        expected = list(range(self.base_level + 1, self.base_level + 1 + len(self.levels)))
        if sorted(self.levels) != expected:
            raise ValueError(f"{name}: LEVELS must run on from base level {self.base_level} without gaps")
        for lvl, block in self.levels.items():
            unknown = block.keys() - _BLOCK_KEYS
            if unknown:
                raise ValueError(f"{name} level {lvl}: unknown keys {sorted(unknown)}")
            if "level" in block.get("character", {}):
                raise ValueError(f"{name} level {lvl}: don't set 'level' in a level block")
            # Going back a level (restoring a Snapshot) needs a value for every field
            # a level changes, so each one must have a value at the base level too.
            unset = block.get("character", {}).keys() - self.character.keys() - _SLOT_MAXES
            if unset:
                raise ValueError(f"{name} level {lvl}: set {sorted(unset)} in the base Sheet too")
        for lvl in self.describes():
            self.at(lvl)  # validates every level's entries up front

    @property
    def name(self):
        return self.character["name"]

    @property
    def base_level(self):
        return self.character.get("level", 1)

    @property
    def max_level(self):
        return self.base_level + len(self.levels)

    def describes(self):
        return range(self.base_level, self.max_level + 1)

    def at(self, level):
        """The Sheet at `level`: (character, abilities, items)."""
        if level not in self.describes():
            raise SheetError(
                f"{self.name}'s Sheet describes levels {self.base_level}–{self.max_level}, not level {level}"
            )
        changed = {k for block in self.levels.values() for k in block.get("character", {})}
        character = {**{k: 0 for k in changed & _SLOT_MAXES}, **self.character}
        rows = {
            "abilities": {e["name"]: dict(e) for e in self.abilities},
            "inventory": {e["name"]: dict(e) for e in self.items},
        }
        for lvl in range(self.base_level + 1, level + 1):
            block = self.levels[lvl]
            character.update(block.get("character", {}))
            for table, key, retire_key in (
                ("abilities", "abilities", "retire_abilities"),
                ("inventory", "items", "retire_items"),
            ):
                for entry in block.get(key, ()):
                    rows[table][entry["name"]] = {**rows[table].get(entry["name"], {}), **entry}
                for retired in block.get(retire_key, ()):
                    if rows[table].pop(retired, None) is None:
                        raise ValueError(f"{self.name} level {lvl}: can't retire unknown {retired!r}")
        character["level"] = level
        abilities, items = list(rows["abilities"].values()), list(rows["inventory"].values())
        _check_entries("abilities", abilities)
        _check_entries("inventory", items)
        return character, abilities, items

    def retired_at(self, level):
        block = self.levels.get(level, {})
        return {"abilities": block.get("retire_abilities", ()), "inventory": block.get("retire_items", ())}


# ── Registry ──────────────────────────────────────────────────────────────────


@cache
def sheets():
    """Every Character module's Sheet, by Character name."""
    found = {}
    for _finder, modname, _ispkg in pkgutil.iter_modules(__path__):
        mod = importlib.import_module(f"{__name__}.{modname}")
        sheet = Sheet(
            character=mod.CHARACTER,
            abilities=tuple(getattr(mod, "ABILITIES", ())),
            items=tuple(getattr(mod, "ITEMS", ())),
            steps=tuple(getattr(mod, "STEPS", ())),
            levels=dict(getattr(mod, "LEVELS", {})),
        )
        found[sheet.name] = sheet
    return found


def sheet_for(conn, character_id):
    """The Sheet for a Character in the database, or None if it has none."""
    row = conn.execute("SELECT name FROM characters WHERE id=?", (character_id,)).fetchone()
    return sheets().get(row[0]) if row else None


# ── Seeding ───────────────────────────────────────────────────────────────────


def seed_all(conn: sqlite3.Connection) -> None:
    """Seed every Character module in this package."""
    for sheet in sheets().values():
        seed_sheet(conn, sheet)


def seed(conn: sqlite3.Connection, *, character, abilities=(), items=(), steps=(), levels=None) -> None:
    """Seed one Character from its Sheet parts. Safe to call on every boot."""
    seed_sheet(conn, Sheet(character, tuple(abilities), tuple(items), tuple(steps), dict(levels or {})))


def seed_sheet(conn: sqlite3.Connection, sheet: Sheet) -> None:
    """Seed one Character in a single transaction. Safe to call on every boot."""
    with transaction(conn):  # BEGIN IMMEDIATE serialises concurrent boots (gunicorn workers)
        row = conn.execute("SELECT id FROM characters WHERE name=?", (sheet.name,)).fetchone()
        if row is None:
            character, _, _ = sheet.at(sheet.base_level)
            cid = _insert(conn, "characters", _initial_character(character))
            conn.executemany(
                "INSERT INTO seed_steps (character, step) VALUES (?, ?)",
                [(sheet.name, sid) for sid, _fn in sheet.steps],
            )
        else:
            cid = row[0]
            applied = {r[0] for r in conn.execute("SELECT step FROM seed_steps WHERE character=?", (sheet.name,))}
            for sid, fn in sheet.steps:
                if sid not in applied:
                    fn(conn, cid)
                    conn.execute("INSERT INTO seed_steps (character, step) VALUES (?, ?)", (sheet.name, sid))
        apply_sheet(conn, sheet, cid)


def apply_sheet(conn, sheet, cid):
    """Overwrite Sheet fields from the Sheet at the Character's current level and
    ensure every row it describes exists. Play state is only set on new rows."""
    level = conn.execute("SELECT level FROM characters WHERE id=?", (cid,)).fetchone()[0]
    character, abilities, items = sheet.at(level)
    _update(conn, "characters", _sheet_part("characters", character), "id=?", (cid,))
    for table, entries in (("abilities", abilities), ("inventory", items)):
        for entry in entries:
            row = {**_SHEET_DEFAULTS[table], **_sheet_part(table, entry), "player_added": 0}
            match = conn.execute(
                f"SELECT id FROM {table} WHERE character_id=? AND name=? ORDER BY id", (cid, entry["name"])
            ).fetchone()
            if match is None:
                _insert(conn, table, {"character_id": cid, **row, **_initial_play(table, entry, row)})
            else:
                _update(conn, table, row, "id=?", (match[0],))


# ── Level-up ──────────────────────────────────────────────────────────────────


def level_up(conn, cid, sheet, *, dry_run=False):
    """Move a Character to the next level its Sheet describes, first taking a
    Snapshot. Returns what changed. With dry_run, nothing is kept: the result
    is the preview."""
    import snapshots  # deferred: snapshots builds on this module

    if sheet is None:
        raise SheetError("This Character has no Sheet to level up from")
    with transaction(conn, commit=not dry_run):
        before = snapshots.capture(conn, cid)
        to = before["character"]["level"] + 1
        if to > sheet.max_level:
            raise SheetError(f"{sheet.name}'s Sheet doesn't describe level {to} yet")
        if not dry_run:
            snapshots.take(conn, cid, f"Before level {to}", automatic=True)

        conn.execute("UPDATE characters SET level=? WHERE id=?", (to, cid))
        for table, names in sheet.retired_at(to).items():
            for name in names:
                conn.execute(f"DELETE FROM {table} WHERE character_id=? AND name=?", (cid, name))
        apply_sheet(conn, sheet, cid)

        new = snapshots.capture(conn, cid)["character"]
        old = before["character"]
        raised = {cur: _raise(old[cur], old[mx], new[mx]) for cur, mx in _CHARACTER_COUNTERS}
        _update(conn, "characters", raised, "id=?", (cid,))
        old_uses = {a["name"]: a for a in before["abilities"]}
        for aid, name, uses_max in conn.execute(
            "SELECT id, name, uses_max FROM abilities WHERE character_id=?", (cid,)
        ).fetchall():
            if name in old_uses and uses_max is not None:
                o = old_uses[name]
                conn.execute(
                    "UPDATE abilities SET uses_remaining=? WHERE id=?",
                    (_raise(o["uses_remaining"], o["uses_max"], uses_max), aid),
                )
        return snapshots.diff(before, snapshots.capture(conn, cid))


def next_level_preview(conn, cid, sheet):
    """The Level-up the Character would get now, or None if its Sheet has no next level."""
    if sheet is None:
        return None
    level = conn.execute("SELECT level FROM characters WHERE id=?", (cid,)).fetchone()[0]
    if level + 1 > sheet.max_level:
        return None
    return level_up(conn, cid, sheet, dry_run=True)


def _raise(current, old_max, new_max):
    """A counter after its maximum moved from old_max to new_max."""
    raised = (current or 0) + (new_max or 0) - (old_max or 0)
    return max(0, min(raised, new_max or 0))


# ── internals ─────────────────────────────────────────────────────────────────


@contextmanager
def transaction(conn, *, commit=True):
    """One write transaction; rolled back on error, or always when commit=False."""
    conn.commit()
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield
    except BaseException:
        conn.rollback()
        raise
    if commit:
        conn.commit()
    else:
        conn.rollback()


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
