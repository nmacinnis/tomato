// Entry point — loads character data and kicks off the full render.
// State and helpers live in character-utils.js; sections in character-*.js files.

async function loadCharacter() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}`);
  if (!res.ok) { alert("Character not found"); return; }
  char = await res.json();
  renderCharacter();
  await loadInventory();  // populates currentItems, then calls loadAbilities
}

loadCharacter();
