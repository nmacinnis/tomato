"""Character sheet for Inkwell — Changeling Aberrant Sorcerer 4."""

CHARACTER = {
    "name": "Inkwell",
    "race": "Changeling (Fey)",
    "class": "Aberrant Sorcerer",
    "level": 4,
    "hp": 24,  # 19 + 5 at level 4: rolled 3 + CON mod 2
    "max_hp": 24,
    "ac": 12,  # 10 + DEX mod 1 + Hardened Skin 1; Mage Armor → 15
    "speed": 30,
    "str": 9,
    "dex": 12,
    "con": 15,  # 14 + 1 from Changeling Metamorphosis
    "int": 13,
    "wis": 16,
    "cha": 19,  # 17 base + 2 Changeling
    "flat_ac_bonus": 1,
    "save_proficiencies": "con,cha",
    "skill_proficiencies": "deception,persuasion,investigation,perception,intimidation,performance,insight,stealth",
    "languages": "Ionian,Ionian Sign,Whisper",
    "alignment": "Chaotic Neutral",
    "size": "Medium",
    "height": "5'4\"",
    "weight": "130 lbs",
    "hit_die": "d6",
    "spell_slots_1_max": 4,
    "spell_slots_2_max": 3,
    # Play state at creation
    "notes": (
        "Background: Audit Gatherer (Scribe). Bookkeeper turned adventurer; perpetually ink-stained fingers.\n"
        "Estranged from her family — the Lord and Lady of Port Ellsmyre, a minor fishing village in the Riverlands.\n\n"
        "Languages: Ionian, Ionian Sign, Whisper\n\n"
        "Personality: I form many shallow friendships, but almost no close relationships.\n"
        "Ideal: Change. Adaptation is survival.\n"
        "Flaw: I can't resist trying on a pretty face.\n"
        "Bond: I owe much to the Audit, but I was claimed by Neris first.\n"
        "Trinket: A cone snail shell (empty).\n"
    ),
    "hit_dice_remaining": 4,
    "coins_gp": 22,
    "coins_sp": 8,
}

