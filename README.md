# D&D Character Tracker

A simple web app to manage your D&D 5e character sheets — ability scores, HP, abilities/spells, and inventory — all in one dark-themed interface.

## Features

- **Character roster** — create and manage multiple characters
- **Ability scores** — click any score to edit it inline; modifiers calculated automatically
- **Combat stats** — HP tracker with +/− buttons, AC, speed, level
- **Abilities & spells** — passive, active, and spell types; track uses-per-rest
- **Inventory** — items with quantity, weight (auto-totals carry weight), and equipped status
- **Notes** — freeform text field per character

---

## Running locally

**Requirements:** Python 3.10+

```bash
# 1. Clone / enter the project directory
cd tomato

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database (run once)
python init_db.py

# 5. Start the dev server
python app.py
```

Open http://localhost:5000 in your browser.

---

## Deploying to Railway (recommended)

[Railway](https://railway.app) is the simplest way to host this — no YAML, no Docker required.

1. Push this project to a GitHub repository.
2. Go to [railway.app](https://railway.app) and sign in with GitHub.
3. Click **New Project → Deploy from GitHub repo** and select your repo.
4. Railway auto-detects the `Procfile` and deploys with gunicorn.
5. Click the generated URL — done.

> **Note on the database:** Railway's filesystem is ephemeral (resets on redeploy). For a persistent database, add a Railway **Volume** and set the `DATABASE` path in `database.py` to point to it, or swap SQLite for Railway's managed Postgres.

### Alternative: Render

1. Push to GitHub.
2. At [render.com](https://render.com), create a **New Web Service**.
3. Set **Build command:** `pip install -r requirements.txt && python init_db.py`
4. Set **Start command:** `gunicorn "app:app"`
5. Deploy. Render also supports persistent disks for the SQLite file.

---

## Project structure

```
tomato/
├── app.py           — Flask REST API + page routes
├── database.py      — SQLite connection + schema
├── init_db.py       — One-time database setup
├── requirements.txt
├── Procfile         — gunicorn entry point for Railway/Render
├── CLAUDE.md        — AI assistant context
├── .gitignore
├── templates/
│   ├── index.html   — Character roster
│   └── character.html — Character sheet
└── static/
    ├── style.css    — Dark fantasy theme
    ├── app.js       — Shared utilities
    └── character.js — Sheet interactions
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

## Suggested frontend improvements

The current frontend is intentional plain vanilla JS — zero build step, zero dependencies. If you want to go further:

- **[HTMX](https://htmx.org)** — add a single `<script>` tag and get reactive updates without writing JS
- **[Alpine.js](https://alpinejs.dev)** — lightweight reactivity via HTML attributes, still no build step
- **React/Vite** — only if you need complex state (e.g. drag-and-drop inventory, dice roller)

For most D&D tracker use cases, HTMX is the sweet spot.

---

## Tech stack

| Layer | Tech |
|-------|------|
| Backend | Python 3 + Flask |
| Database | SQLite (via `sqlite3` stdlib) |
| Frontend | HTML + CSS + vanilla JS |
| Prod server | gunicorn |
| Hosting | Railway or Render |
