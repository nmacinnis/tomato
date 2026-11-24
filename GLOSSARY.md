# DnD Character Tracker

Tracks D&D 5e characters through play: their fixed build and the state that changes at the table.

## Language

**Character**:
A player character tracked by the app, together with its abilities and inventory.

**Sheet**:
The authored definition of a Character's build: race, class, level, ability scores, maximums, descriptions, weapon and spell details. Authored in code; the code's version wins.
_Avoid_: seed data, template

**Play state**:
Everything about a Character that changes during a session: current HP, hit dice, coins, uses remaining, spell slots remaining, active spells, equipped items, quantities, session notes. Set once when the Character is created, then owned by the table.
_Avoid_: runtime data, current stats

**Seeding**:
Bringing a Character in the database up to date with its Sheet without disturbing its Play state.
_Avoid_: apply, sync, migration

**Seed step**:
A named, one-time change to an existing Character that the Sheet alone can't express: a level-up's HP gain, a renamed or retired ability. Runs at most once per database.
_Avoid_: migration, patch, transition