ABILITIES = [
    # ── Changeling (Fey) ─────────────────────────────────────────────────────
    {
        "name": "Shape-Shifter",
        "type": "action",
        "description": (
            "Change appearance and voice (coloration, hair, sex, height, weight, size Medium↔Small). "
            "Can appear as another playable species — stats unchanged. Cannot duplicate someone unseen; "
            "must keep same limb arrangement. Clothing/equipment don't change. "
            "While shape-shifted: Advantage on Charisma checks. Revert by taking an action.\n\n"
            "Metamorphosis (Changeling Metamorphosis feat): each time you use this trait, also choose one — "
            "Aquatic Adaptation (gills and webbed fingers: breathe water, Swim Speed = Speed), "
            "Darkvision 60 ft, or Natural Weapons (claws/fangs/horns/hooves; Unarmed Strike deals 1d6 of the "
            "matching damage type and may use DEX). Benefit lasts until Shape-Shifter is used again."
        ),
    },
    {
        "name": "Changeling Instincts",
        "type": "passive",
        "description": "Fey heritage grants proficiency in Intimidation and Performance.",
    },
    {
        "name": "Feat: Changeling Metamorphosis",
        "type": "passive",
        "description": (
            "Exploring Eberron (2024). Ability Score Increase: +1 Constitution (applied). "
            "Hardened Skin: +1 Armor Class (applied as a flat AC bonus). "
            "Metamorphosis: grants the Shape-Shifter trait an additional choice — see Shape-Shifter."
        ),
    },
    # ── Sorcerer Core ────────────────────────────────────────────────────────
    {
        "name": "Innate Sorcery",
        "type": "bonus_action",
        "uses_max": 2,
        "recharge": "long",
        "description": (
            "Bonus Action: unleash innate magic for 1 minute. While active: "
            "Sorcerer spell save DC +1 (to 15), and Advantage on Sorcerer spell attack rolls. "
            "2 uses per Long Rest."
        ),
        "duration": "1 minute",
        "activatable": 1,
    },
    {
        "name": "Sorcery Points",
        "type": "free_action",
        "uses_max": 4,
        "recharge": "long",
        "description": (
            "Pool of 4 sorcery points. Regain all on Long Rest. Uses:\n"
            "• Metamagic (Extended Spell: 1 SP, Subtle Spell: 1 SP)\n"
            "• Convert slot → SP: spend a slot, gain SP equal to its level (no action).\n"
            "• Create slot (Bonus Action): 1st=2 SP, 2nd=3 SP."
        ),
    },
    {
        "name": "Metamagic: Extended Spell",
        "type": "free_action",
        "description": (
            "Cost: 1 Sorcery Point. When casting a spell with duration 1 min+, double it (max 24 hrs). "
            "If Concentration, gain Advantage on saves to maintain it."
        ),
    },
    {
        "name": "Metamagic: Subtle Spell",
        "type": "free_action",
        "description": (
            "Cost: 1 Sorcery Point. Cast a spell without Verbal, Somatic, or (non-consumed/non-costed) "
            "Material components. Ideal for disguised or social spellcasting."
        ),
    },
    # ── Aberrant Sorcery (Subclass) ──────────────────────────────────────────
    {
        "name": "Telepathic Speech",
        "type": "bonus_action",
        "description": (
            "Choose a visible creature within 30 ft. You and it communicate telepathically while within "
            "CHA modifier miles of each other (min 1 mile). Both must share a known language. "
            "Lasts 3 minutes (Sorcerer level). Ends early if used on a different creature."
        ),
        "duration": "3 minutes",
    },
    {
        "name": "Psionic Spells (Always Prepared)",
        "type": "passive",
        "description": (
            "These spells are always prepared and don't count against the prepared spell limit: "
            "Arms of Hadar, Calm Emotions, Detect Thoughts, Dissonant Whispers, Mind Sliver."
        ),
    },
    # ── Font of Magic Conversions ────────────────────────────────────────────
    {
        "name": "Font of Magic: Slot → Sorcery Points",
        "type": "free_action",
        "description": (
            "Expend a spell slot to gain Sorcery Points equal to the slot's level (no action required). "
            "1st-level slot → 1 SP, 2nd-level slot → 2 SP, etc."
        ),
    },
    {
        "name": "Font of Magic: Sorcery Points → Slot",
        "type": "free_action",
        "description": (
            "Spend Sorcery Points to create a spell slot (no action required). "
            "1st-level slot: 2 SP (min level 2), 2nd-level slot: 3 SP (min level 3). "
            "Created slots vanish on Long Rest."
        ),
    },
    # ── Cantrips ─────────────────────────────────────────────────────────────
    {
        "name": "Cantrip: Mage Hand",
        "type": "action",
        "description": (
            "A spectral hand appears at a point within range. Use it to manipulate an object, open an "
            "unlocked door or container, stow or retrieve an item from an open container, or pour out a vial. "
            "The hand can move up to 30 ft each time you use it. It can't attack, activate magic items, "
            "or carry more than 10 lbs. Vanishes if ever more than 30 ft from you."
        ),
        "components": "V, S",
        "spell_range": "30 ft",
        "duration": "1 minute",
        "concentration": 1,
    },
    {
        "name": "Cantrip: Prestidigitation",
        "type": "action",
        "description": (
            "Create a minor magical effect: a harmless sensory effect; light or snuff a nonmagical flame; "
            "clean or soil, chill, warm, or flavor a 1-cubic-foot object; make a color, mark, or symbol appear "
            "on an object for 1 hour; produce a small trinket or image that fits in your hand (lasts until "
            "end of next turn). Up to three effects active at a time."
        ),
        "components": "V, S",
        "spell_range": "10 ft",
        "duration": "Up to 1 hour",
    },
    {
        "name": "Cantrip: Friends",
        "type": "action",
        "description": (
            "You magically emanate a sense of friendship toward one creature you can see within range. "
            "The target must succeed on a Wisdom saving throw or have the Charmed condition for the duration. "
            "The target succeeds automatically if it isn't a Humanoid, if you're fighting it, or if you have "
            "cast this spell on it within the past 24 hours. "
            "The spell ends early if the target takes damage or if you make an attack roll, deal damage, "
            "or force anyone to make a saving throw. When the spell ends, the target knows it was Charmed by you."
        ),
        "components": "S, M (makeup applied to the face)",
        "spell_range": "Self",
        "duration": "1 minute",
        "concentration": 1,
    },
    {
        "name": "Cantrip: Sorcerous Burst",
        "type": "action",
        "die_type": "d8",
        "description": (
            "Make a ranged spell attack against a creature within range. On a hit, the target takes 1d8 "
            "damage of a type you choose when you cast: acid, cold, fire, lightning, poison, psychic, or "
            "thunder. If any damage die shows its maximum value, roll it again and add the result to the "
            "damage total. At 5th level: 2d8; 11th: 3d8; 17th: 4d8."
        ),
        "components": "V, S",
        "spell_range": "120 ft",
        "duration": "Instantaneous",
    },
    {
        "name": "Psionic Cantrip: Mind Sliver",
        "type": "action",
        "description": (
            "Drive a spike of psychic energy into the mind of one creature you can see within range. "
            "The target must succeed on an Intelligence saving throw or take 1d6 psychic damage "
            "and subtract 1d4 from the next saving throw it makes before the end of your next turn. "
            "Always prepared via Aberrant Sorcery subclass."
        ),
        "components": "V",
        "spell_range": "60 ft",
        "duration": "1 round",
    },
    {
        "name": "Cantrip: Message",
        "type": "action",
        "description": (
            "Point your finger toward a creature within range and whisper a message. Only the target "
            "hears it and can reply in a whisper only you can hear. Can be cast through solid objects "
            "if you are familiar with the target and know it's beyond the barrier. Magical silence, "
            "1 ft of stone, 1 inch of common metal, a thin sheet of lead, or 3 ft of wood or dirt "
            "blocks the spell. Doesn't need to travel in a straight line."
        ),
        "components": "V, S, M (a short piece of copper wire)",
        "spell_range": "120 ft",
        "duration": "1 round",
    },
    # ── Prepared Spells (use slots) ──────────────────────────────────────────
    {
        "name": "Spell: Mage Armor (1st)",
        "type": "action",
        "description": (
            "Touch a willing creature that isn't wearing armor. Until the spell ends, the target's base AC "
            "becomes 13 + its Dexterity modifier (AC 14 for Inkwell). The spell ends if the target dons "
            "armor or if you dismiss the spell."
        ),
        "components": "V, S, M (a piece of cured leather)",
        "spell_range": "Touch",
        "duration": "8 hours",
        "spell_level": 1,
        "sets_base_ac": 1,
        "ac_bonus": 14,
    },
    {
        "name": "Spell: Shield (1st)",
        "type": "reaction",
        "description": (
            "Trigger: you are hit by an attack or targeted by Magic Missile. An invisible barrier of magical "
            "force appears around you. Until the start of your next turn, you gain +5 AC (including against "
            "the triggering attack, potentially turning it into a miss) and you take no damage from "
            "Magic Missile."
        ),
        "components": "V, S",
        "spell_range": "Self",
        "duration": "1 round",
        "spell_level": 1,
    },
    {
        "name": "Spell: Catapult (1st)",
        "type": "action",
        "description": (
            "Choose one object weighing 1–5 lbs within range that isn't being worn or carried. It flies in "
            "a straight line up to 90 ft in a direction you choose, stopping early if it hits a solid surface. "
            "If it would strike a creature, that creature makes a Dexterity save or takes 3d8 "
            "bludgeoning damage (save for half). At Higher Levels: +1d8 per slot level above 1st."
        ),
        "components": "S",
        "spell_range": "60 ft",
        "duration": "Instantaneous",
        "spell_level": 1,
        "upcastable": 1,
    },
    {
        "name": "Spell: Charm Person (1st)",
        "type": "action",
        "description": (
            "One humanoid you can see within range makes a Wisdom saving throw (with Advantage if "
            "you or your companions are fighting it). On a failure, the target is charmed for 1 hour or "
            "until you or your allies harm it. While charmed, it regards you as a friendly acquaintance. "
            "It knows it was charmed when the spell ends. At Higher Levels: +1 target per slot level above 1st."
        ),
        "components": "V, S",
        "spell_range": "30 ft",
        "duration": "1 hour",
        "spell_level": 1,
        "upcastable": 1,
    },
    {
        "name": "Spell: Levitate (2nd)",
        "type": "action",
        "description": (
            "One creature or object (up to 500 lbs) you can see within range rises vertically up to 20 ft "
            "and remains suspended for the duration. An unwilling creature makes a Constitution save "
            "to resist. The target can only move horizontally by pushing or pulling against fixed surfaces — "
            "it cannot ascend or descend under its own power."
        ),
        "components": "V, S, M (a small leather loop or golden wire bent into a cup)",
        "spell_range": "60 ft",
        "duration": "10 minutes",
        "concentration": 1,
        "spell_level": 2,
    },
    {
        "name": "Spell: Maximillian's Earthen Grasp (2nd)",
        "type": "action",
        "description": (
            "A Medium hand of compacted soil bursts from the ground at a point within range, then "
            "strikes one creature within 5 ft of it. The target makes a Strength save or takes 2d6 "
            "bludgeoning damage and has the Restrained condition until the spell ends. As an action, "
            "you can cause the hand to crush the restrained target again (same damage, no save) or "
            "move it up to 5 ft and grapple a different creature within 5 ft, freeing the first."
        ),
        "components": "V, S, M (clay, soil, or stone)",
        "spell_range": "30 ft",
        "duration": "Concentration, up to 1 minute",
        "concentration": 1,
        "spell_level": 2,
    },
    {
        "name": "Spell: Wither and Bloom (2nd)",
        "type": "action",
        "description": (
            "Withering and verdant energy washes over a 10-ft-radius sphere centered on a point within "
            "range. Each creature you choose in that area makes a Constitution save, taking 2d6 "
            "necrotic damage on a failure or half as much on a success (nonmagical vegetation in the "
            "area withers). One creature you choose in the area can spend and roll one of its unspent "
            "Hit Dice, regaining hit points equal to the roll plus your spellcasting ability modifier. "
            "At Higher Levels: damage increases by 1d6, and the number of Hit Dice that can be spent "
            "and added to the healing roll increases by one, for each slot level above 2nd."
        ),
        "components": "V, S, M (a withered vine twisted into a loop)",
        "spell_range": "60 ft",
        "duration": "Instantaneous",
        "spell_level": 2,
        "upcastable": 1,
    },
    # ── Psionic Spells (Always Prepared, use slots) ──────────────────────────
    {
        "name": "Psionic: Arms of Hadar (1st)",
        "type": "action",
        "description": (
            "Tendrils of dark energy erupt from you in a 10-ft radius. Each creature in the area makes a "
            "Strength save. On a failure: 2d6 necrotic damage and can't take reactions until its next "
            "turn. On a success: half damage only. Always prepared via Aberrant Sorcery. "
            "At Higher Levels: +1d6 per slot level above 1st."
        ),
        "components": "V, S",
        "spell_range": "Self (10-ft radius)",
        "duration": "Instantaneous",
        "spell_level": 1,
        "upcastable": 1,
    },
    {
        "name": "Psionic: Calm Emotions (2nd)",
        "type": "action",
        "description": (
            "Each humanoid in a 20-ft radius centered on a point within range makes a Charisma save "
            "(creatures may choose to fail). On a failure, choose one effect: suppress any effect causing "
            "the target to be Charmed or Frightened; OR make the target indifferent toward creatures it is "
            "hostile to (ends if attacked or harmed). Always prepared via Aberrant Sorcery."
        ),
        "components": "V, S",
        "spell_range": "60 ft",
        "duration": "1 minute",
        "concentration": 1,
        "spell_level": 2,
    },
    {
        "name": "Psionic: Detect Thoughts (2nd)",
        "type": "action",
        "description": (
            "Read the surface thoughts of one creature you can see within 30 ft as an action each turn. "
            "You can probe deeper — the target makes a Wisdom save or you gain insight into its "
            "reasoning, emotional state, and dominant thoughts. You can also use this spell to detect the "
            "presence of thinking creatures you can't see. Always prepared via Aberrant Sorcery."
        ),
        "components": "V, S, M (a copper piece)",
        "spell_range": "Self (30-ft radius)",
        "duration": "1 minute",
        "concentration": 1,
        "spell_level": 2,
    },
    {
        "name": "Psionic: Dissonant Whispers (1st)",
        "type": "action",
        "description": (
            "Whisper a discordant melody only one creature within range can hear. The target makes a "
            "Wisdom save. On a failure: 3d6 psychic damage and must use its reaction to move its "
            "full speed directly away from you. On a success: half damage, no forced movement. Opportunity "
            "attacks against the fleeing target have Advantage. Deafened creatures auto-succeed. "
            "Always prepared. At Higher Levels: +1d6 per slot level above 1st."
        ),
        "components": "V",
        "spell_range": "60 ft",
        "duration": "Instantaneous",
        "spell_level": 1,
        "upcastable": 1,
    },
]

