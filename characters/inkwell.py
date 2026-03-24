"""Character sheet for Inkwell — Changeling Aberrant Sorcerer 3."""

_NAME = "Inkwell"

_CHAR = (
    _NAME,
    "Changeling (Fey)",
    "Aberrant Sorcerer",
    3,
    19,  # hp (rolled: 3+4+6 = 13 + CON mod 2×3 = 6 → 19)
    19,  # max_hp
    11,  # ac (10 + DEX mod 1; Mage Armor → 14)
    30,
    9,  # str
    12,  # dex
    14,  # con
    13,  # int
    16,  # wis
    19,  # cha (17 base + 2 Changeling)
    (
        "Spell save DC: 14  |  Spell attack bonus: +6  |  Prof. bonus: +2\n"
        "Alignment: Chaotic Neutral  |  Size: Medium (5'4\", 130 lbs)  |  Creature Type: Fey\n\n"
        "Background: Audit Analyst (Scribe). Bookkeeper turned adventurer; perpetually ink-stained fingers.\n"
        "Estranged from her family — the Lord and Lady of Port Ellsmyre, a minor fishing village in the Riverlands.\n\n"
        "Languages: Common, Common Sign, Elvish\n"
        "Sorcery Points: 3/long rest  |  Innate Sorcery: 2/long rest\n"
        "Metamagic: Extended Spell (1 SP), Subtle Spell (1 SP)\n"
        "Feat — Skilled: Insight, Stealth, Disguise Kit"
    ),
)

