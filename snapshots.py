"""Snapshots: dated copies of a Character's Play state and rows, which can be restored.

A Snapshot holds every Play state field except session notes (level included),
and every ability and item row in full, each marked Sheet or Player-added.

Restoring one (see GLOSSARY.md):

1. takes a Snapshot of the current state first, so a restore can be undone;
2. puts back the Snapshot's level and Play state;
3. makes the rows match the Snapshot, by name: rows added since are removed,
   rows deleted since are recreated, the rest get the Snapshot's values;
4. reseeds at the restored level, so the Sheet wins on everything code owns,
   and drops Sheet rows the Sheet no longer describes (Player-added rows stay).

Notes, the theme, and the flavor text of rows that survive are never touched.
"""

import json
from collections import defaultdict
from datetime import datetime, timezone

from characters import PLAY_FIELDS, SheetError, apply_sheet, transaction

_TABLES = (("abilities", "abilities"), ("items", "inventory"))  # (state key, table)
_KEPT_ON_RESTORE = {"notes"}  # Character fields a Snapshot never holds
_ROW_KEPT_ON_RESTORE = {"flavor"}  # row fields a restore keeps on surviving rows
_NOT_COMPARED = {"id", "character_id"}


class SnapshotError(Exception):
    pass


def capture(conn, cid):
    """The Character's current rows in full: {"character", "abilities", "items"}."""
    character = conn.execute("SELECT * FROM characters WHERE id=?", (cid,)).fetchone()
    if character is None:
        raise SnapshotError(f"No Character {cid}")
    return {
        "character": _as_dict(conn, "characters", character),
        **{
            key: [
                _as_dict(conn, table, r)
                for r in conn.execute(f"SELECT * FROM {table} WHERE character_id=? ORDER BY id", (cid,))
            ]
            for key, table in _TABLES
        },
    }


def take(conn, cid, label="", *, automatic=False):
    """Store a Snapshot of the Character now. Returns its id."""
    state = capture(conn, cid)
    stored = {
        "character": {k: v for k, v in state["character"].items() if k in PLAY_FIELDS["characters"] - _KEPT_ON_RESTORE},
        **{key: [_strip(r) for r in state[key]] for key, _table in _TABLES},
    }
    return conn.execute(
        "INSERT INTO snapshots (character_id, label, taken_at, level, automatic, state) VALUES (?,?,?,?,?,?)",
        (
            cid,
            label.strip(),
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            state["character"]["level"],
            1 if automatic else 0,
            json.dumps(stored),
        ),
    ).lastrowid


def list_for(conn, cid):
    rows = conn.execute(
        "SELECT id, label, taken_at, level, automatic FROM snapshots WHERE character_id=? ORDER BY id DESC",
        (cid,),
    )
    return [dict(zip(("id", "label", "taken_at", "level", "automatic"), r)) for r in rows]


def character_of(conn, snapshot_id):
    row = conn.execute("SELECT character_id FROM snapshots WHERE id=?", (snapshot_id,)).fetchone()
    return row[0] if row else None


def delete(conn, snapshot_id):
    conn.execute("DELETE FROM snapshots WHERE id=?", (snapshot_id,))
    conn.commit()


def restore(conn, snapshot_id, sheet):
    """Restore a Snapshot onto its Character. `sheet` is the Character's Sheet, or None."""
    with transaction(conn):
        row = conn.execute(
            "SELECT character_id, label, taken_at, level, state FROM snapshots WHERE id=?", (snapshot_id,)
        ).fetchone()
        if row is None:
            raise SnapshotError("No such Snapshot")
        cid, label, taken_at, level, state = row
        state = json.loads(state)
        if sheet is not None and level not in sheet.describes():
            raise SnapshotError(
                f"This Snapshot is at level {level}, but {sheet.name}'s Sheet only describes "
                f"levels {sheet.base_level}–{sheet.max_level}"
            )

        take(conn, cid, f"Before restoring “{label}”" if label else "Before restoring a Snapshot", automatic=True)

        columns = _columns(conn, "characters")
        play = {k: v for k, v in state["character"].items() if k in columns and k not in _KEPT_ON_RESTORE}
        if play:
            conn.execute(f"UPDATE characters SET {', '.join(f'{k}=?' for k in play)} WHERE id=?", (*play.values(), cid))
        for key, table in _TABLES:
            _restore_rows(conn, cid, table, state[key])

        if sheet is not None:
            try:
                apply_sheet(conn, sheet, cid)
            except SheetError as e:
                raise SnapshotError(str(e)) from e
            _, abilities, items = sheet.at(level)
            for table, entries in (("abilities", abilities), ("inventory", items)):
                described = {e["name"] for e in entries}
                for rid, name in conn.execute(
                    f"SELECT id, name FROM {table} WHERE character_id=? AND player_added=0", (cid,)
                ).fetchall():
                    if name not in described:
                        conn.execute(f"DELETE FROM {table} WHERE id=?", (rid,))


def diff(before, after):
    """What changed between two captures, for showing a Level-up."""
    return {
        "from_level": before["character"]["level"],
        "to_level": after["character"]["level"],
        "character": _field_changes(before["character"], after["character"]),
        **{key: _row_changes(before[key], after[key]) for key, _table in _TABLES},
    }


# ── internals ─────────────────────────────────────────────────────────────────


def _restore_rows(conn, cid, table, snap_rows):
    columns = _columns(conn, table) - _NOT_COMPARED
    current = defaultdict(list)
    for rid, name in conn.execute(f"SELECT id, name FROM {table} WHERE character_id=? ORDER BY id", (cid,)):
        current[name].append(rid)
    wanted = defaultdict(list)
    for r in snap_rows:
        wanted[r["name"]].append({k: v for k, v in r.items() if k in columns})

    for name in current.keys() | wanted.keys():
        ids, rows = current.get(name, []), wanted.get(name, [])
        for rid, r in zip(ids, rows):
            fields = {k: v for k, v in r.items() if k not in _ROW_KEPT_ON_RESTORE}
            sets = ", ".join(f"{k}=?" for k in fields)
            conn.execute(f"UPDATE {table} SET {sets} WHERE id=?", (*fields.values(), rid))
        for rid in ids[len(rows) :]:
            conn.execute(f"DELETE FROM {table} WHERE id=?", (rid,))
        for r in rows[len(ids) :]:
            row = {"character_id": cid, **r}
            conn.execute(
                f"INSERT INTO {table} ({', '.join(row)}) VALUES ({', '.join('?' * len(row))})", tuple(row.values())
            )


def _field_changes(before, after):
    return [
        {"field": k, "before": before.get(k), "after": v}
        for k, v in after.items()
        if k not in _NOT_COMPARED and before.get(k) != v
    ]


def _row_changes(before, after):
    old = {r["name"]: r for r in before}
    new = {r["name"]: r for r in after}
    ignored = _NOT_COMPARED | {"player_added"}
    changed = []
    for name in sorted(old.keys() & new.keys()):
        changes = [c for c in _field_changes(old[name], new[name]) if c["field"] not in ignored]
        if changes:
            changed.append({"name": name, "changes": changes})
    return {
        "gained": sorted(new.keys() - old.keys()),
        "retired": sorted(old.keys() - new.keys()),
        "changed": changed,
    }


def _strip(row):
    return {k: v for k, v in row.items() if k not in _NOT_COMPARED}


def _columns(conn, table):
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def _as_dict(conn, table, row):
    if hasattr(row, "keys"):
        return dict(row)
    return dict(zip([r[1] for r in conn.execute(f"PRAGMA table_info({table})")], row))
