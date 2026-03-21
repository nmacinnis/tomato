"""Character sheet for Inkwell — Changeling Aberrant Sorcerer 3."""

_NAME = "Inkwell"

_CHAR = (
    _NAME,
    "Changeling (Fey)",
    "Aberrant Sorcerer",
    3,
    19,   # hp (rolled: 3+4+6 = 13 + CON mod 2×3 = 6 → 19)
    19,   # max_hp
    11,   # ac (10 + DEX mod 1; Mage Armor → 14)
    30,
    9,    # str
    12,   # dex
    14,   # con
    13,   # int
    16,   # wis
    19,   # cha (17 base + 2 Changeling)
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

# (name, type, uses_max, recharge, die_type, description)
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
    ),
    (
        "Changeling Instincts",
        "passive",
        None,
        None,
        None,
        "Fey heritage grants proficiency in Intimidation and Performance.",
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
    ),
    (
        "Metamagic: Extended Spell",
        "passive",
        None,
        None,
        None,
        "Cost: 1 Sorcery Point. When casting a spell with duration 1 min+, double it (max 24 hrs). "
        "If Concentration, gain Advantage on saves to maintain it.",
    ),
    (
        "Metamagic: Subtle Spell",
        "passive",
        None,
        None,
        None,
        "Cost: 1 Sorcery Point. Cast a spell without Verbal, Somatic, or (non-consumed/non-costed) "
        "Material components. Ideal for disguised or social spellcasting.",
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
    ),
    (
        "Psionic Spells (Always Prepared)",
        "passive",
        None,
        None,
        None,
        "These spells are always prepared and don't count against the prepared spell limit: "
        "Arms of Hadar, Calm Emotions, Detect Thoughts, Dissonant Whispers, Mind Sliver.",
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
    ),
    (
        "Spell Slots — 2nd Level",
        "free_action",
        2,
        "long",
        None,
        "2 second-level spell slots. Regain all on Long Rest. "
        "Can convert to Sorcery Points (2 SP per slot, no action).",
    ),
    # ── Cantrips ─────────────────────────────────────────────────────────────
    (
        "Cantrip: Mage Hand",
        "action",
        None,
        None,
        None,
        "Spectral hand appears within 30 ft. Manipulate objects, open unlocked doors/containers, "
        "stow/retrieve items, pour liquid. Carry up to 10 lbs. Concentration, up to 1 min.",
    ),
    (
        "Cantrip: Prestidigitation",
        "action",
        None,
        None,
        None,
        "Minor magical tricks: harmless sensory effect, light/snuff fire, clean/soil/chill/warm/flavor "
        "1 cu ft, color/mark object (1 hr), produce a small trinket or image (in hand, until next turn).",
    ),
    (
        "Cantrip: Friends",
        "action",
        None,
        None,
        None,
        "Concentration, up to 1 minute. Non-hostile target creature: Advantage on all Charisma checks "
        "against it while spell lasts. Creature knows it was influenced when the spell ends.",
    ),
    (
        "Cantrip: Sorcerous Burst",
        "action",
        None,
        None,
        "d8",
        "Ranged spell attack, range 120 ft. Hit: 1d8 damage (acid/cold/fire/lightning/poison/psychic/"
        "thunder — chosen on cast). If any die shows its max value, roll it again and add the result. "
        "Damage increases at higher levels.",
    ),
    (
        "Psionic Cantrip: Mind Sliver",
        "action",
        None,
        None,
        None,
        "Range 60 ft. Target makes an INT save (DC 14) or takes 1d6 psychic damage and subtracts 1d4 "
        "from the next saving throw it makes before end of your next turn. Always prepared via subclass.",
    ),
    # ── Prepared Spells (use slots) ──────────────────────────────────────────
    (
        "Spell: Mage Armor (1st)",
        "action",
        None,
        None,
        None,
        "1st-level slot. Touch a willing unarmored creature. AC = 13 + DEX mod (14 for Inkwell). "
        "Duration: 8 hours, no Concentration. Cast on self for AC 14.",
    ),
    (
        "Spell: Shield (1st)",
        "reaction",
        None,
        None,
        None,
        "1st-level slot. Reaction: when hit by an attack or targeted by Magic Missile. "
        "+5 AC until start of your next turn (can turn the hit into a miss). "
        "Also blocks Magic Missile automatically.",
    ),
    (
        "Spell: Catapult (1st)",
        "action",
        None,
        None,
        None,
        "1st-level slot. Hurl a 1–5 lb object up to 90 ft. One creature in its path: "
        "DEX save (DC 14) or 3d8 bludgeoning. Higher slots: +1d8 per level above 1st.",
    ),
    (
        "Spell: Charm Person (1st)",
        "action",
        None,
        None,
        None,
        "1st-level slot. Range 30 ft. Target humanoid: WIS save (DC 14) or charmed 1 hr "
        "(or until harmed by you/allies). Treats you as friendly acquaintance. Knows it was charmed after. "
        "Higher slots: +1 target per level above 1st.",
    ),
    (
        "Spell: Levitate (2nd)",
        "action",
        None,
        None,
        None,
        "2nd-level slot. Concentration, 10 min. Target creature or object (max 500 lbs): "
        "CON save (DC 14) to resist. Rises/descends up to 20 ft per turn. "
        "Levitating creature can move horizontally but can't ascend/descend on its own.",
    ),
    (
        "Spell: Hold Person (2nd)",
        "action",
        None,
        None,
        None,
        "2nd-level slot. Concentration, 1 min. Range 60 ft. Humanoid: WIS save (DC 14) or Paralyzed. "
        "Repeats save each turn. Attacks vs it have Advantage; hits within 5 ft auto-crit. "
        "Higher slots: +1 humanoid per level above 2nd.",
    ),
    # ── Psionic Spells (Always Prepared, use slots) ──────────────────────────
    (
        "Psionic: Arms of Hadar (1st)",
        "action",
        None,
        None,
        None,
        "1st-level slot. Always prepared. Tendrils erupt in 10-ft radius around you. "
        "Each creature: STR save (DC 14) or 2d6 necrotic damage + can't use reactions until next turn. "
        "Save: half damage, no reaction loss. Higher slots: +1d6 per level above 1st.",
    ),
    (
        "Psionic: Calm Emotions (2nd)",
        "action",
        None,
        None,
        None,
        "2nd-level slot. Always prepared. Concentration, 1 min. 20-ft radius, range 60 ft. "
        "Each humanoid: CHA save (DC 14) or suppress fear/charm effects, OR become indifferent "
        "toward hostile creatures (ends if attacked).",
    ),
    (
        "Psionic: Detect Thoughts (2nd)",
        "action",
        None,
        None,
        None,
        "2nd-level slot. Always prepared. Concentration, 1 min. Read surface thoughts of creatures "
        "within 30 ft. Focus to probe deeper: target makes WIS save (DC 14) to resist. "
        "Also usable to detect thinking creatures behind doors.",
    ),
    (
        "Psionic: Dissonant Whispers (1st)",
        "action",
        None,
        None,
        None,
        "1st-level slot. Always prepared. Whisper a discordant melody to one creature within 60 ft. "
        "WIS save (DC 14) or 3d6 psychic damage and must immediately flee max speed using its reaction. "
        "Save: half damage, no flee. Opportunity attacks against fleeing target have Advantage. "
        "Higher slots: +1d6 per level above 1st.",
    ),
]