# (name, type, uses_max, recharge, die_type, description, components, spell_range, duration, concentration)
_ABILITIES = [
    # ── Changeling (Fey) ─────────────────────────────────────────────────────
    (
        "Shape-Shifter",
        "action",
        None,
        None,
        None,
        "Change appearance and voice (coloration, hair, sex, height, weight, size Medium↔Small). "
        "Can appear as another playable species — stats unchanged. Cannot duplicate someone unseen; "
        "must keep same limb arrangement. Clothing/equipment don't change. "
        "While shape-shifted: Advantage on Charisma checks. Revert by taking an action.",
        "",
        "",
        "",
        0,
    ),
    (
        "Changeling Instincts",
        "passive",
        None,
        None,
        None,
        "Fey heritage grants proficiency in Intimidation and Performance.",
        "",
        "",
        "",
        0,
    ),
    # ── Sorcerer Core ────────────────────────────────────────────────────────
    (
        "Innate Sorcery",
        "bonus_action",
        2,
        "long",
        None,
        "Bonus Action: unleash innate magic for 1 minute. While active: "
        "Sorcerer spell save DC +1 (to 15), and Advantage on Sorcerer spell attack rolls. "
        "2 uses per Long Rest.",
        "",
        "",
        "1 minute",
        0,
    ),
    (
        "Sorcery Points",
        "free_action",
        3,
        "long",
        None,
        "Pool of 3 sorcery points. Regain all on Long Rest. Uses:\n"
        "• Metamagic (Extended Spell: 1 SP, Subtle Spell: 1 SP)\n"
        "• Convert slot → SP: spend a slot, gain SP equal to its level (no action).\n"
        "• Create slot (Bonus Action): 1st=2 SP, 2nd=3 SP.",
        "",
        "",
        "",
        0,
    ),
    (
        "Metamagic: Extended Spell",
        "passive",
        None,
        None,
        None,
        "Cost: 1 Sorcery Point. When casting a spell with duration 1 min+, double it (max 24 hrs). "
        "If Concentration, gain Advantage on saves to maintain it.",
        "",
        "",
        "",
        0,
    ),
    (
        "Metamagic: Subtle Spell",
        "passive",
        None,
        None,
        None,
        "Cost: 1 Sorcery Point. Cast a spell without Verbal, Somatic, or (non-consumed/non-costed) "
        "Material components. Ideal for disguised or social spellcasting.",
        "",
        "",
        "",
        0,
    ),
    # ── Aberrant Sorcery (Subclass) ──────────────────────────────────────────
    (
        "Telepathic Speech",
        "bonus_action",
        None,
        None,
        None,
        "Choose a visible creature within 30 ft. You and it communicate telepathically while within "
        "CHA modifier miles of each other (min 1 mile). Both must share a known language. "
        "Lasts 3 minutes (Sorcerer level). Ends early if used on a different creature.",
        "",
        "",
        "3 minutes",
        0,
    ),
    (
        "Psionic Spells (Always Prepared)",
        "passive",
        None,
        None,
        None,
        "These spells are always prepared and don't count against the prepared spell limit: "
        "Arms of Hadar, Calm Emotions, Detect Thoughts, Dissonant Whispers, Mind Sliver.",
        "",
        "",
        "",
        0,
    ),
    # ── Spell Slot Trackers ──────────────────────────────────────────────────
    (
        "Spell Slots — 1st Level",
        "free_action",
        4,
        "long",
        None,
        "4 first-level spell slots. Regain all on Long Rest. "
        "Can convert to Sorcery Points (1 SP per slot level, no action).",
        "",
        "",
        "",
        0,
    ),
    (
        "Spell Slots — 2nd Level",
        "free_action",
        2,
        "long",
        None,
        "2 second-level spell slots. Regain all on Long Rest. "
        "Can convert to Sorcery Points (2 SP per slot, no action).",
        "",
        "",
        "",
        0,
    ),
    # ── Cantrips ─────────────────────────────────────────────────────────────
    (
        "Cantrip: Mage Hand",
        "action",
        None,
        None,
        None,
        "A spectral hand appears at a point within range. Use it to manipulate an object, open an "
        "unlocked door or container, stow or retrieve an item from an open container, or pour out a vial. "
        "The hand can move up to 30 ft each time you use it. It can't attack, activate magic items, "
        "or carry more than 10 lbs. Vanishes if ever more than 30 ft from you.",
        "V, S",
        "30 ft",
        "1 minute",
        1,
    ),
    (
        "Cantrip: Prestidigitation",
        "action",
        None,
        None,
        None,
        "Create a minor magical effect: a harmless sensory effect; light or snuff a nonmagical flame; "
        "clean or soil, chill, warm, or flavor a 1-cubic-foot object; make a color, mark, or symbol appear "
        "on an object for 1 hour; produce a small trinket or image that fits in your hand (lasts until "
        "end of next turn). Up to three effects active at a time.",
        "V, S",
        "10 ft",
        "Up to 1 hour",
        0,
    ),
    (
        "Cantrip: Friends",
        "action",
        None,
        None,
        None,
        "You magically emanate a sense of friendship toward one creature you can see within range. "
        "The target must succeed on a Wisdom saving throw or have the Charmed condition for the duration. "
        "The target succeeds automatically if it isn't a Humanoid, if you're fighting it, or if you have "
        "cast this spell on it within the past 24 hours. "
        "The spell ends early if the target takes damage or if you make an attack roll, deal damage, "
        "or force anyone to make a saving throw. When the spell ends, the target knows it was Charmed by you.",
        "S, M (makeup applied to the face)",
        "Self",
        "1 minute",
        1,
    ),
    (
        "Cantrip: Sorcerous Burst",
        "action",
        None,
        None,
        "d8",
        "Make a ranged spell attack against a creature within range. On a hit, the target takes 1d8 "
        "damage of a type you choose when you cast: acid, cold, fire, lightning, poison, psychic, or "
        "thunder. If any damage die shows its maximum value, roll it again and add the result to the "
        "damage total. At 5th level: 2d8; 11th: 3d8; 17th: 4d8.",
        "V, S",
        "120 ft",
        "Instantaneous",
        0,
    ),
    (
        "Psionic Cantrip: Mind Sliver",
        "action",
        None,
        None,
        None,
        "Drive a spike of psychic energy into the mind of one creature you can see within range. "
        "The target must succeed on an Intelligence saving throw (DC 14) or take 1d6 psychic damage "
        "and subtract 1d4 from the next saving throw it makes before the end of your next turn. "
        "Always prepared via Aberrant Sorcery subclass.",
        "V",
        "60 ft",
        "1 round",
        0,
    ),
    # ── Prepared Spells (use slots) ──────────────────────────────────────────
    (
        "Spell: Mage Armor (1st)",
        "action",
        None,
        None,
        None,
        "Touch a willing creature that isn't wearing armor. Until the spell ends, the target's base AC "
        "becomes 13 + its Dexterity modifier (AC 14 for Inkwell). The spell ends if the target dons "
        "armor or if you dismiss the spell.",
        "V, S, M (a piece of cured leather)",
        "Touch",
        "8 hours",
        0,
    ),
    (
        "Spell: Shield (1st)",
        "reaction",
        None,
        None,
        None,
        "Trigger: you are hit by an attack or targeted by Magic Missile. An invisible barrier of magical "
        "force appears around you. Until the start of your next turn, you gain +5 AC (including against "
        "the triggering attack, potentially turning it into a miss) and you take no damage from "
        "Magic Missile.",
        "V, S",
        "Self",
        "1 round",
        0,
    ),
    (
        "Spell: Catapult (1st)",
        "action",
        None,
        None,
        None,
        "Choose one object weighing 1–5 lbs within range that isn't being worn or carried. It flies in "
        "a straight line up to 90 ft in a direction you choose, stopping early if it hits a solid surface. "
        "If it would strike a creature, that creature makes a DC 14 Dexterity save or takes 3d8 "
        "bludgeoning damage (save for half). At Higher Levels: +1d8 per slot level above 1st.",
        "S",
        "60 ft",
        "Instantaneous",
        0,
    ),
    (
        "Spell: Charm Person (1st)",
        "action",
        None,
        None,
        None,
        "One humanoid you can see within range makes a DC 14 Wisdom saving throw (with Advantage if "
        "you or your companions are fighting it). On a failure, the target is charmed for 1 hour or "
        "until you or your allies harm it. While charmed, it regards you as a friendly acquaintance. "
        "It knows it was charmed when the spell ends. At Higher Levels: +1 target per slot level above 1st.",
        "V, S",
        "30 ft",
        "1 hour",
        0,
    ),
    (
        "Spell: Levitate (2nd)",
        "action",
        None,
        None,
        None,
        "One creature or object (up to 500 lbs) you can see within range rises vertically up to 20 ft "
        "and remains suspended for the duration. An unwilling creature makes a DC 14 Constitution save "
        "to resist. The target can only move horizontally by pushing or pulling against fixed surfaces — "
        "it cannot ascend or descend under its own power.",
        "V, S, M (a small leather loop or golden wire bent into a cup)",
        "60 ft",
        "10 minutes",
        1,
    ),
    (
        "Spell: Hold Person (2nd)",
        "action",
        None,
        None,
        None,
        "One humanoid you can see within range makes a DC 14 Wisdom save or is Paralyzed for the "
        "duration. At the end of each of its turns it repeats the save, ending the spell on a success. "
        "While paralyzed, attacks against it have Advantage, and hits from within 5 ft are critical hits. "
        "At Higher Levels: +1 humanoid per slot level above 2nd.",
        "V, S, M (a small straight piece of iron)",
        "60 ft",
        "1 minute",
        1,
    ),
    # ── Psionic Spells (Always Prepared, use slots) ──────────────────────────
    (
        "Psionic: Arms of Hadar (1st)",
        "action",
        None,
        None,
        None,
        "Tendrils of dark energy erupt from you in a 10-ft radius. Each creature in the area makes a "
        "DC 14 Strength save. On a failure: 2d6 necrotic damage and can't take reactions until its next "
        "turn. On a success: half damage only. Always prepared via Aberrant Sorcery. "
        "At Higher Levels: +1d6 per slot level above 1st.",
        "V, S",
        "Self (10-ft radius)",
        "Instantaneous",
        0,
    ),
    (
        "Psionic: Calm Emotions (2nd)",
        "action",
        None,
        None,
        None,
        "Each humanoid in a 20-ft radius centered on a point within range makes a DC 14 Charisma save "
        "(creatures may choose to fail). On a failure, choose one effect: suppress any effect causing "
        "the target to be Charmed or Frightened; OR make the target indifferent toward creatures it is "
        "hostile to (ends if attacked or harmed). Always prepared via Aberrant Sorcery.",
        "V, S",
        "60 ft",
        "1 minute",
        1,
    ),
    (
        "Psionic: Detect Thoughts (2nd)",
        "action",
        None,
        None,
        None,
        "Read the surface thoughts of one creature you can see within 30 ft as an action each turn. "
        "You can probe deeper — the target makes a DC 14 Wisdom save or you gain insight into its "
        "reasoning, emotional state, and dominant thoughts. You can also use this spell to detect the "
        "presence of thinking creatures you can't see. Always prepared via Aberrant Sorcery.",
        "V, S, M (a copper piece)",
        "Self (30-ft radius)",
        "1 minute",
        1,
    ),
    (
        "Psionic: Dissonant Whispers (1st)",
        "action",
        None,
        None,
        None,
        "Whisper a discordant melody only one creature within range can hear. The target makes a "
        "DC 14 Wisdom save. On a failure: 3d6 psychic damage and must use its reaction to move its "
        "full speed directly away from you. On a success: half damage, no forced movement. Opportunity "
        "attacks against the fleeing target have Advantage. Deafened creatures auto-succeed. "
        "Always prepared. At Higher Levels: +1d6 per slot level above 1st.",
        "V",
        "60 ft",
        "Instantaneous",
        0,
    ),
]

