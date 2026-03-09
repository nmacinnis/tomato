import os
import sqlite3
from flask import g

DATABASE = os.environ.get("DATABASE_PATH", "dnd.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_=None):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS characters (
            id                     INTEGER PRIMARY KEY AUTOINCREMENT,
            name                   TEXT    NOT NULL,
            race                   TEXT    NOT NULL DEFAULT 'Human',
            class                  TEXT    NOT NULL DEFAULT 'Fighter',
            level                  INTEGER NOT NULL DEFAULT 1,
            hp                     INTEGER NOT NULL DEFAULT 10,
            max_hp                 INTEGER NOT NULL DEFAULT 10,
            ac                     INTEGER NOT NULL DEFAULT 10,
            speed                  INTEGER NOT NULL DEFAULT 30,
            str                    INTEGER NOT NULL DEFAULT 10,
            dex                    INTEGER NOT NULL DEFAULT 10,
            con                    INTEGER NOT NULL DEFAULT 10,
            int                    INTEGER NOT NULL DEFAULT 10,
            wis                    INTEGER NOT NULL DEFAULT 10,
            cha                    INTEGER NOT NULL DEFAULT 10,
            notes                  TEXT    NOT NULL DEFAULT '',
            hit_dice_remaining     INTEGER NOT NULL DEFAULT 0,
            death_save_successes   INTEGER NOT NULL DEFAULT 0,
            death_save_failures    INTEGER NOT NULL DEFAULT 0,
            goodberries            INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS abilities (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id    INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
            name            TEXT    NOT NULL,
            type            TEXT    NOT NULL DEFAULT 'passive',
            description     TEXT    NOT NULL DEFAULT '',
            uses_max        INTEGER,
            uses_remaining  INTEGER,
            recharge        TEXT    -- 'short', 'long', or NULL
        );

        CREATE TABLE IF NOT EXISTS inventory (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id    INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
            name            TEXT    NOT NULL,
            quantity        INTEGER NOT NULL DEFAULT 1,
            weight          REAL    NOT NULL DEFAULT 0.0,
            description     TEXT    NOT NULL DEFAULT '',
            equipped        INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    # Migrate existing databases that predate these columns
    for col_def in (
        "hit_dice_remaining   INTEGER NOT NULL DEFAULT 0",
        "death_save_successes INTEGER NOT NULL DEFAULT 0",
        "death_save_failures  INTEGER NOT NULL DEFAULT 0",
        "goodberries          INTEGER NOT NULL DEFAULT 0",
    ):
        try:
            conn.execute(f"ALTER TABLE characters ADD COLUMN {col_def}")
        except sqlite3.OperationalError:
            pass
    try:
        conn.execute("ALTER TABLE abilities ADD COLUMN recharge TEXT")
    except sqlite3.OperationalError:
        pass
    for col_def in (
        "ac_bonus     INTEGER NOT NULL DEFAULT 0",
        "sets_base_ac INTEGER NOT NULL DEFAULT 0",
    ):
        try:
            conn.execute(f"ALTER TABLE inventory ADD COLUMN {col_def}")
        except sqlite3.OperationalError:
            pass
    try:
        conn.execute("ALTER TABLE characters ADD COLUMN flat_ac_bonus INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    # Set AC values on Tomato's items
    conn.execute("UPDATE inventory SET ac_bonus=17, sets_base_ac=1 WHERE name='Splint Armor'")
    conn.execute("UPDATE inventory SET ac_bonus=2  WHERE name='Shield'")
    conn.execute("UPDATE inventory SET ac_bonus=1  WHERE name='Cloak of Protection'")
    # Defense fighting style +1 AC while wearing armor
    conn.execute("UPDATE characters SET flat_ac_bonus=1 WHERE name='Tomato'")

    # Seed hit_dice_remaining = level for freshly migrated characters
    conn.execute("UPDATE characters SET hit_dice_remaining = level WHERE hit_dice_remaining = 0")

    # Tag Tomato's abilities with their recharge type
    short_rest = (
        "Action Surge",
        "Second Wind",
        "Feat — Mage Slayer: Guarded Mind",
        "Superiority Dice Pool (d8)",
    )
    long_rest = (
        "Knowledge from a Past Life",
        "Know Your Enemy",
        "Indomitable",
        "Spell: Goodberry",
    )
    for name in short_rest:
        conn.execute("UPDATE abilities SET recharge='short' WHERE name=? AND recharge IS NULL", (name,))
    for name in long_rest:
        conn.execute("UPDATE abilities SET recharge='long' WHERE name=? AND recharge IS NULL", (name,))

    conn.commit()
    conn.close()
