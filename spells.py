"""The shared spell list: each spell's Rules text (or a link to it) and card details.

Card details and source come from 5e.tools: the 2024 Player's Handbook where the spell is
in it, otherwise the newest book that has it. A Sheet names a spell with
`"spell": "<name>"` on an ability; Seeding fills in the fields below from here.

Rules text is stored word-for-word only for spells in the SRD 5.2, which Wizards of the
Coast released under CC-BY-4.0 (attribution is on the character page). Every other spell's
wording is copyrighted, so it has a `rules_url` to its 5e.tools page instead of a
`rules_text`; don't paste its text here. Never add notes about a particular Character to
a Rules text: those go in the Sheet's Summary (`description`). See GLOSSARY.md.

Rules text uses a small markdown subset: blank-line paragraphs, `- ` list items, **bold**.
"""

SPELLS = {
    "Arms of Hadar": {
        "rules_source": "PHB 2024, p. 243",
        "spell_level": 1,
        "spell_range": "Self (10-foot Emanation)",
        "components": "V, S",
        "duration": "Instantaneous",
        "concentration": 0,
        "rules_url": "https://5e.tools/spells.html#arms%20of%20hadar_xphb",
    },
    "Calm Emotions": {
        "rules_source": "PHB 2024, p. 249 · SRD 5.2",
        "spell_level": 2,
        "spell_range": "60 feet",
        "components": "V, S",
        "duration": "1 minute",
        "concentration": 1,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "Each Humanoid in a 20-foot-radius Sphere centered on a point you choose within range "
            "must succeed on a Charisma saving throw or be affected by one of the following effects "
            "(choose for each creature):\n"
            "\n"
            "- The creature has Immunity to the Charmed and Frightened conditions until the spell "
            "ends. If the creature was already Charmed or Frightened, those conditions are suppressed"
            " for the duration.\n"
            "- The creature becomes Indifferent about creatures of your choice that it's Hostile "
            "toward. This indifference ends if the target takes damage or witnesses its allies taking"
            " damage. When the spell ends, the creature's attitude returns to normal."
        ),
    },
    "Catapult": {
        "rules_source": "Xanathar's Guide to Everything, p. 150",
        "spell_level": 1,
        "spell_range": "60 feet",
        "components": "S",
        "duration": "Instantaneous",
        "concentration": 0,
        "rules_url": "https://5e.tools/spells.html#catapult_xge",
    },
    "Charm Person": {
        "rules_source": "PHB 2024, p. 249 · SRD 5.2",
        "spell_level": 1,
        "spell_range": "30 feet",
        "components": "V, S",
        "duration": "1 hour",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "One Humanoid you can see within range makes a Wisdom saving throw. It does so with "
            "Advantage if you or your allies are fighting it. On a failed save, the target has the "
            "Charmed condition until the spell ends or until you or your allies damage it. The "
            "Charmed creature is Friendly to you. When the spell ends, the target knows it was "
            "Charmed by you.\n"
            "\n"
            "**Using a Higher-Level Spell Slot.** You can target one additional creature for each "
            "spell slot level above 1."
        ),
    },
    "Detect Thoughts": {
        "rules_source": "PHB 2024, p. 262 · SRD 5.2",
        "spell_level": 2,
        "spell_range": "Self",
        "components": "V, S, M (1 Copper Piece)",
        "duration": "1 minute",
        "concentration": 1,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "You activate one of the effects below. Until the spell ends, you can activate either "
            "effect as a Magic action on your later turns.\n"
            "\n"
            "**Sense Thoughts.** You sense the presence of thoughts within 30 feet of yourself that "
            "belong to creatures that know languages or are telepathic. You don't read the thoughts, "
            "but you know that a thinking creature is present.\n"
            "\n"
            "The spell is blocked by 1 foot of stone, dirt, or wood; 1 inch of metal; or a thin sheet"
            " of lead.\n"
            "\n"
            "**Read Thoughts.** Target one creature you can see within 30 feet of yourself or one "
            "creature within 30 feet of yourself that you detected with the Sense Thoughts option. "
            "You learn what is most on the target's mind right now. If the target doesn't know any "
            "languages and isn't telepathic, you learn nothing.\n"
            "\n"
            "As a Magic action on your next turn, you can try to probe deeper into the target's mind."
            " If you probe deeper, the target makes a Wisdom saving throw. On a failed save, you "
            "discern the target's reasoning, emotions, and something that looms large in its mind "
            "(such as a worry, love, or hate). On a successful save, the spell ends. Either way, the "
            "target knows that you are probing into its mind, and until you shift your attention away"
            " from the target's mind, the target can take an action on its turn to make an "
            "Intelligence (Arcana) check against your spell save DC, ending the spell on a success."
        ),
    },
    "Dissonant Whispers": {
        "rules_source": "PHB 2024, p. 264 · SRD 5.2",
        "spell_level": 1,
        "spell_range": "60 feet",
        "components": "V",
        "duration": "Instantaneous",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "One creature of your choice that you can see within range hears a discordant melody in "
            "its mind. The target makes a Wisdom saving throw. On a failed save, it takes 3d6 Psychic"
            " damage and must immediately use its Reaction, if available, to move as far away from "
            "you as it can, using the safest route. On a successful save, the target takes half as "
            "much damage only.\n"
            "\n"
            "**Using a Higher-Level Spell Slot.** The damage increases by 1d6 for each spell slot "
            "level above 1."
        ),
    },
    "Druidcraft": {
        "rules_source": "PHB 2024, p. 266 · SRD 5.2",
        "spell_level": 0,
        "spell_range": "30 feet",
        "components": "V, S",
        "duration": "Instantaneous",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "Whispering to the spirits of nature, you create one of the following effects within "
            "range.\n"
            "\n"
            "**Weather Sensor.** You create a Tiny, harmless sensory effect that predicts what the "
            "weather will be at your location for the next 24 hours. The effect might manifest as a "
            "golden orb for clear skies, a cloud for rain, falling snowflakes for snow, and so on. "
            "This effect persists for 1 round.\n"
            "\n"
            "**Bloom.** You instantly make a flower blossom, a seed pod open, or a leaf bud bloom.\n"
            "\n"
            "**Sensory Effect.** You create a harmless sensory effect, such as falling leaves, "
            "spectral dancing fairies, a gentle breeze, the sound of an animal, or the faint odor of "
            "skunk. The effect must fit in a 5-foot Cube.\n"
            "\n"
            "**Fire Play.** You light or snuff out a candle, a torch, or a campfire."
        ),
    },
    "Friends": {
        "rules_source": "PHB 2024, p. 277",
        "spell_level": 0,
        "spell_range": "10 feet",
        "components": "S, M (some makeup)",
        "duration": "1 minute",
        "concentration": 1,
        "rules_url": "https://5e.tools/spells.html#friends_xphb",
    },
    "Goodberry": {
        "rules_source": "PHB 2024, p. 280 · SRD 5.2",
        "spell_level": 1,
        "spell_range": "Touch",
        "components": "V, S, M (a sprig of mistletoe)",
        "duration": "24 hours",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "Ten berries appear in your hand and are infused with magic for the duration. A creature "
            "can take a Bonus Action to eat one berry. Eating a berry restores 1 Hit Point, and the "
            "berry provides enough nourishment to sustain a creature for one day.\n"
            "\n"
            "Uneaten berries disappear when the spell ends."
        ),
    },
    "Guidance": {
        "rules_source": "PHB 2024, p. 282 · SRD 5.2",
        "spell_level": 0,
        "spell_range": "Touch",
        "components": "V, S",
        "duration": "1 minute",
        "concentration": 1,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "You touch a willing creature and choose a skill. Until the spell ends, the creature adds"
            " 1d4 to any ability check using the chosen skill."
        ),
    },
    "Levitate": {
        "rules_source": "PHB 2024, p. 291 · SRD 5.2",
        "spell_level": 2,
        "spell_range": "60 feet",
        "components": "V, S, M (a metal spring)",
        "duration": "10 minutes",
        "concentration": 1,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "One creature or loose object of your choice that you can see within range rises "
            "vertically up to 20 feet and remains suspended there for the duration. The spell can "
            "levitate an object that weighs up to 500 pounds. An unwilling creature that succeeds on "
            "a Constitution saving throw is unaffected.\n"
            "\n"
            "The target can move only by pushing or pulling against a fixed object or surface within "
            "reach (such as a wall or a ceiling), which allows it to move as if it were climbing. You"
            " can change the target's altitude by up to 20 feet in either direction on your turn. If "
            "you are the target, you can move up or down as part of your move. Otherwise, you can "
            "take a Magic action to move the target, which must remain within the spell's range.\n"
            "\n"
            "When the spell ends, the target floats gently to the ground if it is still aloft."
        ),
    },
    "Mage Armor": {
        "rules_source": "PHB 2024, p. 293 · SRD 5.2",
        "spell_level": 1,
        "spell_range": "Touch",
        "components": "V, S, M (a piece of cured leather)",
        "duration": "8 hours",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "You touch a willing creature who isn't wearing armor. Until the spell ends, the target's"
            " base AC becomes 13 plus its Dexterity modifier. The spell ends early if the target dons"
            " armor."
        ),
    },
    "Mage Hand": {
        "rules_source": "PHB 2024, p. 293 · SRD 5.2",
        "spell_level": 0,
        "spell_range": "30 feet",
        "components": "V, S",
        "duration": "1 minute",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "A spectral, floating hand appears at a point you choose within range. The hand lasts for"
            " the duration. The hand vanishes if it is ever more than 30 feet away from you or if you"
            " cast this spell again.\n"
            "\n"
            "When you cast the spell, you can use the hand to manipulate an object, open an unlocked "
            "door or container, stow or retrieve an item from an open container, or pour the contents"
            " out of a vial.\n"
            "\n"
            "As a Magic action on your later turns, you can control the hand thus again. As part of "
            "that action, you can move the hand up to 30 feet.\n"
            "\n"
            "The hand can't attack, activate magic items, or carry more than 10 pounds."
        ),
    },
    "Maximilian's Earthen Grasp": {
        "rules_source": "Xanathar's Guide to Everything, p. 161",
        "spell_level": 2,
        "spell_range": "30 feet",
        "components": "V, S, M (a miniature hand sculpted from clay)",
        "duration": "1 minute",
        "concentration": 1,
        "rules_url": "https://5e.tools/spells.html#maximilian's%20earthen%20grasp_xge",
    },
    "Message": {
        "rules_source": "PHB 2024, p. 298 · SRD 5.2",
        "spell_level": 0,
        "spell_range": "120 feet",
        "components": "S, M (a copper wire)",
        "duration": "1 round",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "You point toward a creature within range and whisper a message. The target (and only the"
            " target) hears the message and can reply in a whisper that only you can hear.\n"
            "\n"
            "You can cast this spell through solid objects if you are familiar with the target and "
            "know it is beyond the barrier. Magical silence; 1 foot of stone, metal, or wood; or a "
            "thin sheet of lead blocks the spell."
        ),
    },
    "Mind Sliver": {
        "rules_source": "PHB 2024, p. 298",
        "spell_level": 0,
        "spell_range": "60 feet",
        "components": "V",
        "duration": "Instantaneous",
        "concentration": 0,
        "rules_url": "https://5e.tools/spells.html#mind%20sliver_xphb",
    },
    "Prestidigitation": {
        "rules_source": "PHB 2024, p. 307 · SRD 5.2",
        "spell_level": 0,
        "spell_range": "10 feet",
        "components": "V, S",
        "duration": "1 hour",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "You create a magical effect within range. Choose the effect from the options below. If "
            "you cast this spell multiple times, you can have up to three of its non-instantaneous "
            "effects active at a time.\n"
            "\n"
            "**Sensory Effect.** You create an instantaneous, harmless sensory effect, such as a "
            "shower of sparks, a puff of wind, faint musical notes, or an odd odor.\n"
            "\n"
            "**Fire Play.** You instantaneously light or snuff out a candle, a torch, or a small "
            "campfire.\n"
            "\n"
            "**Clean or Soil.** You instantaneously clean or soil an object no larger than 1 cubic "
            "foot.\n"
            "\n"
            "**Minor Sensation.** You chill, warm, or flavor up to 1 cubic foot of nonliving material"
            " for 1 hour.\n"
            "\n"
            "**Magic Mark.** You make a color, a small mark, or a symbol appear on an object or a "
            "surface for 1 hour.\n"
            "\n"
            "**Minor Creation.** You create a nonmagical trinket or an illusory image that can fit in"
            " your hand. It lasts until the end of your next turn. A trinket can deal no damage and "
            "has no monetary worth."
        ),
    },
    "Shield": {
        "rules_source": "PHB 2024, p. 316 · SRD 5.2",
        "spell_level": 1,
        "spell_range": "Self",
        "components": "V, S",
        "duration": "1 round",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Reaction, which you take when you are hit by an attack roll or "
            "targeted by the Magic Missile spell\n"
            "\n"
            "An imperceptible barrier of magical force protects you. Until the start of your next "
            "turn, you have a +5 bonus to AC, including against the triggering attack, and you take "
            "no damage from Magic Missile."
        ),
    },
    "Sorcerous Burst": {
        "rules_source": "PHB 2024, p. 318 · SRD 5.2",
        "spell_level": 0,
        "spell_range": "120 feet",
        "components": "V, S",
        "duration": "Instantaneous",
        "concentration": 0,
        "rules_text": (
            "**Casting Time:** Action\n"
            "\n"
            "You cast sorcerous energy at one creature or object within range. Make a ranged spell "
            "attack against the target. On a hit, the target takes 1d8 damage of a type you choose: "
            "Acid, Cold, Fire, Lightning, Poison, Psychic, or Thunder.\n"
            "\n"
            "If you roll an 8 on a d8 for this spell, you can roll another d8, and add it to the "
            "damage. When you cast this spell, the maximum number of these d8s you can add to the "
            "spell's damage equals your spellcasting ability modifier.\n"
            "\n"
            "**Cantrip Upgrade.** The damage increases by 1d8 when you reach levels 5 (2d8), 11 "
            "(3d8), and 17 (4d8)."
        ),
    },
    "Wither and Bloom": {
        "rules_source": "Strixhaven: A Curriculum of Chaos, p. 38",
        "spell_level": 2,
        "spell_range": "60 feet",
        "components": "V, S, M (a withered vine twisted into a loop)",
        "duration": "Instantaneous",
        "concentration": 0,
        "rules_url": "https://5e.tools/spells.html#wither%20and%20bloom_scc",
    },
}
