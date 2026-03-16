"""Character sheet for ••TOMATO• — Reborn Warforged Battlemaster Fighter 9."""

_NAME = "••TOMATO•"

_CHAR = (
    _NAME,
    "Reborn Warforged",
    "Battlemaster Fighter",
    9,
    87,
    87,
    19,  # splint + defense + cloak (shield bumps to 21 in combat)
    30,
    20,
    12,
    16,
    8,
    13,
    10,
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
)

# name, type, uses_max, recharge, die_type, description
_ABILITIES = [
    # Racial — Reborn Warforged
    (
        "Deathless Nature",
        "passive",
        None,
        None,
        None,
        "Advantage on saves vs disease and poison; resistance to poison damage. "
        "Advantage on death saving throws. No need to eat, drink, or breathe. "
        "No sleep needed; long rest in 4 hrs while inactive (retains consciousness). "
        "Magic cannot put you to sleep.",
    ),
    (
        "Knowledge from a Past Life",
        "free_action",
        4,
        "long",
        "d6",
        "When you make an ability check using a skill, roll a d6 immediately after seeing "
        "the d20 result and add it to the check. "
        "Regains all uses on long rest.",
    ),
    # Fighter core
    (
        "Action Surge",
        "free_action",
        1,
        "short",
        None,
        "Take one additional action on your turn (not the Magic action). Once per Short or Long Rest.",
    ),
    (
        "Second Wind",
        "bonus_action",
        3,
        "short",
        "d10",
        "Bonus action: regain 1d10 + 9 (fighter level) HP. "
        "Also usable via Tactical Mind: expend a use to add 1d10 to a failed ability check "
        "(if the check still fails, the use is not expended). "
        "Tactical Shift: when activated as a bonus action, may move up to 15 ft without "
        "provoking Opportunity Attacks.",
    ),
    (
        "Know Your Enemy",
        "bonus_action",
        1,
        "long",
        None,
        "Bonus Action: learn whether a visible creature within 30 ft has any Immunities, "
        "Resistances, or Vulnerabilities, and what they are. "
        "1 use per Long Rest; can restore by expending one Superiority Die (no action).",
    ),
    (
        "Indomitable",
        "free_action",
        1,
        "long",
        None,
        "When you fail a saving throw, reroll it with a bonus equal to your Fighter level (+9). "
        "You must use the new roll. Once per Long Rest.",
    ),
    ("Extra Attack", "passive", None, None, None, "Attack twice whenever you take the Attack action on your turn."),
    (
        "Fighting Style: Defense",
        "passive",
        None,
        None,
        None,
        "+1 AC while wearing armor. (Contributes to current AC of 19; 21 with shield.)",
    ),
    (
        "Tactical Mind",
        "free_action",
        None,
        None,
        "d10",
        "When you fail an ability check, expend one Second Wind use to add 1d10 to the roll "
        "(after seeing the d20 result). If the check still fails, the use is not expended.",
    ),
    (
        "Tactical Shift",
        "passive",
        None,
        None,
        None,
        "When you activate Second Wind as a Bonus Action, you may move up to half your Speed "
        "(15 ft) without provoking Opportunity Attacks.",
    ),
    (
        "Tactical Master",
        "passive",
        None,
        None,
        None,
        "When attacking with a weapon whose Mastery property you can use, you may replace "
        "that property with Push, Sap, or Slow for that attack.",
    ),
    # Battlemaster Maneuvers — shared pool of 4d8 superiority dice
    (
        "Superiority Dice Pool (d8)",
        "free_action",
        4,
        "short",
        "d8",
        "Pool of 4 superiority dice (d8) shared across all maneuvers. "
        "Regain all on Short or Long Rest. "
        "Maneuver save DC: 17 (8 + STR mod +4 prof + 1).",
    ),
    (
        "Maneuver: Goading Attack",
        "action",
        None,
        None,
        None,
        "Expend 1 Superiority Die. On a hit, add the die to damage and the target must make "
        "a Wis save (DC 17) or have Disadvantage on attacks against targets other than you "
        "until the end of its next turn.",
    ),
    (
        "Maneuver: Rally",
        "bonus_action",
        None,
        None,
        None,
        "Bonus Action: expend 1 Superiority Die. An ally you can see gains temp HP equal to "
        "the die result + 4 (half fighter level, rounded down).",
    ),
    (
        "Maneuver: Riposte",
        "reaction",
        None,
        None,
        None,
        "Reaction: when a creature misses you with a melee attack, expend 1 Superiority Die "
        "to make one melee weapon attack against the creature. On a hit, add the die to damage.",
    ),
    (
        "Maneuver: Precision Attack",
        "action",
        None,
        None,
        None,
        "Expend 1 Superiority Die immediately after seeing the d20 roll for an attack. "
        "Add the die result to the attack roll. Can be used before or after knowing if it hits.",
    ),
    (
        "Maneuver: Parry",
        "reaction",
        None,
        None,
        None,
        "Reaction: when you take damage from a melee attack, expend 1 Superiority Die "
        "to reduce the damage by the die result + STR modifier (+5). Total reduction: d8+5.",
    ),
    # Feats
    (
        "Feat — Mage Slayer: Guarded Mind",
        "free_action",
        1,
        "short",
        None,
        "If you fail an Intelligence, Wisdom, or Charisma saving throw, you can cause yourself "
        "to succeed instead. Once per Short or Long Rest. "
        "Flavor: Tomato's half-organic, half-mechanical brain — if one half is charmed, "
        "the other half can break the spell.",
    ),
    (
        "Feat — Mage Slayer: Concentration Breaker",
        "passive",
        None,
        None,
        None,
        "When you damage a creature that is Concentrating, it has Disadvantage on its "
        "Constitution saving throw to maintain concentration.",
    ),
    (
        "Feat — Sentinel: Guardian",
        "reaction",
        None,
        None,
        None,
        "You can make an Opportunity Attack when a creature within 5 ft of you takes the "
        "Disengage action OR hits a target other than you with an attack.",
    ),
    (
        "Feat — Sentinel: Halt",
        "passive",
        None,
        None,
        None,
        "When you hit a creature with an Opportunity Attack, that creature's Speed becomes 0 "
        "for the rest of the current turn.",
    ),
    # Magic Initiate (Druid) — innate dryad magic
    (
        "Cantrip: Druidcraft",
        "action",
        None,
        None,
        None,
        "Create minor nature effects: predict weather, make a flower bloom, light a campfire, "
        "create a sensory effect. Unlimited uses.",
    ),
    (
        "Cantrip: Guidance",
        "action",
        None,
        None,
        None,
        "Touch a willing creature. Once before the spell ends (concentration, up to 1 minute) "
        "the creature can roll a d4 and add it to one ability check. Unlimited uses.",
    ),
    (
        "Spell: Goodberry",
        "action",
        1,
        "long",
        None,
        "Up to 10 magical berries appear. A berry restores 1 HP and provides nourishment for "
        "a day. Berries last 24 hours. Once per Long Rest (Magic Initiate).",
    ),
    # Background
    (
        "Rustic Hospitality",
        "passive",
        None,
        None,
        None,
        "Among common folk you fit in with ease. You can find a place to hide, rest, or "
        "recuperate with commoners, who will shield you from law or pursuers — "
        "though they will not risk their lives for you.",
    ),
    # Weapon Mastery
    (
        "Weapon Mastery: Spear (Sap)",
        "passive",
        None,
        None,
        None,
        "On a hit with a Spear, the target has Disadvantage on its next attack roll before "
        "the start of your next turn.",
    ),
    (
        "Weapon Mastery: Hand Axe (Vex)",
        "passive",
        None,
        None,
        None,
        "On a hit with a Hand Axe, you gain Advantage on your next attack roll against "
        "that creature before the end of your next turn.",
    ),
    (
        "Weapon Mastery: Javelin (Slow)",
        "passive",
        None,
        None,
        None,
        "On a hit with a Javelin, the target's Speed is reduced by 10 ft until the start of your next turn.",
    ),
    (
        "Weapon Mastery: Halberd (Cleave)",
        "passive",
        None,
        None,
        None,
        "On a hit with a Halberd, you may make an additional attack against a second creature "
        "within reach that is within 5 ft of the original target. No attack roll bonus applies.",
    ),
]

