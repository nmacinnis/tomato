"""Seed the database with Tomato's character sheet."""
import sqlite3
from database import init_db, DATABASE

init_db()
db = sqlite3.connect(DATABASE)

# ── Character ──────────────────────────────────────────────────────────────────
cur = db.execute(
    """INSERT INTO characters
       (name, race, class, level, hp, max_hp, ac, speed,
        str, dex, con, int, wis, cha, notes)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
    (
        "Tomato",
        "Reborn Warforged",
        "Battlemaster Fighter",
        9,
        87, 87,
        19,   # splint + defense + cloak (shield bumps to 21 in combat)
        30,
        20, 12, 16, 8, 13, 10,
        (
            "Proficiency bonus: +4  |  Maneuver save DC: 17  |  "
            "Alignment: Chaotic Good  |  Size: Medium (6'6\", 302 lbs)\n\n"
            "Background: Folk Hero — stood up to Zhentarim agents raiding her village. "
            "Defining event awakened her dormant consciousness.\n\n"
            "Languages: Common, Sylvan\n"
            "Trinket: A single seed from the Harvest House in Daggerford\n"
            "Heraldic Sign: Crossed Wrench and Scythe (maker's mark)\n\n"
            "Personality: If someone is in trouble, I'm always ready to lend help.\n"
            "Ideal: Freedom — tyrants must not be allowed to oppress the people.\n"
            "Bond: I protect those who cannot protect themselves.\n"
            "Flaw: The people who knew me when I was young know my shameful secret — "
            "the villagers who owned me see me as a friend, but they are afraid of me anyway."
        ),
    ),
)
cid = cur.lastrowid
db.commit()

# ── Abilities ──────────────────────────────────────────────────────────────────
abilities = [

    # Racial — Reborn Warforged
    ("Deathless Nature", "passive",
     "Advantage on saves vs disease and poison; resistance to poison damage. "
     "Advantage on death saving throws. No need to eat, drink, or breathe. "
     "No sleep needed; long rest in 4 hrs while inactive (retains consciousness). "
     "Magic cannot put you to sleep.",
     None),

    ("Knowledge from a Past Life", "active",
     "When you make an ability check using a skill, roll a d6 immediately after seeing "
     "the d20 result and add it to the check. "
     "Regains all uses on long rest.",
     4),   # = proficiency bonus

    # Fighter core
    ("Action Surge", "active",
     "Take one additional action on your turn (not the Magic action). "
     "Once per Short or Long Rest.",
     1),

    ("Second Wind", "active",
     "Bonus action: regain 1d10 + 9 (fighter level) HP. "
     "Also usable via Tactical Mind: expend a use to add 1d10 to a failed ability check "
     "(if the check still fails, the use is not expended). "
     "Tactical Shift: when activated as a bonus action, may move up to 15 ft without "
     "provoking Opportunity Attacks.",
     3),

    ("Know Your Enemy", "active",
     "Bonus Action: learn whether a visible creature within 30 ft has any Immunities, "
     "Resistances, or Vulnerabilities, and what they are. "
     "1 use per Long Rest; can restore by expending one Superiority Die (no action).",
     1),

    ("Indomitable", "active",
     "When you fail a saving throw, reroll it with a bonus equal to your Fighter level (+9). "
     "You must use the new roll. Once per Long Rest.",
     1),

    ("Extra Attack", "passive",
     "Attack twice whenever you take the Attack action on your turn.",
     None),

    ("Fighting Style: Defense", "passive",
     "+1 AC while wearing armor. (Contributes to current AC of 19; 21 with shield.)",
     None),

    ("Tactical Shift", "passive",
     "When you activate Second Wind as a Bonus Action, you may move up to half your Speed "
     "(15 ft) without provoking Opportunity Attacks.",
     None),

    ("Tactical Master", "passive",
     "When attacking with a weapon whose Mastery property you can use, you may replace "
     "that property with Push, Sap, or Slow for that attack.",
     None),

    # Battlemaster Maneuvers — shared pool of 4d8 superiority dice
    ("Superiority Dice Pool (d8)", "active",
     "Pool of 4 superiority dice (d8) shared across all maneuvers. "
     "Regain all on Short or Long Rest. "
     "Maneuver save DC: 17 (8 + STR mod +4 prof + 1).",
     4),

    ("Maneuver: Goading Attack", "active",
     "Expend 1 Superiority Die. On a hit, add the die to damage and the target must make "
     "a Wis save (DC 17) or have Disadvantage on attacks against targets other than you "
     "until the end of its next turn.",
     None),

    ("Maneuver: Rally", "active",
     "Bonus Action: expend 1 Superiority Die. An ally you can see gains temp HP equal to "
     "the die result + 4 (half fighter level, rounded down).",
     None),

    ("Maneuver: Riposte", "active",
     "Reaction: when a creature misses you with a melee attack, expend 1 Superiority Die "
     "to make one melee weapon attack against the creature. On a hit, add the die to damage.",
     None),

    ("Maneuver: Precision Attack", "active",
     "Expend 1 Superiority Die immediately after seeing the d20 roll for an attack. "
     "Add the die result to the attack roll. Can be used before or after knowing if it hits.",
     None),

    ("Maneuver: Parry", "active",
     "Reaction: when you take damage from a melee attack, expend 1 Superiority Die "
     "to reduce the damage by the die result + STR modifier (+5). Total reduction: d8+5.",
     None),

    # Feats
    ("Feat — Mage Slayer: Guarded Mind", "active",
     "If you fail an Intelligence, Wisdom, or Charisma saving throw, you can cause yourself "
     "to succeed instead. Once per Short or Long Rest. "
     "Flavor: Tomato's half-organic, half-mechanical brain — if one half is charmed, "
     "the other half can break the spell.",
     1),

    ("Feat — Mage Slayer: Concentration Breaker", "passive",
     "When you damage a creature that is Concentrating, it has Disadvantage on its "
     "Constitution saving throw to maintain concentration.",
     None),

    ("Feat — Sentinel: Guardian", "passive",
     "You can make an Opportunity Attack when a creature within 5 ft of you takes the "
     "Disengage action OR hits a target other than you with an attack.",
     None),

    ("Feat — Sentinel: Halt", "passive",
     "When you hit a creature with an Opportunity Attack, that creature's Speed becomes 0 "
     "for the rest of the current turn.",
     None),

    # Magic Initiate (Druid) — innate dryad magic
    ("Cantrip: Druidcraft", "spell",
     "Create minor nature effects: predict weather, make a flower bloom, light a campfire, "
     "create a sensory effect. Unlimited uses.",
     None),

    ("Cantrip: Guidance", "spell",
     "Touch a willing creature. Once before the spell ends (concentration, up to 1 minute) "
     "the creature can roll a d4 and add it to one ability check. Unlimited uses.",
     None),

    ("Spell: Goodberry", "spell",
     "Up to 10 magical berries appear. A berry restores 1 HP and provides nourishment for "
     "a day. Berries last 24 hours. Once per Long Rest (Magic Initiate).",
     1),

    # Background
    ("Rustic Hospitality", "passive",
     "Among common folk you fit in with ease. You can find a place to hide, rest, or "
     "recuperate with commoners, who will shield you from law or pursuers — "
     "though they will not risk their lives for you.",
     None),

    # Weapon Mastery
    ("Weapon Mastery: Spear (Sap)", "passive",
     "On a hit with a Spear, the target has Disadvantage on its next attack roll before "
     "the start of your next turn.",
     None),

    ("Weapon Mastery: Hand Axe (Vex)", "passive",
     "On a hit with a Hand Axe, you gain Advantage on your next attack roll against "
     "that creature before the end of your next turn.",
     None),

    ("Weapon Mastery: Javelin (Slow)", "passive",
     "On a hit with a Javelin, the target's Speed is reduced by 10 ft until the start "
     "of your next turn.",
     None),

    ("Weapon Mastery: Halberd (Cleave)", "passive",
     "On a hit with a Halberd, you may make an additional attack against a second creature "
     "within reach that is within 5 ft of the original target. No attack roll bonus applies.",
     None),
]

for name, atype, desc, uses in abilities:
    db.execute(
        """INSERT INTO abilities
           (character_id, name, type, description, uses_max, uses_remaining)
           VALUES (?,?,?,?,?,?)""",
        (cid, name, atype, desc, uses, uses),
    )

# ── Inventory ──────────────────────────────────────────────────────────────────
items = [
    # Armor & shield
    ("Splint Armor", 1, 60.0,
     "AC 17. Heavy armor; Disadvantage on Stealth checks.", True),
    ("Shield", 1, 6.0,
     "+2 AC when equipped. Bumps total AC to 21.", False),
    ("Cloak of Protection", 1, 1.0,
     "+1 AC (already included in base AC 19) and +1 to all saving throws.", True),

    # Weapons
    ("Spear", 1, 3.0,
     "1d6 piercing (1d8 versatile). Thrown (20/60). Mastery: Sap. "
     "Starting equipment.", True),
    ("Hand Axe", 1, 2.0,
     "1d6 slashing. Light, Thrown (20/60). Mastery: Vex. Starting equipment.", False),
    ("Hand Axe (Shovel — sharpened WW1-style)", 1, 5.0,
     "1d6 slashing. Light, Thrown (20/60). Mastery: Vex. "
     "Actually Tomato's shovel from her Folk Hero days, sharpened for combat.", False),
    ("Javelin", 1, 2.0,
     "1d6 piercing. Thrown (30/120). Mastery: Slow. Starting equipment.", False),
    ("Halberd", 1, 6.0,
     "2-handed. 1d10 slashing. Reach. Heavy. Mastery: Cleave. "
     "Picked up during adventuring.", True),
    ("Yester Hill Axe", 1, 4.0,
     "+1 Battleaxe. 1d8+1 slashing (1d10+1 versatile). "
     "+1d8 damage against animals, plants, and monstrosities.", True),

    # Tools & gear
    ("Carpenter's Tools", 1, 6.0,
     "Proficiency from Student of War. Used for construction and repair.", False),
    ("Tinker's Tools", 1, 10.0,
     "Proficiency from Folk Hero background. Used for mechanical tinkering.", False),
    ("Herbalism Kit", 1, 3.0,
     "Proficiency from Ancestral Legacy (Reborn). Used to identify and apply herbs.", False),

    # Dungeoneer's Pack contents
    ("Backpack", 1, 5.0, "Container for gear.", False),
    ("Crowbar", 1, 5.0, "Useful for prying things open. Advantage on Str checks where applicable.", False),
    ("Hammer", 1, 3.0, "For driving pitons or general construction.", False),
    ("Pitons", 10, 0.25, "Iron spikes for climbing or anchoring ropes.", False),
    ("Torches", 10, 1.0, "Burns for 1 hour; bright light 20 ft, dim light 20 ft beyond.", False),
    ("Tinderbox", 1, 1.0, "For lighting fires (torches, campfires, etc.).", False),
    ("Rations (days)", 10, 2.0, "Trail rations, 1 day's food each.", False),
    ("Waterskin", 1, 5.0, "Holds 4 pints of liquid. Full.", False),
    ("Hempen Rope (50 ft)", 1, 10.0, "Can hold up to 3 knots.", False),

    # Other
    ("Iron Pot", 1, 10.0, "For cooking.", False),
    ("Common Clothes", 1, 3.0, "A set of plain common clothes.", False),
    ("Belt Pouch", 1, 0.5, "Contains 10 gp.", False),
    ("Seed from the Harvest House (Daggerford)", 1, 0.0,
     "Trinket. A single seed from the Harvest House in Daggerford. "
     "Significance unknown but felt important to keep.", False),
]

for name, qty, weight, desc, equipped in items:
    db.execute(
        """INSERT INTO inventory
           (character_id, name, quantity, weight, description, equipped)
           VALUES (?,?,?,?,?,?)""",
        (cid, name, qty, weight, desc, equipped),
    )

db.commit()
db.close()
print(f"Tomato seeded successfully (character id={cid}).")
