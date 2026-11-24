# DnD Character Tracker

Tracks D&D 5e characters through play: their fixed build and the state that changes at the table.

## Language

**Character**:
A player character tracked by the app, together with its abilities and inventory.

**Sheet**:
The authored definition of a Character's build at each of its levels: race, class, ability scores, maximums, descriptions, weapon and spell details. Authored in code; the code's version wins.
_Avoid_: seed data, template

**Rules text**:
A spell's published wording, word-for-word, together with the book it comes from. The same for every Character who has the spell; never carries notes about a particular Character. The app keeps the wording itself only for spells in the SRD 5.2 (openly licensed); for any other spell it links to where the wording can be read.
_Avoid_: full description, spell text

**Summary**:
The Sheet's short, table-ready version of an ability: the mechanics that matter in play, plus any notes specific to this Character. Paraphrase, never quoted as rules.
_Avoid_: short description, blurb

**Level**:
How far a Character has advanced. Part of Play state; it selects which level of the Sheet applies.

**Play state**:
Everything about a Character that changes during a session: level, current HP, hit dice, coins, uses remaining, spell slots remaining, active spells, equipped items, quantities, session notes. Set once when the Character is created, then owned by the table.
_Avoid_: runtime data, current stats

**Level-up**:
Moving a Character to the next level its Sheet describes, chosen at the table. Each Play state counter rises by however much its maximum rose; it is not a rest.

**Snapshot**:
A dated copy of a Character's Play state (except session notes) and of which abilities and items it has, which can later be restored. Taken by hand, or automatically before a restore or a Level-up.
_Avoid_: save, checkpoint, backup

**Player-added**:
An ability or item added at the table rather than described by the Sheet. If the Sheet later describes it by name, the Sheet takes it over.
_Avoid_: manual, custom, homebrew

**Seeding**:
Bringing a Character in the database up to date with its Sheet without disturbing its Play state.
_Avoid_: apply, sync, migration

**Seed step**:
A named, one-time change to an existing Character that the Sheet alone can't express, such as a renamed or retired ability. Runs at most once per database.
_Avoid_: migration, patch, transition

## Flagged ambiguities

- "Save" means a saving throw (death saves, save bonuses). Never use it for a Snapshot.