# (name, qty, weight, description, equipped)
_ITEMS = [
    ("Backpack", 1, 5.0, "Standard adventuring backpack.", False),
    ("Traveler's Clothes", 1, 4.0, "Practical fine clothes, well-worn — her default bookkeeper disguise.", True),
    (
        "Ball Bearings",
        2,
        2.0,
        "Bag of 1,000 bearings. Scatter as an action in a 10-ft square: DC 10 DEX save or fall prone.",
        False,
    ),
    ("Blanket", 1, 3.0, "Warm travel blanket.", False),
    ("Rations", 5, 2.0, "Trail rations, 1 day's food each.", False),
    ("Dagger", 2, 1.0, "1d4 piercing. Light, Finesse, Thrown (20/60). Can use DEX or STR.", True),
    ("Waterskin", 1, 5.0, "Holds 4 pints of liquid. Full.", False),
    ("Book", 1, 5.0, "A well-thumbed journal or reference tome — ink-stained and annotated.", False),
    ("Healer's Kit", 1, 3.0, "10 uses. Stabilize a dying creature without a Medicine check.", False),
    ("Disguise Kit", 1, 3.0, "Tools for altering appearance. Inkwell is proficient (Skilled feat).", False),
    (
        "Calligrapher's Supplies",
        1,
        5.0,
        "Inks, quills, and vellum for fine writing. Inkwell is proficient (Background).",
        False,
    ),
]


