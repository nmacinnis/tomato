# Level is Play state; the Sheet describes every level

Level-ups happen at the table, mid-session, and must be undoable by restoring a Snapshot taken before them. So a Character's current level is Play state, and its Sheet describes each level as a base plus a block of changes per later level (`LEVELS`). The Sheet that applies is the Sheet at the current level. Level-ups no longer go through Seed steps.

## Considered Options

- **Level as a Sheet field, level-ups as Seed steps** (the previous model): code decides when a level-up lands (next boot), not the table, and a Seed step can't be undone, so restoring a pre-level-up Snapshot would leave a level 3 Character under a level 4 Sheet.
- **One queued "pending level-up" in code, applied by a button**: simpler at first, but once applied the previous level's Sheet no longer exists anywhere, so restoring to before the level-up has nothing to restore to.
- **Freeform level-up form in the UI**: breaks "the Sheet is authored in code".

## Consequences

- Restoring a Snapshot restores its level, then reseeds at that level: abilities the later level retired come back, and abilities it added go away.
- Seeding only ensures the rows the Sheet describes at the current level; retired rows are deleted at Level-up rather than hidden.
- Existing Characters take their current Sheet as the base level. Levels below the base aren't described, which is fine because no Snapshot can predate this decision.
