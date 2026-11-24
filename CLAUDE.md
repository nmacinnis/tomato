# CLAUDE.md — DnD Character Tracker

This file gives Claude context about the project so it can assist effectively.

## Project overview

A lightweight web app to track D&D 5e character sheets: ability scores, HP/AC,
abilities/spells, and inventory. Built with Flask + SQLite on the backend and
vanilla HTML/CSS/JS on the frontend. No JS framework — keep it that way unless
there is a compelling reason to add one.

## Architecture

```
app.py          — Flask routes (REST API + page rendering)
database.py     — SQLite connection management and schema init
init_db.py      — One-time DB setup script
characters/
  __init__.py   — Seeding (seed_all runs on boot) and Level-up (see GLOSSARY.md)
  inkwell.py    — Sheet (CHARACTER / ABILITIES / ITEMS dicts) + LEVELS + STEPS
  tomato.py     — Sheet + LEVELS + STEPS
spells.py       — Shared spell list: Rules text (SRD 5.2 only) or a 5e.tools link + card details
snapshots.py    — Snapshots: take / restore a Character's Play state and rows
tests/          — pytest, run with `python -m pytest`
GLOSSARY.md     — Domain terms: Sheet, Level, Play state, Level-up, Snapshot, Player-added, Seeding, Seed step
docs/adr/       — Architecture decisions (0001: level is Play state)
templates/
  index.html    — Character roster page
  character.html — Character sheet page
static/
  style.css     — All styles (dark DnD theme)
  app.js        — Shared utilities (loadCharacters, escHtml, modifier)
  character.js  — Character sheet interactions
  character-snapshots.js — Snapshots panel + Level-up preview dialog
requirements.txt
Procfile        — gunicorn entry point for Railway/Render
```

## Data model

Three tables, all joined by `character_id`:

| Table        | Key fields                                                               |
|--------------|--------------------------------------------------------------------------|
| `characters` | name, race, class, level, hp, max_hp, ac, speed, str/dex/con/int/wis/cha |
| `abilities`  | name, type (passive/active/spell), description, uses_max, uses_remaining |
| `inventory`  | name, quantity, weight, description, equipped                            |

## API summary

```
GET  /api/characters
POST /api/characters
GET  /api/characters/:id
PUT  /api/characters/:id
DEL  /api/characters/:id

GET  /api/characters/:id/abilities
POST /api/characters/:id/abilities
PUT  /api/abilities/:id
DEL  /api/abilities/:id

GET  /api/characters/:id/inventory
POST /api/characters/:id/inventory
PUT  /api/inventory/:id
DEL  /api/inventory/:id
```

## Common commands

```bash
# First-time setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python init_db.py

# Run dev server
python app.py          # http://localhost:5000

# Run tests
python -m pytest

# Run with gunicorn (production-like)
gunicorn "app:app"
```

## Conventions

- **No ORM.** Use plain `sqlite3` with parameterized queries. Do not add SQLAlchemy.
- **No JS framework.** Vanilla JS only. Do not add React/Vue/Alpine.
- **REST only.** All data is returned as JSON from `/api/*` routes. Templates contain no business logic.
- **Single SQLite file** (`dnd.db`). Do not introduce Postgres/MySQL unless the user explicitly asks.
- **Characters are seeded, not hand-migrated.** Edit a character by editing its Sheet in
  `characters/<name>.py`; seeding overwrites Sheet fields (from the Sheet at the Character's
  current level) on every boot and never touches Play state (`PLAY_FIELDS` in
  `characters/__init__.py`, which includes `level`) after creation.
- **Level-ups are authored ahead, applied at the table.** To prepare the next level, add a
  block to the module's `LEVELS` (format in `characters/__init__.py`): new Sheet values,
  abilities/items gained or changed, and `retire_abilities`/`retire_items`. Every choice
  (HP gain, feats, spells) is decided there. The player presses Level up in the UI; don't
  bump `level` in `CHARACTER` and don't write a Seed step for it. See ADR 0001.
- **Spells name an entry in `spells.py`.** A spell ability in a Sheet sets `"spell": "<name>"`;
  Seeding fills its Rules text, source, range, components, duration, concentration and level
  from `spells.py` (the Sheet may override `spell_level` only). Its `description` is the
  Summary, written for this Character. Rules text is copied word-for-word from 5e.tools
  (2024 PHB when the spell is in it) and never edited to add character notes.
- **Only SRD 5.2 spell text goes in the repo** (it's public; the SRD is CC-BY-4.0, credited in
  `character.html`'s footer). A spell not in the SRD gets a `rules_url` to its 5e.tools page,
  never a pasted `rules_text`. Summaries are our own paraphrase and are fine for any spell.
- **Seed steps** are for renames, retirements outside a Level-up, and data-shape changes:
  steps run once per database, before the Sheet refresh.
- **Play state is written only** by the table (the API), Level-up, Snapshot restore, or a
  Seed step. Never write raw UPDATEs to Play state anywhere else.
- **Gunicorn in prod.** The `Procfile` targets Railway/Render. Do not change the entry point without updating this file.

## Extending the project

Common tasks Claude might be asked to help with:

- **Add a new field** (e.g. `proficiency_bonus`): add column to `init_db.py` schema, add to `PUT` handler field list in `app.py`, render in `character.js`.
- **Add spell slots**: new table `spell_slots(character_id, level, total, used)` — same pattern as abilities.
- **Add saving throws / skills**: new table or JSON column on the character row.
- **Persist uses_remaining across sessions**: already stored in DB — `Use` button PATCHes immediately.
- **Add a long rest button**: call `PUT /api/abilities/:id` for each ability setting `uses_remaining = uses_max`.