# name, qty, weight, description, equipped
_ITEMS = [
    # Armor & shield
    ("Splint Armor", 1, 60.0, "AC 17. Heavy armor; Disadvantage on Stealth checks.", True),
    ("Shield", 1, 6.0, "+2 AC when equipped. Bumps total AC to 21.", False),
    ("Cloak of Protection", 1, 1.0, "+1 AC (already included in base AC 19) and +1 to all saving throws.", True),
    # Weapons
    ("Spear", 1, 3.0, "1d6 piercing (1d8 versatile). Thrown (20/60). Mastery: Sap. Starting equipment.", True),
    ("Hand Axe", 1, 2.0, "1d6 slashing. Light, Thrown (20/60). Mastery: Vex. Starting equipment.", False),
    (
        "Hand Axe (Shovel \u2014 sharpened WW1-style)",
        1,
        5.0,
        "1d6 slashing. Light, Thrown (20/60). Mastery: Vex. "
        "Actually Tomato's shovel from her Folk Hero days, sharpened for combat.",
        False,
    ),
    ("Javelin", 1, 2.0, "1d6 piercing. Thrown (30/120). Mastery: Slow. Starting equipment.", False),
    ("Halberd", 1, 6.0, "2-handed. 1d10 slashing. Reach. Heavy. Mastery: Cleave. Picked up during adventuring.", True),
    (
        "Yester Hill Axe",
        1,
        4.0,
        "+1 Battleaxe. 1d8+1 slashing (1d10+1 versatile). +1d8 damage against animals, plants, and monstrosities.",
        True,
    ),
    # Tools & gear
    ("Carpenter's Tools", 1, 6.0, "Proficiency from Student of War. Used for construction and repair.", False),
    ("Tinker's Tools", 1, 10.0, "Proficiency from Folk Hero background. Used for mechanical tinkering.", False),
    ("Herbalism Kit", 1, 3.0, "Proficiency from Ancestral Legacy (Reborn). Used to identify and apply herbs.", False),
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
    (
        "Seed from the Harvest House (Daggerford)",
        1,
        0.0,
        "Trinket. A single seed from the Harvest House in Daggerford. Significance unknown but felt important to keep.",
        False,
    ),
]