ITEMS = [
    {
        "name": "Backpack",
        "quantity": 1,
        "weight": 5.0,
        "description": "Standard adventuring backpack.",
        "equipped": 0,
    },
    {
        "name": "Traveler's Clothes",
        "quantity": 1,
        "weight": 4.0,
        "description": "Practical fine clothes, well-worn — her default bookkeeper disguise.",
        "equipped": 1,
    },
    {
        "name": "Ball Bearings",
        "quantity": 2,
        "weight": 2.0,
        "description": "Bag of 1,000 bearings. Scatter as an action in a 10-ft square: DC 10 DEX save or fall prone.",
        "equipped": 0,
    },
    {
        "name": "Blanket",
        "quantity": 1,
        "weight": 3.0,
        "description": "Warm travel blanket.",
        "equipped": 0,
    },
    {
        "name": "Rations",
        "quantity": 5,
        "weight": 2.0,
        "description": "Trail rations, 1 day's food each.",
        "equipped": 0,
    },
    {
        "name": "Dagger",
        "quantity": 2,
        "weight": 1.0,
        "description": "1d4 piercing. Light, Finesse, Thrown (20/60). Can use DEX or STR.",
        "equipped": 1,
        "is_weapon": 1,
        "is_melee": 1,
        "finesse": 1,
        "damage_dice": "1d4",
        "damage_type": "piercing",
        "magic_bonus": 0,
        "damage_notes": "Light, Finesse, Thrown 20/60",
    },
    {
        "name": "Waterskin",
        "quantity": 1,
        "weight": 5.0,
        "description": "Holds 4 pints of liquid. Full.",
        "equipped": 0,
    },
    {
        "name": "Book",
        "quantity": 1,
        "weight": 5.0,
        "description": "A well-thumbed journal or reference tome — ink-stained and annotated.",
        "equipped": 0,
    },
    {
        "name": "Healer's Kit",
        "quantity": 1,
        "weight": 3.0,
        "description": "10 uses. Stabilize a dying creature without a Medicine check.",
        "equipped": 0,
    },
    {
        "name": "Disguise Kit",
        "quantity": 1,
        "weight": 3.0,
        "description": "Tools for altering appearance. Inkwell is proficient (Skilled feat).",
        "equipped": 0,
        "tool_proficient": 1,
    },
    {
        "name": "Calligrapher's Supplies",
        "quantity": 1,
        "weight": 5.0,
        "description": "Inks, quills, and vellum for fine writing. Inkwell is proficient (Background).",
        "equipped": 0,
        "tool_proficient": 1,
    },
]