# (name, qty, weight, description, equipped)
_ITEMS = [
    ("Backpack", 1, 5.0, "Standard adventuring backpack.", False),
    ("Traveler's Clothes", 1, 4.0, "Practical fine clothes, well-worn — her default bookkeeper disguise.", True),
    ("Ball Bearings", 2, 2.0, "Bag of 1,000 bearings. Scatter as an action in a 10-ft square: DC 10 DEX save or fall prone.", False),
    ("Blanket", 1, 3.0, "Warm travel blanket.", False),
    ("Rations", 5, 2.0, "Trail rations, 1 day's food each.", False),
    ("Dagger", 2, 1.0, "1d4 piercing. Light, Finesse, Thrown (20/60). Can use DEX or STR.", True),
    ("Waterskin", 1, 5.0, "Holds 4 pints of liquid. Full.", False),
    ("Book", 1, 5.0, "A well-thumbed journal or reference tome — ink-stained and annotated.", False),
    ("Healer's Kit", 1, 3.0, "10 uses. Stabilize a dying creature without a Medicine check.", False),
    ("Disguise Kit", 1, 3.0, "Tools for altering appearance. Inkwell is proficient (Skilled feat).", False),
    ("Calligrapher's Supplies", 1, 5.0, "Inks, quills, and vellum for fine writing. Inkwell is proficient (Background).", False),
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

    # Idempotent updates — keep data current
    conn.execute(
        "UPDATE characters SET skill_proficiencies=? WHERE id=?",
        ("deception,persuasion,investigation,perception,intimidation,performance,insight,stealth", cid),
    )
    conn.execute(
        "UPDATE characters SET save_proficiencies='con,cha',"
        " alignment='Chaotic Neutral', size='Medium', height='5''4\"', weight='130 lbs',"
        " languages='Common,Common Sign,Elvish',"
        " hit_dice_remaining=3, hit_die='d6'"
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
