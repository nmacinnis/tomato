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
            goodberries            INTEGER NOT NULL DEFAULT 0,
            alignment              TEXT    NOT NULL DEFAULT '',
            size                   TEXT    NOT NULL DEFAULT 'Medium',
            height                 TEXT    NOT NULL DEFAULT '',
            weight                 TEXT    NOT NULL DEFAULT '',
            flat_ac_bonus          INTEGER NOT NULL DEFAULT 0,
            save_proficiencies     TEXT    NOT NULL DEFAULT '',
            temp_hp                INTEGER NOT NULL DEFAULT 0,
            skill_proficiencies    TEXT    NOT NULL DEFAULT '',
            languages              TEXT    NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS abilities (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id    INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
            name            TEXT    NOT NULL,
            type            TEXT    NOT NULL DEFAULT 'passive',
            description     TEXT    NOT NULL DEFAULT '',
            uses_max        INTEGER,
            uses_remaining  INTEGER,
            recharge        TEXT,    -- 'short', 'long', or NULL
            die_type        TEXT,    -- 'd4', 'd6', 'd8', 'd10', 'd12', 'd20', or NULL
            ac_bonus        INTEGER NOT NULL DEFAULT 0,
            save_bonus      INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS inventory (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id    INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
            name            TEXT    NOT NULL,
            quantity        INTEGER NOT NULL DEFAULT 1,
            weight          REAL    NOT NULL DEFAULT 0.0,
            description     TEXT    NOT NULL DEFAULT '',
            equipped        INTEGER NOT NULL DEFAULT 0,
            save_bonus      INTEGER NOT NULL DEFAULT 0,
            ac_bonus        INTEGER NOT NULL DEFAULT 0,
            sets_base_ac    INTEGER NOT NULL DEFAULT 0,
            tool_proficient INTEGER NOT NULL DEFAULT 0,
            damage_dice     TEXT    NOT NULL DEFAULT '',
            damage_type     TEXT    NOT NULL DEFAULT '',
            damage_notes    TEXT    NOT NULL DEFAULT '',
            magic_bonus     INTEGER NOT NULL DEFAULT 0,
            is_weapon       INTEGER NOT NULL DEFAULT 0,
            is_melee        INTEGER NOT NULL DEFAULT 1
        );

        CREATE INDEX IF NOT EXISTS idx_abilities_char ON abilities(character_id);
        CREATE INDEX IF NOT EXISTS idx_inventory_char ON inventory(character_id);

        CREATE TABLE IF NOT EXISTS themes (
            character_id INTEGER PRIMARY KEY REFERENCES characters(id) ON DELETE CASCADE,
            accent       TEXT NOT NULL DEFAULT '#e94560',
            accent2      TEXT NOT NULL DEFAULT '#c7a026',
            bg           TEXT NOT NULL DEFAULT '#1a1a2e',
            surface      TEXT NOT NULL DEFAULT '#16213e',
            panel_color  TEXT NOT NULL DEFAULT '#0f3460',
            border       TEXT NOT NULL DEFAULT '#2a3a5e'
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
    try:
        conn.execute("ALTER TABLE characters ADD COLUMN save_proficiencies TEXT NOT NULL DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE characters ADD COLUMN temp_hp INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE characters ADD COLUMN skill_proficiencies TEXT NOT NULL DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE inventory ADD COLUMN tool_proficient INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE characters ADD COLUMN languages TEXT NOT NULL DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE abilities ADD COLUMN die_type TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE abilities ADD COLUMN ac_bonus INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE abilities ADD COLUMN save_bonus INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE inventory ADD COLUMN save_bonus INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    for col_def in (
        "alignment TEXT NOT NULL DEFAULT ''",
        "size      TEXT NOT NULL DEFAULT 'Medium'",
        "height    TEXT NOT NULL DEFAULT ''",
        "weight    TEXT NOT NULL DEFAULT ''",
    ):
        try:
            conn.execute(f"ALTER TABLE characters ADD COLUMN {col_def}")
        except sqlite3.OperationalError:
            pass

    for col_def in (
        "damage_dice  TEXT    NOT NULL DEFAULT ''",
        "damage_type  TEXT    NOT NULL DEFAULT ''",
        "damage_notes TEXT    NOT NULL DEFAULT ''",
        "magic_bonus  INTEGER NOT NULL DEFAULT 0",
        "is_weapon    INTEGER NOT NULL DEFAULT 0",
        "is_melee     INTEGER NOT NULL DEFAULT 1",
    ):
        try:
            conn.execute(f"ALTER TABLE inventory ADD COLUMN {col_def}")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()
