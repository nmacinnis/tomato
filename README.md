# D&D Character Tracker

A simple web app to manage your D&D 5e character sheets — ability scores, HP, abilities/spells, and inventory — all in one dark-themed interface.

## Features

- **Character roster** — create and manage multiple characters
- **Ability scores** — click any score to edit it inline; modifiers calculated automatically
- **Combat stats** — HP tracker with +/− buttons, AC, speed, level
- **Abilities & spells** — passive, active, and spell types; track uses-per-rest
- **Inventory** — items with quantity, weight (auto-totals carry weight), and equipped status
- **Skills & saving throws** — proficiency toggles, ability-linked bonuses
- **Death saves** — track successes/failures with survival odds display
- **AC breakdown** — collapsible equation with item/ability contribution detail
- **Notes** — freeform text field per character
- **Snapshots** — save a dated copy of a character's current state and restore it later (a restore snapshots first, so it can be undone)
- **Level up** — preview the next level written in the character's Sheet, then apply it mid-session

---

## Running locally

**Requirements:** Python 3.10+, Node.js (for linting/formatting)

```bash
# 1. Clone / enter the project directory
cd tomato

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install JS dev dependencies (eslint + prettier)
npm install

# 5. Initialize the database (run once)
python init_db.py

# 6. Start the dev server
python app.py
```

Open http://localhost:5000 in your browser.

### Linting & formatting

```bash
# Python (ruff)
ruff check .          # lint
ruff format .         # format

# JavaScript (eslint + prettier)
npm run lint          # lint
npm run lint:fix      # lint + auto-fix
npm run format        # format
npm run format:check  # check formatting without writing
```

---

## Deploying to Railway

[Railway](https://railway.app) is the simplest way to host this — no YAML, no Docker required.

1. Push this project to a GitHub repository.
2. Go to [railway.app](https://railway.app) and sign in with GitHub.
3. Click **New Project → Deploy from GitHub repo** and select your repo.
4. Railway auto-detects the `Procfile` and deploys with gunicorn.
5. Click the generated URL — done.

> **Note on the database:** Railway's filesystem is ephemeral (resets on redeploy). For a persistent database, add a Railway **Volume** and set the `DATABASE` path in `database.py` to point to it, or swap SQLite for Railway's managed Postgres.

---

## Project structure

```
tomato/
├── app.py               — Flask REST API + page routes
├── database.py          — SQLite connection + schema
├── init_db.py           — One-time database setup
├── characters/          — Character Sheets + Seeding (see GLOSSARY.md)
│   ├── __init__.py      — seed_all(): syncs Sheets into the DB on boot; Level-up
│   ├── inkwell.py       — Inkwell's Sheet + Seed steps
│   └── tomato.py        — TOMATO's Sheet + Seed steps
├── snapshots.py         — Snapshots: take / restore a character's state
├── docs/adr/            — Architecture decision records
├── tests/               — pytest (python -m pytest)
├── GLOSSARY.md          — Domain terms
├── requirements.txt
├── pyproject.toml       — ruff (Python linter/formatter) config
├── package.json         — eslint + prettier config & scripts
├── Procfile             — gunicorn entry point for Railway
├── CLAUDE.md            — AI assistant context
├── .gitignore
├── templates/
│   ├── index.html       — Character roster
│   └── character.html   — Character sheet
└── static/
    ├── style.css        — Dark fantasy theme
    ├── app.js           — Shared utilities
    ├── character.js     — Sheet entry point
    ├── character-stats.js    — Ability scores & combat stats
    ├── character-abilities.js — Abilities & spells
    ├── character-inventory.js — Inventory management
    ├── character-skills.js   — Skills & saving throws
    ├── character-utils.js    — Shared helpers
    └── character-theme.js    — Theme / UI utilities
```

---

## API reference

All endpoints return/accept JSON.

### Characters

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/characters` | List all characters |
| POST | `/api/characters` | Create a character |
| GET | `/api/characters/:id` | Get a character |
| PUT | `/api/characters/:id` | Update character fields |
| DELETE | `/api/characters/:id` | Delete character (cascades) |

### Abilities

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/characters/:id/abilities` | List abilities |
| POST | `/api/characters/:id/abilities` | Add an ability |
| PUT | `/api/abilities/:id` | Edit an ability |
| DELETE | `/api/abilities/:id` | Remove an ability |

### Inventory

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/characters/:id/inventory` | List items |
| POST | `/api/characters/:id/inventory` | Add an item |
| PUT | `/api/inventory/:id` | Edit an item |
| DELETE | `/api/inventory/:id` | Remove an item |

---

## Tech stack

| Layer | Tech |
|-------|------|
| Backend | Python 3 + Flask |
| Database | SQLite (via `sqlite3` stdlib) |
| Frontend | HTML + CSS + vanilla JS |
| Prod server | gunicorn |
| Hosting | Railway |
| Python linting | ruff |
| JS linting | eslint |
| JS formatting | prettier |