# ── Seed steps ────────────────────────────────────────────────────────────────
# One-time changes to an existing Inkwell. Sheet fields (max_hp, con, uses_max,
# spell_slots_N_max, …) are refreshed from the Sheet right after the steps run,
# so steps only adjust Play state and rename/remove rows. `level-4` predates
# LEVELS; future level-ups go in LEVELS, not here.


def _spell_slots_to_columns(conn, cid):
    # Slots used to be ability rows; level-3 pools were 4 × 1st, 2 × 2nd.
    conn.execute(
        """UPDATE characters
           SET spell_slots_1_max=4, spell_slots_1_remaining=4,
               spell_slots_2_max=2, spell_slots_2_remaining=2
           WHERE id=? AND spell_slots_1_max=0 AND spell_slots_2_max=0""",
        (cid,),
    )
    conn.execute(
        "DELETE FROM abilities WHERE character_id=? AND name IN (?, ?)",
        (cid, "Spell Slots — 1st Level", "Spell Slots — 2nd Level"),
    )


def _level_4(conn, cid):
    # +5 HP, a 3rd 2nd-level slot, a 4th hit die, and a 4th Sorcery Point
    conn.execute(
        """UPDATE characters
           SET hp=hp+5, spell_slots_2_remaining=spell_slots_2_remaining+1,
               hit_dice_remaining=hit_dice_remaining+1
           WHERE id=? AND level<4""",
        (cid,),
    )
    conn.execute(
        """UPDATE abilities SET uses_remaining=uses_remaining+1
           WHERE character_id=? AND name='Sorcery Points' AND uses_max=3""",
        (cid,),
    )


def _retire_hold_person(conn, cid):
    # Replaced by Maximillian's Earthen Grasp / Wither and Bloom
    conn.execute("DELETE FROM abilities WHERE character_id=? AND name=?", (cid, "Spell: Hold Person (2nd)"))


STEPS = [
    ("spell-slots-to-columns", _spell_slots_to_columns),
    ("level-4", _level_4),
    ("retire-hold-person", _retire_hold_person),
]
