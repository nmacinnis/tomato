"""Character sheet for Inkwell — Changeling Aberrant Sorcerer 4."""

_NAME = "Inkwell"

_CHAR = (
    _NAME,
    "Changeling (Fey)",
    "Aberrant Sorcerer",
    4,
    24,  # hp (19 + 5 at level 4: rolled 3 + CON mod 2)
    24,  # max_hp
    12,  # ac (10 + DEX mod 1 + Hardened Skin 1; Mage Armor → 15)
    30,
    9,  # str
    12,  # dex
    15,  # con (14 + 1 from Changeling Metamorphosis)
    13,  # int
    16,  # wis
    19,  # cha (17 base + 2 Changeling)
    (
        "Background: Audit Gatherer (Scribe). Bookkeeper turned adventurer; perpetually ink-stained fingers.\n"
        "Estranged from her family — the Lord and Lady of Port Ellsmyre, a minor fishing village in the Riverlands.\n\n"
        "Languages: Ionian, Ionian Sign, Whisper\n\n"
        "Personality: I form many shallow friendships, but almost no close relationships.\n"
        "Ideal: Change. Adaptation is survival.\n"
        "Flaw: I can't resist trying on a pretty face.\n"
        "Bond: I owe much to the Audit, but I was claimed by Neris first.\n"
        "Trinket: A cone snail shell (empty).\n"
    ),
)

