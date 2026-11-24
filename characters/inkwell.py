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
    # Spells: Rules text and card details come from spells.py; `description` is
    # the Summary (see GLOSSARY.md).
    {
        "name": "Cantrip: Mage Hand",
        "spell": "Mage Hand",
        "type": "action",
        "description": (
            "A spectral hand within 30 ft manipulates an object, opens an unlocked door or container, "
            "stows or retrieves an item from an open container, or pours out a vial. Magic action on later "
            "turns to use it again and move it up to 30 ft. Can't attack or activate magic items; carries "
            "up to 10 lb. Vanishes if more than 30 ft from you."
        ),
    },
    {
        "name": "Cantrip: Prestidigitation",
        "spell": "Prestidigitation",
        "type": "action",
        "description": (
            "Pick one: a harmless sensory effect; light or snuff a candle, torch, or small campfire; clean "
            "or soil a 1-cubic-foot object; chill, warm, or flavor 1 cubic foot of material (1 hr); a "
            "color, mark, or symbol on an object (1 hr); or a hand-sized trinket or illusory image (until "
            "end of next turn). Up to three lasting effects at once."
        ),
    },
    {
        "name": "Cantrip: Friends",
        "spell": "Friends",
        "type": "action",
        "description": (
            "One creature within 10 ft: Wisdom save or Charmed for the duration. Auto-succeeds if it "
            "isn't a Humanoid, you're fighting it, or you've cast this on it in the past 24 hours. Ends "
            "early if it takes damage or you attack, deal damage, or force a save; it then knows it was "
            "Charmed by you."
        ),
    },
    {
        "name": "Cantrip: Sorcerous Burst",
        "spell": "Sorcerous Burst",
        "type": "action",
        "die_type": "d8",
        "description": (
            "Ranged spell attack: 1d8 damage, your choice of Acid, Cold, Fire, Lightning, Poison, Psychic, "
            "or Thunder. Each 8 rolled lets you add another d8, up to your Charisma modifier in extra dice. "
            "2d8 at level 5."
        ),
    },
    {
        "name": "Psionic Cantrip: Mind Sliver",
        "spell": "Mind Sliver",
        "type": "action",
        "description": (
            "One creature you can see: Intelligence save or 1d6 Psychic damage and it subtracts 1d4 from "
            "its next saving throw before the end of your next turn. 2d6 at level 5. "
            "Always prepared (Aberrant Sorcery)."
        ),
    },
    {
        "name": "Cantrip: Message",
        "spell": "Message",
        "type": "action",
        "description": (
            "Whisper to a creature within 120 ft; only it hears, and it can whisper back. Works through "
            "solid objects if you know the target and that it's beyond the barrier. Blocked by magical "
            "silence; 1 ft of stone, metal, or wood; or a thin sheet of lead."
        ),
    },
    # ── Prepared Spells (use slots) ──────────────────────────────────────────
    {
        "name": "Spell: Mage Armor (1st)",
        "spell": "Mage Armor",
        "type": "action",
        "description": (
            "Touch a willing creature not wearing armor: its base AC becomes 13 + its Dexterity modifier "
            "for 8 hours (AC 14 for Inkwell). Ends early if it dons armor."
        ),
        "sets_base_ac": 1,
        "ac_bonus": 14,
    },
    {
        "name": "Spell: Shield (1st)",
        "spell": "Shield",
        "type": "reaction",
        "description": (
            "Reaction when you're hit by an attack roll or targeted by Magic Missile: +5 AC until the "
            "start of your next turn, including against the triggering attack, and no damage from "
            "Magic Missile."
        ),
    },
    {
        "name": "Spell: Catapult (1st)",
        "spell": "Catapult",
        "type": "action",
        "description": (
            "Fling a 1–5 lb object no one is wearing or carrying up to 90 ft in a straight line. A "
            "creature it would strike makes a Dexterity save; on a failure the object hits it, and both "
            "take 3d8 bludgeoning damage (no damage on a success). Upcast: +5 lb and +1d8 per slot level "
            "above 1st."
        ),
        "upcastable": 1,
    },
    {
        "name": "Spell: Charm Person (1st)",
        "spell": "Charm Person",
        "type": "action",
        "description": (
            "One Humanoid within 30 ft: Wisdom save (with Advantage if you or your allies are fighting it) "
            "or Charmed for 1 hour, and Friendly to you. Ends early if you or your allies damage it; it "
            "knows it was Charmed afterwards. Upcast: +1 target per slot level above 1st."
        ),
        "upcastable": 1,
    },
    {
        "name": "Spell: Levitate (2nd)",
        "spell": "Levitate",
        "type": "action",
        "description": (
            "A creature or loose object (up to 500 lb) within 60 ft rises up to 20 ft and hangs there; an "
            "unwilling creature resists with a Constitution save. It moves only by pushing or pulling on "
            "fixed surfaces. You change its altitude by up to 20 ft on your turn (a Magic action unless "
            "you're the target). It floats gently down when the spell ends."
        ),
    },
    {
        "name": "Spell: Maximilian's Earthen Grasp (2nd)",
        "spell": "Maximilian's Earthen Grasp",
        "type": "action",
        "description": (
            "A soil hand rises in a 5-ft space within 30 ft and grabs a creature within 5 ft of it: "
            "Strength save or 2d6 bludgeoning and Restrained. Action: crush the target (Strength save, "
            "2d6 or half), or send the hand at another creature or space (releasing the first). The "
            "target escapes with a Strength check against your spell save DC."
        ),
    },
    {
        "name": "Spell: Wither and Bloom (2nd)",
        "spell": "Wither and Bloom",
        "type": "action",
        "description": (
            "10-ft-radius sphere within 60 ft: creatures you choose make a Constitution save, 2d6 necrotic "
            "or half on a success. One creature you choose in the area may spend and roll a Hit Die, "
            "regaining the roll + your Charisma modifier. Upcast: +1d6 damage and +1 Hit Die per slot "
            "level above 2nd."
        ),
        "upcastable": 1,
    },
    # ── Psionic Spells (Always Prepared, use slots) ──────────────────────────
    {
        "name": "Psionic: Arms of Hadar (1st)",
        "spell": "Arms of Hadar",
        "type": "action",
        "description": (
            "Every creature within 10 ft of you (allies too) makes a Strength save: 2d6 Necrotic and no "
            "Reactions until the start of its next turn; half damage only on a success. Always prepared "
            "(Aberrant Sorcery). Upcast: +1d6 per slot level above 1st."
        ),
        "upcastable": 1,
    },
    {
        "name": "Psionic: Calm Emotions (2nd)",
        "spell": "Calm Emotions",
        "type": "action",
        "description": (
            "Each Humanoid in a 20-ft-radius sphere within 60 ft: Charisma save or, your choice per "
            "creature, Immunity to Charmed and Frightened (existing ones suppressed), or Indifferent toward "
            "creatures you choose that it's Hostile to (ends if it or its allies take damage). Always "
            "prepared (Aberrant Sorcery)."
        ),
    },
    {
        "name": "Psionic: Detect Thoughts (2nd)",
        "spell": "Detect Thoughts",
        "type": "action",
        "description": (
            "Sense Thoughts: notice thinking creatures within 30 ft (blocked by 1 ft of stone, dirt, or "
            "wood, 1 inch of metal, or thin lead). Read Thoughts: learn what's on one creature's mind; on "
            "your next turn, a Magic action probes deeper (Wisdom save: on a failure you learn its "
            "reasoning and emotions; on a success the spell ends). Magic action to switch effects. Always "
            "prepared (Aberrant Sorcery)."
        ),
    },
    {
        "name": "Psionic: Dissonant Whispers (1st)",
        "spell": "Dissonant Whispers",
        "type": "action",
        "description": (
            "One creature within 60 ft: Wisdom save or 3d6 Psychic and it must use its Reaction to move "
            "as far from you as it can; half damage only on a success. Always prepared (Aberrant "
            "Sorcery). Upcast: +1d6 per slot level above 1st."
        ),
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
    # Replaced by Maximilian's Earthen Grasp / Wither and Bloom
    conn.execute("DELETE FROM abilities WHERE character_id=? AND name=?", (cid, "Spell: Hold Person (2nd)"))


def _fix_earthen_grasp_spelling(conn, cid):
    # Was "Maximillian's"; renamed so the row keeps its Play state (e.g. active)
    conn.execute(
        "UPDATE abilities SET name=? WHERE character_id=? AND name=?",
        ("Spell: Maximilian's Earthen Grasp (2nd)", cid, "Spell: Maximillian's Earthen Grasp (2nd)"),
    )


STEPS = [
    ("spell-slots-to-columns", _spell_slots_to_columns),
    ("level-4", _level_4),
    ("retire-hold-person", _retire_hold_person),
    ("fix-earthen-grasp-spelling", _fix_earthen_grasp_spelling),
]
