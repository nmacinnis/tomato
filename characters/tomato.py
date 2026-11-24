"""Character sheet for ••TOMATO• — Reborn Warforged Battlemaster Fighter 10."""

CHARACTER = {
    "name": "••TOMATO•",
    "race": "Reborn Warforged",
    "class": "Battlemaster Fighter",
    "level": 10,
    "hp": 100,
    "max_hp": 100,
    "ac": 19,  # splint + defense + cloak (shield bumps to 21 in combat)
    "speed": 30,
    "str": 20,
    "dex": 12,
    "con": 16,
    "int": 8,
    "wis": 13,
    "cha": 10,
    "flat_ac_bonus": 0,
    "save_proficiencies": "str,con",
    "skill_proficiencies": "athletics,perception,animal_handling,survival,insight,stealth",
    "alignment": "Chaotic Good",
    "size": "Medium",
    "height": "6'6\"",
    "weight": "302 lbs",
    "hit_die": "d10",
    # Play state at creation
    "notes": (
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
    "hit_dice_remaining": 10,
    "coins_gp": 10,
}

ABILITIES = [
    # Racial — Reborn Warforged
    {
        "name": "Deathless Nature",
        "type": "passive",
        "description": (
            "Advantage on saves vs disease and poison; resistance to poison damage. "
            "Advantage on death saving throws. No need to eat, drink, or breathe. "
            "No sleep needed; long rest in 4 hrs while inactive (retains consciousness). "
            "Magic cannot put you to sleep."
        ),
    },
    {
        "name": "Knowledge from a Past Life",
        "type": "free_action",
        "uses_max": 4,
        "recharge": "long",
        "die_type": "d6",
        "description": (
            "When you make an ability check using a skill, roll a d6 immediately after seeing "
            "the d20 result and add it to the check. "
            "Regains all uses on long rest."
        ),
    },
    # Fighter core
    {
        "name": "Action Surge",
        "type": "free_action",
        "uses_max": 1,
        "recharge": "short",
        "description": "Take one additional action on your turn (not the Magic action). Once per Short or Long Rest.",
    },
    {
        "name": "Second Wind",
        "type": "bonus_action",
        "uses_max": 3,
        "recharge": "short",
        "die_type": "d10",
        "description": (
            "Bonus action: regain 1d10 + 9 (fighter level) HP. "
            "Also usable via Tactical Mind: expend a use to add 1d10 to a failed ability check "
            "(if the check still fails, the use is not expended). "
            "Tactical Shift: when activated as a bonus action, may move up to 15 ft without "
            "provoking Opportunity Attacks."
        ),
    },
    {
        "name": "Know Your Enemy",
        "type": "bonus_action",
        "uses_max": 1,
        "recharge": "long",
        "description": (
            "Bonus Action: learn whether a visible creature within 30 ft has any Immunities, "
            "Resistances, or Vulnerabilities, and what they are. "
            "1 use per Long Rest; can restore by expending one Superiority Die (no action)."
        ),
    },
    {
        "name": "Indomitable",
        "type": "free_action",
        "uses_max": 1,
        "recharge": "long",
        "description": (
            "When you fail a saving throw, reroll it with a bonus equal to your Fighter level (+9). "
            "You must use the new roll. Once per Long Rest."
        ),
    },
    {
        "name": "Extra Attack",
        "type": "passive",
        "description": "Attack twice whenever you take the Attack action on your turn.",
    },
    {
        "name": "Fighting Style: Defense",
        "type": "passive",
        "description": "+1 AC while wearing armor. (Contributes to current AC of 19; 21 with shield.)",
        "ac_bonus": 1,
    },
    {
        "name": "Tactical Mind",
        "type": "free_action",
        "die_type": "d10",
        "description": (
            "When you fail an ability check, expend one Second Wind use to add 1d10 to the roll "
            "(after seeing the d20 result). If the check still fails, the use is not expended."
        ),
    },
    {
        "name": "Tactical Shift",
        "type": "passive",
        "description": (
            "When you activate Second Wind as a Bonus Action, you may move up to half your Speed "
            "(15 ft) without provoking Opportunity Attacks."
        ),
    },
    {
        "name": "Tactical Master",
        "type": "passive",
        "description": (
            "When attacking with a weapon whose Mastery property you can use, you may replace "
            "that property with Push, Sap, or Slow for that attack."
        ),
    },
    # Battlemaster Maneuvers — shared pool of 5d10 superiority dice
    {
        "name": "Superiority Dice Pool (d10)",
        "type": "free_action",
        "uses_max": 5,
        "recharge": "short",
        "die_type": "d10",
        "description": (
            "Pool of 5 superiority dice (d10) shared across all maneuvers. Regain all on Short or Long "
            "Rest. Maneuver save DC: 17 (8 + STR mod +4 prof + 1)."
        ),
    },
    {
        "name": "Maneuver: Goading Attack",
        "type": "action",
        "description": (
            "Expend 1 Superiority Die. On a hit, add the die to damage and the target must make "
            "a Wis save (DC 17) or have Disadvantage on attacks against targets other than you "
            "until the end of its next turn."
        ),
    },
    {
        "name": "Maneuver: Rally",
        "type": "bonus_action",
        "description": (
            "Bonus Action: expend 1 Superiority Die. An ally you can see gains temp HP equal to "
            "the die result + 4 (half fighter level, rounded down)."
        ),
    },
    {
        "name": "Maneuver: Riposte",
        "type": "reaction",
        "description": (
            "Reaction: when a creature misses you with a melee attack, expend 1 Superiority Die "
            "to make one melee weapon attack against the creature. On a hit, add the die to damage."
        ),
    },
    {
        "name": "Maneuver: Precision Attack",
        "type": "action",
        "description": (
            "Expend 1 Superiority Die immediately after seeing the d20 roll for an attack. "
            "Add the die result to the attack roll. Can be used before or after knowing if it hits."
        ),
    },
    {
        "name": "Maneuver: Parry",
        "type": "reaction",
        "description": (
            "Reaction: when you take damage from a melee attack, expend 1 Superiority Die to reduce the "
            "damage by the die result + STR modifier (+5). Total reduction: d10+5."
        ),
    },
    {
        "name": "Maneuver: Lunging Attack",
        "type": "bonus_action",
        "description": (
            "As a Bonus Action, you can expend one Superiority Die and take the Dash action. "
            "If you move at least 5 feet in a straight line immediately before hitting with a melee attack "
            "as part of the Attack action on this turn, you can add the Superiority Die to the attack's damage roll."
        ),
    },
    {
        "name": "Maneuver: Commander's Strike",
        "type": "action",
        "description": (
            "When you take the Attack action, forgo one attack and use a Bonus Action to direct an ally. "
            "Expend 1 Superiority Die — the chosen ally can immediately use their Reaction to make one weapon attack, "
            "adding the superiority die to the damage roll."
        ),
    },
    # Feats
    {
        "name": "Feat — Mage Slayer: Guarded Mind",
        "type": "free_action",
        "uses_max": 1,
        "recharge": "short",
        "description": (
            "If you fail an Intelligence, Wisdom, or Charisma saving throw, you can cause yourself "
            "to succeed instead. Once per Short or Long Rest. "
            "Flavor: Tomato's half-organic, half-mechanical brain — if one half is charmed, "
            "the other half can break the spell."
        ),
    },
    {
        "name": "Feat — Mage Slayer: Concentration Breaker",
        "type": "passive",
        "description": (
            "When you damage a creature that is Concentrating, it has Disadvantage on its "
            "Constitution saving throw to maintain concentration."
        ),
    },
    {
        "name": "Feat — Sentinel: Guardian",
        "type": "reaction",
        "description": (
            "You can make an Opportunity Attack when a creature within 5 ft of you takes the "
            "Disengage action OR hits a target other than you with an attack."
        ),
    },
    {
        "name": "Feat — Sentinel: Halt",
        "type": "passive",
        "description": (
            "When you hit a creature with an Opportunity Attack, that creature's Speed becomes 0 "
            "for the rest of the current turn."
        ),
    },
    # Magic Initiate (Druid) — innate dryad magic
    {
        "name": "Cantrip: Druidcraft",
        "type": "action",
        "description": (
            "Create minor nature effects: predict weather, make a flower bloom, light a campfire, "
            "create a sensory effect. Unlimited uses."
        ),
    },
    {
        "name": "Cantrip: Guidance",
        "type": "action",
        "description": (
            "Touch a willing creature. Once before the spell ends (concentration, up to 1 minute) "
            "the creature can roll a d4 and add it to one ability check. Unlimited uses."
        ),
    },
    {
        "name": "Spell: Goodberry",
        "type": "action",
        "uses_max": 1,
        "recharge": "long",
        "description": (
            "Up to 10 magical berries appear. A berry restores 1 HP and provides nourishment for "
            "a day. Berries last 24 hours. Once per Long Rest (Magic Initiate)."
        ),
    },
    # Background
    {
        "name": "Rustic Hospitality",
        "type": "passive",
        "description": (
            "Among common folk you fit in with ease. You can find a place to hide, rest, or "
            "recuperate with commoners, who will shield you from law or pursuers — "
            "though they will not risk their lives for you."
        ),
    },
    # Weapon Mastery
    {
        "name": "Weapon Mastery: Spear (Sap)",
        "type": "passive",
        "description": (
            "On a hit with a Spear, the target has Disadvantage on its next attack roll before "
            "the start of your next turn."
        ),
    },
    {
        "name": "Weapon Mastery: Hand Axe (Vex)",
        "type": "passive",
        "description": (
            "On a hit with a Hand Axe, you gain Advantage on your next attack roll against "
            "that creature before the end of your next turn."
        ),
    },
    {
        "name": "Weapon Mastery: Javelin (Slow)",
        "type": "passive",
        "description": (
            "On a hit with a Javelin, the target's Speed is reduced by 10 ft until the start of your next turn."
        ),
    },
    {
        "name": "Weapon Mastery: Halberd (Cleave)",
        "type": "passive",
        "description": (
            "On a hit with a Halberd, you may make an additional attack against a second creature "
            "within reach that is within 5 ft of the original target. No attack roll bonus applies."
        ),
    },
    {
        "name": "Weapon Mastery: Longsword (Sap)",
        "type": "passive",
        "description": (
            "When you hit a creature with a Longsword, you can apply the Sap mastery effect: "
            "the target has Disadvantage on its next attack roll before the start of your next turn."
        ),
    },
]

ITEMS = [
    # Armor & shield
    {
        "name": "Splint Armor",
        "quantity": 1,
        "weight": 60.0,
        "description": "AC 17. Heavy armor; Disadvantage on Stealth checks.",
        "equipped": 1,
        "ac_bonus": 17,
        "sets_base_ac": 1,
    },
    {
        "name": "Shield",
        "quantity": 1,
        "weight": 6.0,
        "description": "+2 AC when equipped. Bumps total AC to 21.",
        "equipped": 0,
        "ac_bonus": 2,
    },
    {
        "name": "Cloak of Protection",
        "quantity": 1,
        "weight": 1.0,
        "description": "+1 AC (already included in base AC 19) and +1 to all saving throws.",
        "equipped": 1,
        "ac_bonus": 1,
        "save_bonus": 1,
    },
    # Weapons
    {
        "name": "Spear",
        "quantity": 1,
        "weight": 3.0,
        "description": "1d6 piercing (1d8 versatile). Thrown (20/60). Mastery: Sap. Starting equipment.",
        "equipped": 1,
        "is_weapon": 1,
        "is_melee": 1,
        "damage_dice": "1d6",
        "damage_type": "piercing",
        "magic_bonus": 0,
        "damage_notes": "Versatile (1d8), Thrown 20/60, Sap",
    },
    {
        "name": "Hand Axe",
        "quantity": 1,
        "weight": 2.0,
        "description": "1d6 slashing. Light, Thrown (20/60). Mastery: Vex. Starting equipment.",
        "equipped": 0,
        "is_weapon": 1,
        "is_melee": 1,
        "damage_dice": "1d6",
        "damage_type": "slashing",
        "magic_bonus": 0,
        "damage_notes": "Light, Thrown 20/60, Vex",
    },
    {
        "name": "Hand Axe (Shovel \u2014 sharpened WW1-style)",
        "quantity": 1,
        "weight": 5.0,
        "description": (
            "1d6 slashing. Light, Thrown (20/60). Mastery: Vex. "
            "Actually Tomato's shovel from her Folk Hero days, sharpened for combat."
        ),
        "equipped": 0,
        "is_weapon": 1,
        "is_melee": 1,
        "damage_dice": "1d6",
        "damage_type": "slashing",
        "magic_bonus": 0,
        "damage_notes": "Light, Thrown 20/60, Vex",
    },
    {
        "name": "Javelin",
        "quantity": 1,
        "weight": 2.0,
        "description": "1d6 piercing. Thrown (30/120). Mastery: Slow. Starting equipment.",
        "equipped": 0,
        "is_weapon": 1,
        "is_melee": 1,
        "damage_dice": "1d6",
        "damage_type": "piercing",
        "magic_bonus": 0,
        "damage_notes": "Thrown 30/120, Slow (STR-based)",
    },
    {
        "name": "Halberd",
        "quantity": 1,
        "weight": 6.0,
        "description": "2-handed. 1d10 slashing. Reach. Heavy. Mastery: Cleave. Picked up during adventuring.",
        "equipped": 1,
        "is_weapon": 1,
        "is_melee": 1,
        "damage_dice": "1d10",
        "damage_type": "slashing",
        "magic_bonus": 0,
        "damage_notes": "Reach, Heavy, Cleave",
    },
    {
        "name": "Yester Hill Axe",
        "quantity": 1,
        "weight": 4.0,
        "description": (
            "+1 Battleaxe. 1d8+1 slashing (1d10+1 versatile). +1d8 damage against animals, plants, and monstrosities."
        ),
        "equipped": 1,
        "is_weapon": 1,
        "is_melee": 1,
        "damage_dice": "1d8",
        "damage_type": "slashing",
        "magic_bonus": 1,
        "damage_notes": "Versatile (1d10), +1d8 vs animals/plants/monstrosities",
    },
    # Tools & gear
    {
        "name": "Carpenter's Tools",
        "quantity": 1,
        "weight": 6.0,
        "description": "Proficiency from Student of War. Used for construction and repair.",
        "equipped": 0,
        "tool_proficient": 1,
    },
    {
        "name": "Tinker's Tools",
        "quantity": 1,
        "weight": 10.0,
        "description": "Proficiency from Folk Hero background. Used for mechanical tinkering.",
        "equipped": 0,
        "tool_proficient": 1,
    },
    {
        "name": "Herbalism Kit",
        "quantity": 1,
        "weight": 3.0,
        "description": "Proficiency from Ancestral Legacy (Reborn). Used to identify and apply herbs.",
        "equipped": 0,
        "tool_proficient": 1,
    },
    # Dungeoneer's Pack contents
    {
        "name": "Backpack",
        "quantity": 1,
        "weight": 5.0,
        "description": "Container for gear.",
        "equipped": 0,
    },
    {
        "name": "Crowbar",
        "quantity": 1,
        "weight": 5.0,
        "description": "Useful for prying things open. Advantage on Str checks where applicable.",
        "equipped": 0,
    },
    {
        "name": "Hammer",
        "quantity": 1,
        "weight": 3.0,
        "description": "For driving pitons or general construction.",
        "equipped": 0,
    },
    {
        "name": "Pitons",
        "quantity": 10,
        "weight": 0.25,
        "description": "Iron spikes for climbing or anchoring ropes.",
        "equipped": 0,
    },
    {
        "name": "Torches",
        "quantity": 10,
        "weight": 1.0,
        "description": "Burns for 1 hour; bright light 20 ft, dim light 20 ft beyond.",
        "equipped": 0,
    },
    {
        "name": "Tinderbox",
        "quantity": 1,
        "weight": 1.0,
        "description": "For lighting fires (torches, campfires, etc.).",
        "equipped": 0,
    },
    {
        "name": "Rations (days)",
        "quantity": 10,
        "weight": 2.0,
        "description": "Trail rations, 1 day's food each.",
        "equipped": 0,
    },
    {
        "name": "Waterskin",
        "quantity": 1,
        "weight": 5.0,
        "description": "Holds 4 pints of liquid. Full.",
        "equipped": 0,
    },
    {
        "name": "Hempen Rope (50 ft)",
        "quantity": 1,
        "weight": 10.0,
        "description": "Can hold up to 3 knots.",
        "equipped": 0,
    },
    # Other
    {
        "name": "Iron Pot",
        "quantity": 1,
        "weight": 10.0,
        "description": "For cooking.",
        "equipped": 0,
    },
    {
        "name": "Common Clothes",
        "quantity": 1,
        "weight": 3.0,
        "description": "A set of plain common clothes.",
        "equipped": 0,
    },
    {
        "name": "Belt Pouch",
        "quantity": 1,
        "weight": 0.5,
        "description": "Contains 10 gp.",
        "equipped": 0,
    },
    {
        "name": "Seed from the Harvest House (Daggerford)",
        "quantity": 1,
        "weight": 0.0,
        "description": (
            "Trinket. A single seed from the Harvest House in Daggerford. Significance unknown but felt "
            "important to keep."
        ),
        "equipped": 0,
    },
]


# ── Seed steps ────────────────────────────────────────────────────────────────
# One-time changes to an existing TOMATO. Sheet fields are refreshed from the
# Sheet right after the steps run, so steps only adjust Play state and
# rename/remove rows.


def _superiority_dice_d10(conn, cid):
    # The pool grew from 4 × d8 to 5 × d10; rename the old row so it keeps its id
    conn.execute(
        """UPDATE abilities SET name='Superiority Dice Pool (d10)', uses_remaining=5
           WHERE character_id=? AND name='Superiority Dice Pool (d8)'""",
        (cid,),
    )


def _level_10(conn, cid):
    conn.execute("UPDATE characters SET hp=100 WHERE id=? AND level<10", (cid,))


STEPS = [
    ("superiority-dice-d10", _superiority_dice_d10),
    ("level-10", _level_10),
]
