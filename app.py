from flask import Flask, jsonify, request, render_template
from database import init_db, get_db, close_db, DATABASE

app = Flask(__name__)
app.teardown_appcontext(close_db)
init_db()

# Seed Tomato's data on first run if the database is empty
import sqlite3 as _sqlite3
with _sqlite3.connect(DATABASE) as _c:
    if _c.execute("SELECT COUNT(*) FROM characters").fetchone()[0] == 0:
        import runpy
        runpy.run_path("seed_tomato.py")


# ── Pages ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/character/<int:character_id>")
def character_page(character_id):
    return render_template("character.html", character_id=character_id)


# ── Characters ─────────────────────────────────────────────────────────────────

@app.route("/api/characters", methods=["GET"])
def list_characters():
    db = get_db()
    rows = db.execute("SELECT * FROM characters ORDER BY name").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/characters", methods=["POST"])
def create_character():
    data = request.json
    db = get_db()
    cur = db.execute(
        """INSERT INTO characters
           (name, race, class, level, hp, max_hp, ac, speed,
            str, dex, con, int, wis, cha, notes)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            data.get("name", "Unnamed Hero"),
            data.get("race", "Human"),
            data.get("class", "Fighter"),
            data.get("level", 1),
            data.get("hp", 10),
            data.get("max_hp", 10),
            data.get("ac", 10),
            data.get("speed", 30),
            data.get("str", 10),
            data.get("dex", 10),
            data.get("con", 10),
            data.get("int", 10),
            data.get("wis", 10),
            data.get("cha", 10),
            data.get("notes", ""),
        ),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/characters/<int:cid>", methods=["GET"])
def get_character(cid):
    db = get_db()
    row = db.execute("SELECT * FROM characters WHERE id=?", (cid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


@app.route("/api/characters/<int:cid>", methods=["PUT"])
def update_character(cid):
    data = request.json
    db = get_db()
    fields = [
        "name", "race", "class", "level", "hp", "max_hp", "ac", "speed",
        "str", "dex", "con", "int", "wis", "cha", "notes",
        "hit_dice_remaining", "death_save_successes", "death_save_failures", "goodberries",
        "flat_ac_bonus", "ac", "save_proficiencies",
    ]
    set_clause = ", ".join(f"{f}=?" for f in fields if f in data)
    values = [data[f] for f in fields if f in data]
    if not set_clause:
        return jsonify({"error": "No fields to update"}), 400
    db.execute(f"UPDATE characters SET {set_clause} WHERE id=?", values + [cid])
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/characters/<int:cid>", methods=["DELETE"])
def delete_character(cid):
    db = get_db()
    db.execute("DELETE FROM characters WHERE id=?", (cid,))
    db.commit()
    return jsonify({"ok": True})


# ── Abilities ──────────────────────────────────────────────────────────────────

@app.route("/api/characters/<int:cid>/abilities", methods=["GET"])
def list_abilities(cid):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM abilities WHERE character_id=? ORDER BY name", (cid,)
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/characters/<int:cid>/abilities", methods=["POST"])
def create_ability(cid):
    data = request.json
    db = get_db()
    cur = db.execute(
        """INSERT INTO abilities (character_id, name, type, description, uses_max, uses_remaining, recharge)
           VALUES (?,?,?,?,?,?,?)""",
        (
            cid,
            data.get("name", "New Ability"),
            data.get("type", "passive"),
            data.get("description", ""),
            data.get("uses_max", None),
            data.get("uses_max", None),
            data.get("recharge", None),
        ),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/characters/<int:cid>/rest", methods=["POST"])
def do_rest(cid):
    rest_type = request.json.get("type")  # 'short' or 'long'
    if rest_type not in ("short", "long"):
        return jsonify({"error": "type must be 'short' or 'long'"}), 400
    db = get_db()

    if rest_type == "short":
        db.execute(
            "UPDATE abilities SET uses_remaining=uses_max WHERE character_id=? AND recharge='short'",
            (cid,),
        )
        db.execute(
            "UPDATE characters SET death_save_successes=0, death_save_failures=0 WHERE id=?",
            (cid,),
        )

    elif rest_type == "long":
        db.execute(
            "UPDATE abilities SET uses_remaining=uses_max WHERE character_id=? AND uses_max IS NOT NULL",
            (cid,),
        )
        char = db.execute("SELECT level FROM characters WHERE id=?", (cid,)).fetchone()
        db.execute(
            """UPDATE characters
               SET hp=max_hp, hit_dice_remaining=level,
                   death_save_successes=0, death_save_failures=0,
                   goodberries=10
               WHERE id=?""",
            (cid,),
        )

    db.commit()
    return jsonify({"ok": True, "type": rest_type})


@app.route("/api/abilities/<int:aid>", methods=["PUT"])
def update_ability(aid):
    data = request.json
    db = get_db()
    fields = ["name", "type", "description", "uses_max", "uses_remaining", "recharge"]
    set_clause = ", ".join(f"{f}=?" for f in fields if f in data)
    values = [data[f] for f in fields if f in data]
    if not set_clause:
        return jsonify({"error": "No fields to update"}), 400
    db.execute(f"UPDATE abilities SET {set_clause} WHERE id=?", values + [aid])
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/abilities/<int:aid>", methods=["DELETE"])
def delete_ability(aid):
    db = get_db()
    db.execute("DELETE FROM abilities WHERE id=?", (aid,))
    db.commit()
    return jsonify({"ok": True})


# ── Inventory ──────────────────────────────────────────────────────────────────

@app.route("/api/characters/<int:cid>/inventory", methods=["GET"])
def list_inventory(cid):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM inventory WHERE character_id=? ORDER BY name", (cid,)
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/characters/<int:cid>/inventory", methods=["POST"])
def create_item(cid):
    data = request.json
    db = get_db()
    cur = db.execute(
        """INSERT INTO inventory (character_id, name, quantity, weight, description, equipped)
           VALUES (?,?,?,?,?,?)""",
        (
            cid,
            data.get("name", "Item"),
            data.get("quantity", 1),
            data.get("weight", 0.0),
            data.get("description", ""),
            data.get("equipped", False),
        ),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/inventory/<int:iid>", methods=["PUT"])
def update_item(iid):
    data = request.json
    db = get_db()
    fields = ["name", "quantity", "weight", "description", "equipped", "ac_bonus", "sets_base_ac"]
    set_clause = ", ".join(f"{f}=?" for f in fields if f in data)
    values = [data[f] for f in fields if f in data]
    if not set_clause:
        return jsonify({"error": "No fields to update"}), 400
    db.execute(f"UPDATE inventory SET {set_clause} WHERE id=?", values + [iid])
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/inventory/<int:iid>", methods=["DELETE"])
def delete_item(iid):
    db = get_db()
    db.execute("DELETE FROM inventory WHERE id=?", (iid,))
    db.commit()
    return jsonify({"ok": True})


# ── Boot ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