def apply(conn):
    conn.execute(
        """INSERT INTO characters
               (name, race, class, level, hp, max_hp, ac, speed,
                str, dex, con, int, wis, cha, notes)
           SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
           WHERE NOT EXISTS (SELECT 1 FROM characters WHERE name=?)""",
        _CHAR + (_NAME,),
    )

    cid = conn.execute("SELECT id FROM characters WHERE name=?", (_NAME,)).fetchone()[0]

    for name, atype, uses, recharge, die_type, desc, components, spell_range, duration, concentration in _ABILITIES:
        conn.execute(
            """INSERT INTO abilities
                   (character_id, name, type, description, uses_max, uses_remaining, recharge, die_type,
                    components, spell_range, duration, concentration)
               SELECT ?,?,?,?,?,?,?,?,?,?,?,?
               WHERE NOT EXISTS (
                   SELECT 1 FROM abilities WHERE character_id=? AND name=?
               )""",
            (
                cid,
                name,
                atype,
                desc,
                uses,
                uses,
                recharge,
                die_type,
                components,
                spell_range,
                duration,
                concentration,
                cid,
                name,
            ),
        )
        # Idempotent spell field updates (keeps data current on re-runs)
        conn.execute(
            """UPDATE abilities
               SET description=?, components=?, spell_range=?, duration=?, concentration=?
               WHERE character_id=? AND name=?""",
            (desc, components, spell_range, duration, concentration, cid, name),
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

    # Idempotent updates — keep data current
    conn.execute(
        "UPDATE characters SET skill_proficiencies=? WHERE id=?",
        ("deception,persuasion,investigation,perception,intimidation,performance,insight,stealth", cid),
    )
    conn.execute(
        "UPDATE characters SET save_proficiencies='con,cha',"
        " alignment='Chaotic Neutral', size='Medium', height='5''4\"', weight='130 lbs',"
        " languages='Common,Common Sign,Elvish',"
        " hit_dice_remaining=3, hit_die='d6',"
        " coins_gp=22, coins_sp=8"
        " WHERE id=?",
        (cid,),
    )

    # Weapon stats
    conn.execute(
        """UPDATE inventory
           SET damage_dice=?, damage_type=?, magic_bonus=?,
               is_melee=?, damage_notes=?, is_weapon=1
           WHERE character_id=? AND name=?""",
        ("1d4", "piercing", 0, 1, "Light, Finesse, Thrown 20/60", cid, "Dagger"),
    )

    # Tool proficiencies
    for tool in ("Disguise Kit", "Calligrapher's Supplies"):
        conn.execute(
            "UPDATE inventory SET tool_proficient=1 WHERE character_id=? AND name=?",
            (cid, tool),
        )