# (name, type, uses_max, recharge, die_type, description, components, spell_range, duration, concentration, spell_level, upcastable)
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
        "While shape-shifted: Advantage on Charisma checks. Revert by taking an action.\n\n"
        "Metamorphosis (Changeling Metamorphosis feat): each time you use this trait, also choose one — "
        "Aquatic Adaptation (gills and webbed fingers: breathe water, Swim Speed = Speed), "
        "Darkvision 60 ft, or Natural Weapons (claws/fangs/horns/hooves; Unarmed Strike deals 1d6 of the "
        "matching damage type and may use DEX). Benefit lasts until Shape-Shifter is used again.",
        "",
        "",
        "",
        0,
        None, 0,
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
        None, 0,
    ),
    (
        "Feat: Changeling Metamorphosis",
        "passive",
        None,
        None,
        None,
        "Exploring Eberron (2024). Ability Score Increase: +1 Constitution (applied). "
        "Hardened Skin: +1 Armor Class (applied as a flat AC bonus). "
        "Metamorphosis: grants the Shape-Shifter trait an additional choice — see Shape-Shifter.",
        "",
        "",
        "",
        0,
        None, 0,
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
        None, 0,
    ),
    (
        "Sorcery Points",
        "passive",
        4,
        "long",
        None,
        "Pool of 4 sorcery points. Regain all on Long Rest. Uses:\n"
        "• Metamagic (Extended Spell: 1 SP, Subtle Spell: 1 SP)\n"
        "• Convert slot → SP: spend a slot, gain SP equal to its level (no action).\n"
        "• Create slot (Bonus Action): 1st=2 SP, 2nd=3 SP.",
        "",
        "",
        "",
        0,
        None, 0,
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
        None, 0,
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
        None, 0,
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
        None, 0,
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
        None, 0,
    ),
    # ── Font of Magic Conversions ────────────────────────────────────────────
    (
        "Font of Magic: Slot → Sorcery Points",
        "free_action",
        None,
        None,
        None,
        "Expend a spell slot to gain Sorcery Points equal to the slot's level (no action required). "
        "1st-level slot → 1 SP, 2nd-level slot → 2 SP, etc.",
        "",
        "",
        "",
        0,
        None, 0,
    ),
    (
        "Font of Magic: Sorcery Points → Slot",
        "free_action",
        None,
        None,
        None,
        "Spend Sorcery Points to create a spell slot (no action required). "
        "1st-level slot: 2 SP (min level 2), 2nd-level slot: 3 SP (min level 3). "
        "Created slots vanish on Long Rest.",
        "",
        "",
        "",
        0,
        None, 0,
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
        None, 0,
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
        None, 0,
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
        None, 0,
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
        None, 0,
    ),
    (
        "Psionic Cantrip: Mind Sliver",
        "action",
        None,
        None,
        None,
        "Drive a spike of psychic energy into the mind of one creature you can see within range. "
        "The target must succeed on an Intelligence saving throw or take 1d6 psychic damage "
        "and subtract 1d4 from the next saving throw it makes before the end of your next turn. "
        "Always prepared via Aberrant Sorcery subclass.",
        "V",
        "60 ft",
        "1 round",
        0,
        None, 0,
    ),
    (
        "Cantrip: Message",
        "action",
        None,
        None,
        None,
        "Point your finger toward a creature within range and whisper a message. Only the target "
        "hears it and can reply in a whisper only you can hear. Can be cast through solid objects "
        "if you are familiar with the target and know it's beyond the barrier. Magical silence, "
        "1 ft of stone, 1 inch of common metal, a thin sheet of lead, or 3 ft of wood or dirt "
        "blocks the spell. Doesn't need to travel in a straight line.",
        "V, S, M (a short piece of copper wire)",
        "120 ft",
        "1 round",
        0,
        None, 0,
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
        1, 0,
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
        1, 0,
    ),
    (
        "Spell: Catapult (1st)",
        "action",
        None,
        None,
        None,
        "Choose one object weighing 1–5 lbs within range that isn't being worn or carried. It flies in "
        "a straight line up to 90 ft in a direction you choose, stopping early if it hits a solid surface. "
        "If it would strike a creature, that creature makes a Dexterity save or takes 3d8 "
        "bludgeoning damage (save for half). At Higher Levels: +1d8 per slot level above 1st.",
        "S",
        "60 ft",
        "Instantaneous",
        0,
        1, 1,
    ),
    (
        "Spell: Charm Person (1st)",
        "action",
        None,
        None,
        None,
        "One humanoid you can see within range makes a Wisdom saving throw (with Advantage if "
        "you or your companions are fighting it). On a failure, the target is charmed for 1 hour or "
        "until you or your allies harm it. While charmed, it regards you as a friendly acquaintance. "
        "It knows it was charmed when the spell ends. At Higher Levels: +1 target per slot level above 1st.",
        "V, S",
        "30 ft",
        "1 hour",
        0,
        1, 1,
    ),
    (
        "Spell: Levitate (2nd)",
        "action",
        None,
        None,
        None,
        "One creature or object (up to 500 lbs) you can see within range rises vertically up to 20 ft "
        "and remains suspended for the duration. An unwilling creature makes a Constitution save "
        "to resist. The target can only move horizontally by pushing or pulling against fixed surfaces — "
        "it cannot ascend or descend under its own power.",
        "V, S, M (a small leather loop or golden wire bent into a cup)",
        "60 ft",
        "10 minutes",
        1,
        2, 0,
    ),
    (
        "Spell: Maximillian's Earthen Grasp (2nd)",
        "action",
        None,
        None,
        None,
        "A Medium hand of compacted soil bursts from the ground at a point within range, then "
        "strikes one creature within 5 ft of it. The target makes a Strength save or takes 2d6 "
        "bludgeoning damage and has the Restrained condition until the spell ends. As an action, "
        "you can cause the hand to crush the restrained target again (same damage, no save) or "
        "move it up to 5 ft and grapple a different creature within 5 ft, freeing the first.",
        "V, S, M (clay, soil, or stone)",
        "30 ft",
        "Concentration, up to 1 minute",
        1,
        2, 0,
    ),
    (
        "Spell: Wither and Bloom (2nd)",
        "action",
        None,
        None,
        None,
        "Withering and verdant energy washes over a 10-ft-radius sphere centered on a point within "
        "range. Each creature you choose in that area makes a Constitution save, taking 2d6 "
        "necrotic damage on a failure or half as much on a success (nonmagical vegetation in the "
        "area withers). One creature you choose in the area can spend and roll one of its unspent "
        "Hit Dice, regaining hit points equal to the roll plus your spellcasting ability modifier. "
        "At Higher Levels: damage increases by 1d6, and the number of Hit Dice that can be spent "
        "and added to the healing roll increases by one, for each slot level above 2nd.",
        "V, S, M (a withered vine twisted into a loop)",
        "60 ft",
        "Instantaneous",
        0,
        2, 1,
    ),
    # ── Psionic Spells (Always Prepared, use slots) ──────────────────────────
    (
        "Psionic: Arms of Hadar (1st)",
        "action",
        None,
        None,
        None,
        "Tendrils of dark energy erupt from you in a 10-ft radius. Each creature in the area makes a "
        "Strength save. On a failure: 2d6 necrotic damage and can't take reactions until its next "
        "turn. On a success: half damage only. Always prepared via Aberrant Sorcery. "
        "At Higher Levels: +1d6 per slot level above 1st.",
        "V, S",
        "Self (10-ft radius)",
        "Instantaneous",
        0,
        1, 1,
    ),
    (
        "Psionic: Calm Emotions (2nd)",
        "action",
        None,
        None,
        None,
        "Each humanoid in a 20-ft radius centered on a point within range makes a Charisma save "
        "(creatures may choose to fail). On a failure, choose one effect: suppress any effect causing "
        "the target to be Charmed or Frightened; OR make the target indifferent toward creatures it is "
        "hostile to (ends if attacked or harmed). Always prepared via Aberrant Sorcery.",
        "V, S",
        "60 ft",
        "1 minute",
        1,
        2, 0,
    ),
    (
        "Psionic: Detect Thoughts (2nd)",
        "action",
        None,
        None,
        None,
        "Read the surface thoughts of one creature you can see within 30 ft as an action each turn. "
        "You can probe deeper — the target makes a Wisdom save or you gain insight into its "
        "reasoning, emotional state, and dominant thoughts. You can also use this spell to detect the "
        "presence of thinking creatures you can't see. Always prepared via Aberrant Sorcery.",
        "V, S, M (a copper piece)",
        "Self (30-ft radius)",
        "1 minute",
        1,
        2, 0,
    ),
    (
        "Psionic: Dissonant Whispers (1st)",
        "action",
        None,
        None,
        None,
        "Whisper a discordant melody only one creature within range can hear. The target makes a "
        "Wisdom save. On a failure: 3d6 psychic damage and must use its reaction to move its "
        "full speed directly away from you. On a success: half damage, no forced movement. Opportunity "
        "attacks against the fleeing target have Advantage. Deafened creatures auto-succeed. "
        "Always prepared. At Higher Levels: +1d6 per slot level above 1st.",
        "V",
        "60 ft",
        "Instantaneous",
        0,
        1, 1,
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
                str, dex, con, int, wis, cha, notes, coins_gp, coins_sp, hit_dice_remaining)
           SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
           WHERE NOT EXISTS (SELECT 1 FROM characters WHERE name=?)""",
        _CHAR + (22, 8, 4, _NAME),
    )

    cid = conn.execute("SELECT id FROM characters WHERE name=?", (_NAME,)).fetchone()[0]

    for name, atype, uses, recharge, die_type, desc, components, spell_range, duration, concentration, spell_level, upcastable in _ABILITIES:
        conn.execute(
            """INSERT INTO abilities
                   (character_id, name, type, description, uses_max, uses_remaining, recharge, die_type,
                    components, spell_range, duration, concentration, spell_level, upcastable)
               SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?
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
                spell_level,
                upcastable,
                cid,
                name,
            ),
        )
        # Idempotent spell field updates (keeps data current on re-runs)
        conn.execute(
            """UPDATE abilities
               SET description=?, components=?, spell_range=?, duration=?, concentration=?,
                   spell_level=?, upcastable=?
               WHERE character_id=? AND name=?""",
            (desc, components, spell_range, duration, concentration, spell_level, upcastable, cid, name),
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
        " languages='Ionian,Ionian Sign,Whisper',"
        " hit_die='d6'"
        " WHERE id=?",
        (cid,),
    )

    # Innate Sorcery: activatable — Use button sets active=1 (+1 DC, ADV on spell attacks)
    conn.execute(
        "UPDATE abilities SET activatable=1 WHERE character_id=? AND name=?",
        (cid, "Innate Sorcery"),
    )

    # Mage Armor: sets base AC when active (13 + DEX mod 1 = 14 for Inkwell)
    conn.execute(
        "UPDATE abilities SET sets_base_ac=1, ac_bonus=14 WHERE character_id=? AND name=?",
        (cid, "Spell: Mage Armor (1st)"),
    )

    # Weapon stats
    conn.execute(
        """UPDATE inventory
           SET damage_dice=?, damage_type=?, magic_bonus=?,
               is_melee=?, finesse=1, damage_notes=?, is_weapon=1
           WHERE character_id=? AND name=?""",
        ("1d4", "piercing", 0, 1, "Light, Finesse, Thrown 20/60", cid, "Dagger"),
    )

    # Tool proficiencies
    for tool in ("Disguise Kit", "Calligrapher's Supplies"):
        conn.execute(
            "UPDATE inventory SET tool_proficient=1 WHERE character_id=? AND name=?",
            (cid, tool),
        )

    # Spell slots as character stats — always keep max current; init remaining only on first use
    conn.execute(
        "UPDATE characters SET spell_slots_1_max=4, spell_slots_2_max=3 WHERE id=?",
        (cid,),
    )
    conn.execute(
        """UPDATE characters
           SET spell_slots_1_remaining=4
           WHERE id=? AND spell_slots_1_remaining=0 AND spell_slots_1_max=4""",
        (cid,),
    )
    conn.execute(
        """UPDATE characters
           SET spell_slots_2_remaining=3
           WHERE id=? AND spell_slots_2_remaining=0 AND spell_slots_2_max=3""",
        (cid,),
    )

    # Remove legacy spell slot ability rows if they still exist
    conn.execute(
        "DELETE FROM abilities WHERE character_id=? AND name IN (?, ?)",
        (cid, "Spell Slots — 1st Level", "Spell Slots — 2nd Level"),
    )

    # Level 4: +5 HP, +1 CON, +1 AC (Changeling Metamorphosis), a 3rd 2nd-level
    # spell slot, and a 4th hit die
    conn.execute(
        """UPDATE characters
           SET level=4, hp=hp+5, max_hp=max_hp+5, con=con+1, ac=ac+1, flat_ac_bonus=flat_ac_bonus+1,
               spell_slots_2_remaining=spell_slots_2_remaining+1,
               hit_dice_remaining=hit_dice_remaining+1
           WHERE id=? AND level<4""",
        (cid,),
    )

    # Level 4: Sorcery Points pool grows from 3 to 4 — gain the new point
    conn.execute(
        """UPDATE abilities
           SET uses_max=4, uses_remaining=uses_remaining+1
           WHERE character_id=? AND name='Sorcery Points' AND uses_max=3""",
        (cid,),
    )

    # Hold Person retired in favor of Maximillian's Earthen Grasp / Wither and Bloom
    conn.execute(
        "DELETE FROM abilities WHERE character_id=? AND name=?",
        (cid, "Spell: Hold Person (2nd)"),
    )
