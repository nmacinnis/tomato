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
templates/
  index.html    — Character roster page
  character.html — Character sheet page
static/
  style.css     — All styles (dark DnD theme)
  app.js        — Shared utilities (loadCharacters, escHtml, modifier)
  character.js  — Character sheet interactions
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

# Run with gunicorn (production-like)
gunicorn "app:app"
```

## Conventions

- **No ORM.** Use plain `sqlite3` with parameterized queries. Do not add SQLAlchemy.
- **No JS framework.** Vanilla JS only. Do not add React/Vue/Alpine.
- **REST only.** All data is returned as JSON from `/api/*` routes. Templates contain no business logic.
- **Single SQLite file** (`dnd.db`). Do not introduce Postgres/MySQL unless the user explicitly asks.
- **Gunicorn in prod.** The `Procfile` targets Railway/Render. Do not change the entry point without updating this file.

## Extending the project

Common tasks Claude might be asked to help with:

- **Add a new field** (e.g. `proficiency_bonus`): add column to `init_db.py` schema, add to `PUT` handler field list in `app.py`, render in `character.js`.
- **Add spell slots**: new table `spell_slots(character_id, level, total, used)` — same pattern as abilities.
- **Add saving throws / skills**: new table or JSON column on the character row.
- **Persist uses_remaining across sessions**: already stored in DB — `Use` button PATCHes immediately.
- **Add a long rest button**: call `PUT /api/abilities/:id` for each ability setting `uses_remaining = uses_max`.
