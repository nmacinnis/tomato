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

        CREATE INDEX IF NOT EXISTS idx_abilities_char ON abilities(character_id);
        CREATE INDEX IF NOT EXISTS idx_inventory_char ON inventory(character_id);
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

    # Seed hit_dice_remaining = level for freshly migrated characters
    conn.execute("UPDATE characters SET hit_dice_remaining = level WHERE hit_dice_remaining = 0")

    _apply_tomato_data(conn)

    conn.commit()
    conn.close()


def _apply_tomato_data(conn):
    """Idempotent data migrations specific to the Tomato character sheet."""
    conn.execute(
        "UPDATE characters SET skill_proficiencies=? WHERE name='Tomato'",
        ("athletics,perception,animal_handling,survival,insight,stealth",),
    )
    conn.execute("UPDATE characters SET save_proficiencies='str,con' WHERE name='Tomato'")
    conn.execute("UPDATE characters SET flat_ac_bonus=1 WHERE name='Tomato'")

    # Re-categorize abilities into action-economy types
    ability_types = {
        "action": [
            "Cantrip: Druidcraft",
            "Cantrip: Guidance",
            "Spell: Goodberry",
            "Maneuver: Goading Attack",
            "Maneuver: Precision Attack",
        ],
        "bonus_action": [
            "Second Wind",
            "Know Your Enemy",
            "Maneuver: Rally",
        ],
        "reaction": [
            "Maneuver: Riposte",
            "Maneuver: Parry",
            "Feat — Sentinel: Guardian",
        ],
        "free_action": [
            "Action Surge",
            "Knowledge from a Past Life",
            "Indomitable",
            "Feat — Mage Slayer: Guarded Mind",
            "Superiority Dice Pool (d8)",
        ],
        "passive": [
            "Deathless Nature",
            "Extra Attack",
            "Fighting Style: Defense",
            "Tactical Mind (phb 2024)",
            "Tactical Shift",
            "Tactical Master",
            "Feat — Mage Slayer: Concentration Breaker",
            "Feat — Sentinel: Halt",
            "Rustic Hospitality",
            "Weapon Mastery: Spear (Sap)",
            "Weapon Mastery: Hand Axe (Vex)",
            "Weapon Mastery: Javelin (Slow)",
            "Weapon Mastery: Halberd (Cleave)",
        ],
    }
    for new_type, names in ability_types.items():
        for name in names:
            conn.execute("UPDATE abilities SET type=? WHERE name=?", (new_type, name))

    # Recharge types
    for name in ("Action Surge", "Second Wind", "Feat — Mage Slayer: Guarded Mind", "Superiority Dice Pool (d8)"):
        conn.execute("UPDATE abilities SET recharge='short' WHERE name=? AND recharge IS NULL", (name,))
    for name in ("Knowledge from a Past Life", "Know Your Enemy", "Indomitable", "Spell: Goodberry"):
        conn.execute("UPDATE abilities SET recharge='long' WHERE name=? AND recharge IS NULL", (name,))

    # AC values
    conn.execute("UPDATE inventory SET ac_bonus=17, sets_base_ac=1 WHERE name='Splint Armor'")
    conn.execute("UPDATE inventory SET ac_bonus=2  WHERE name='Shield'")
    conn.execute("UPDATE inventory SET ac_bonus=1  WHERE name='Cloak of Protection'")

    # Tool proficiencies
    for tool in ("Carpenter's Tools", "Tinker's Tools", "Herbalism Kit"):
        conn.execute("UPDATE inventory SET tool_proficient=1 WHERE name=?", (tool,))

    # Weapon stats
    weapons = [
        ("Spear",
         "1d6", "piercing", 0, 1, "Versatile (1d8), Thrown 20/60, Sap"),
        ("Hand Axe",
         "1d6", "slashing", 0, 1, "Light, Thrown 20/60, Vex"),
        ("Hand Axe (Shovel \u2014 sharpened WW1-style)",
         "1d6", "slashing", 0, 1, "Light, Thrown 20/60, Vex"),
        ("Javelin",
         "1d6", "piercing", 0, 1, "Thrown 30/120, Slow (STR-based)"),
        ("Halberd",
         "1d10", "slashing", 0, 1, "Reach, Heavy, Cleave"),
        ("Yester Hill Axe",
         "1d8", "slashing", 1, 1, "Versatile (1d10), +1d8 vs animals/plants/monstrosities"),
    ]
    for name, dd, dt, mb, im, notes in weapons:
        conn.execute(
            """UPDATE inventory
               SET damage_dice=?, damage_type=?, magic_bonus=?,
                   is_melee=?, damage_notes=?, is_weapon=1
               WHERE name=?""",
            (dd, dt, mb, im, notes, name),
        )