def apply(conn):
    # Insert character if not already present
    conn.execute(
        """INSERT INTO characters
               (name, race, class, level, hp, max_hp, ac, speed,
                str, dex, con, int, wis, cha, notes)
           SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
           WHERE NOT EXISTS (SELECT 1 FROM characters WHERE name=?)""",
        _CHAR + (_NAME,),
    )

    cid = conn.execute("SELECT id FROM characters WHERE name=?", (_NAME,)).fetchone()[0]

    for name, atype, uses, recharge, die_type, desc in _ABILITIES:
        conn.execute(
            """INSERT INTO abilities
                   (character_id, name, type, description, uses_max, uses_remaining, recharge, die_type)
               SELECT ?,?,?,?,?,?,?,?
               WHERE NOT EXISTS (
                   SELECT 1 FROM abilities WHERE character_id=? AND name=?
               )""",
            (cid, name, atype, desc, uses, uses, recharge, die_type, cid, name),
        )

    for name, qty, weight, desc, equipped in _ITEMS:
        conn.execute(
            """INSERT INTO inventory
                   (character_id, name, quantity, weight, description, equipped)
               SELECT ?,?,?,?,?,?
               WHERE NOT EXISTS (
                   SELECT 1 FROM inventory WHERE character_id=? AND name=?
               )""",
            (cid, name, qty, weight, desc, equipped, cid, name),
        )

    # Idempotent updates — keep data current across schema/data changes
    conn.execute(
        "UPDATE characters SET skill_proficiencies=? WHERE id=?",
        ("athletics,perception,animal_handling,survival,insight,stealth", cid),
    )
    conn.execute(
        "UPDATE characters SET save_proficiencies='str,con', flat_ac_bonus=0,"
        " alignment='Chaotic Good', size='Medium', height='6''6\"', weight='302 lbs'"
        " WHERE id=?",
        (cid,),
    )

    conn.execute(
        "UPDATE abilities SET ac_bonus=1 WHERE character_id=? AND name='Fighting Style: Defense'",
        (cid,),
    )
    conn.execute(
        "UPDATE abilities SET type=?, recharge=?, die_type=? WHERE character_id=? AND name=?",
        ("free_action", None, "d10", cid, "Tactical Mind"),
    )

    # Inventory: AC and save bonuses
    conn.execute(
        "UPDATE inventory SET ac_bonus=17, sets_base_ac=1 WHERE character_id=? AND name='Splint Armor'",
        (cid,),
    )
    conn.execute(
        "UPDATE inventory SET ac_bonus=2 WHERE character_id=? AND name='Shield'",
        (cid,),
    )
    conn.execute(
        "UPDATE inventory SET ac_bonus=1, save_bonus=1 WHERE character_id=? AND name='Cloak of Protection'",
        (cid,),
    )

    # Tool proficiencies
    for tool in ("Carpenter's Tools", "Tinker's Tools", "Herbalism Kit"):
        conn.execute(
            "UPDATE inventory SET tool_proficient=1 WHERE character_id=? AND name=?",
            (cid, tool),
        )

    # Weapon stats
    weapons = [
        ("Spear", "1d6", "piercing", 0, 1, "Versatile (1d8), Thrown 20/60, Sap"),
        ("Hand Axe", "1d6", "slashing", 0, 1, "Light, Thrown 20/60, Vex"),
        ("Hand Axe (Shovel \u2014 sharpened WW1-style)", "1d6", "slashing", 0, 1, "Light, Thrown 20/60, Vex"),
        ("Javelin", "1d6", "piercing", 0, 1, "Thrown 30/120, Slow (STR-based)"),
        ("Halberd", "1d10", "slashing", 0, 1, "Reach, Heavy, Cleave"),
        ("Yester Hill Axe", "1d8", "slashing", 1, 1, "Versatile (1d10), +1d8 vs animals/plants/monstrosities"),
    ]
    for name, dd, dt, mb, im, notes in weapons:
        conn.execute(
            """UPDATE inventory
               SET damage_dice=?, damage_type=?, magic_bonus=?,
                   is_melee=?, damage_notes=?, is_weapon=1
               WHERE character_id=? AND name=?""",
            (dd, dt, mb, im, notes, cid, name),
        )
