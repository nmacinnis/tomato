import sqlite3
from flask import g

DATABASE = "dnd.db"


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
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            race      TEXT    NOT NULL DEFAULT 'Human',
            class     TEXT    NOT NULL DEFAULT 'Fighter',
            level     INTEGER NOT NULL DEFAULT 1,
            hp        INTEGER NOT NULL DEFAULT 10,
            max_hp    INTEGER NOT NULL DEFAULT 10,
            ac        INTEGER NOT NULL DEFAULT 10,
            speed     INTEGER NOT NULL DEFAULT 30,
            str       INTEGER NOT NULL DEFAULT 10,
            dex       INTEGER NOT NULL DEFAULT 10,
            con       INTEGER NOT NULL DEFAULT 10,
            int       INTEGER NOT NULL DEFAULT 10,
            wis       INTEGER NOT NULL DEFAULT 10,
            cha       INTEGER NOT NULL DEFAULT 10,
            notes     TEXT    NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS abilities (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id    INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
            name            TEXT    NOT NULL,
            type            TEXT    NOT NULL DEFAULT 'passive',
            description     TEXT    NOT NULL DEFAULT '',
            uses_max        INTEGER,
            uses_remaining  INTEGER
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
    conn.close()
