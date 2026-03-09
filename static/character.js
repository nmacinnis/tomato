// Character sheet page logic

let char = null;

async function loadCharacter() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}`);
  if (!res.ok) { alert("Character not found"); return; }
  char = await res.json();
  renderCharacter();
  loadAbilities();
  loadInventory();
}

function profBonus(level) {
  return Math.floor((level - 1) / 4) + 2;
}

function renderCharacter() {
  document.title = char.name;
  document.getElementById("char-name").textContent = char.name;
  document.getElementById("char-subtitle").textContent =
    `${char.race} ${char.class} — Level ${char.level}`;

  const prof = profBonus(char.level);
  const saveProfs = new Set((char.save_proficiencies || "").split(",").map(s => s.trim()).filter(Boolean));

  ["str", "dex", "con", "int", "wis", "cha"].forEach(stat => {
    const box = document.querySelector(`.stat-box[data-stat="${stat}"]`);
    box.querySelector(".stat-val").textContent = char[stat];
    box.querySelector(".stat-mod").textContent = modifier(char[stat]);
    box.onclick = () => editStat(stat);

    const mod = Math.floor((char[stat] - 10) / 2);
    const proficient = saveProfs.has(stat);
    const saveVal = mod + (proficient ? prof : 0);
    const saveEl = box.querySelector(".stat-save");
    saveEl.textContent = `save ${saveVal >= 0 ? "+" : ""}${saveVal}`;
    saveEl.className = "stat-save" + (proficient ? " save-proficient" : "");
  });

  updateHpDisplay();
  document.getElementById("ac-val").textContent = char.ac;
  document.getElementById("speed-val").textContent = `${char.speed} ft`;
  document.getElementById("level-val").textContent = char.level;
  document.getElementById("notes-area").value = char.notes || "";

  // Derived stats
  const dexMod = Math.floor((char.dex - 10) / 2);
  const wisMod = Math.floor((char.wis - 10) / 2);
  document.getElementById("prof-val").textContent = `+${prof}`;
  document.getElementById("init-val").textContent = dexMod >= 0 ? `+${dexMod}` : `${dexMod}`;
  document.getElementById("perc-val").textContent = 10 + wisMod + prof;

  // Hit dice
  updateHdDisplay();

  // Death saves
  renderDeathSaves();

  // Goodberries
  renderTomatoes();
}

// ── Hit Dice ───────────────────────────────────────────────────────────────────

function updateHdDisplay() {
  document.getElementById("hd-display").textContent =
    `${char.hit_dice_remaining} / ${char.level}d10`;
}

document.getElementById("hd-down").onclick = async () => {
  if (char.hit_dice_remaining <= 0) return;
  await patchChar({ hit_dice_remaining: char.hit_dice_remaining - 1 });
  updateHdDisplay();
};

document.getElementById("hd-up").onclick = async () => {
  if (char.hit_dice_remaining >= char.level) return;
  await patchChar({ hit_dice_remaining: char.hit_dice_remaining + 1 });
  updateHdDisplay();
};

// ── Death Saves ────────────────────────────────────────────────────────────────

function renderDeathSaves() {
  ["success", "failure"].forEach(type => {
    const count = type === "success" ? char.death_save_successes : char.death_save_failures;
    document.querySelectorAll(`[data-type="${type}"]`).forEach((pip, i) => {
      pip.classList.toggle("pip-filled", i < count);
    });
  });
}

document.getElementById("ds-successes").addEventListener("click", async (e) => {
  const pip = e.target.closest(".ds-pip");
  if (!pip) return;
  const idx = Number(pip.dataset.idx);
  const current = char.death_save_successes;
  const next = (idx < current) ? idx : idx + 1;
  await patchChar({ death_save_successes: Math.min(3, next) });
  renderDeathSaves();
});

document.getElementById("ds-failures").addEventListener("click", async (e) => {
  const pip = e.target.closest(".ds-pip");
  if (!pip) return;
  const idx = Number(pip.dataset.idx);
  const current = char.death_save_failures;
  const next = (idx < current) ? idx : idx + 1;
  await patchChar({ death_save_failures: Math.min(3, next) });
  renderDeathSaves();
});

document.getElementById("reset-death-saves").onclick = async () => {
  await patchChar({ death_save_successes: 0, death_save_failures: 0 });
  renderDeathSaves();
};

// ── Goodberries ────────────────────────────────────────────────────────────────

function renderTomatoes() {
  const container = document.getElementById("tomato-pips");
  const count = char.goodberries;
  container.innerHTML = "";
  for (let i = 0; i < 10; i++) {
    const btn = document.createElement("button");
    btn.className = "tomato-pip" + (i < count ? " tomato-filled" : "");
    btn.textContent = "🍅";
    btn.title = i < count ? `Eat berry ${i + 1}` : `Add berry ${i + 1}`;
    btn.addEventListener("click", async () => {
      // clicking a filled pip sets count to that index (eating it)
      // clicking an empty pip sets count to that index + 1 (adding up to there)
      const next = i < count ? i : i + 1;
      await patchChar({ goodberries: next });
      renderTomatoes();
      document.getElementById("tomato-count").textContent = char.goodberries;
    });
    container.appendChild(btn);
  }
  document.getElementById("tomato-count").textContent = count;
}

function updateHpDisplay() {
  document.getElementById("hp-display").textContent = `${char.hp} / ${char.max_hp}`;
}

async function patchChar(fields) {
  await fetch(`/api/characters/${CHARACTER_ID}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(fields),
  });
  Object.assign(char, fields);
}

// HP controls
document.getElementById("hp-down").onclick = async () => {
  if (char.hp <= 0) return;
  await patchChar({ hp: char.hp - 1 });
  updateHpDisplay();
};

document.getElementById("hp-up").onclick = async () => {
  if (char.hp >= char.max_hp) return;
  await patchChar({ hp: char.hp + 1 });
  updateHpDisplay();
};

// Notes
document.getElementById("save-notes-btn").onclick = async () => {
  await patchChar({ notes: document.getElementById("notes-area").value });
  document.getElementById("save-notes-btn").textContent = "Saved!";
  setTimeout(() => { document.getElementById("save-notes-btn").textContent = "Save Notes"; }, 1500);
};

// Inline stat edit
function editStat(stat) {
  const box = document.querySelector(`.stat-box[data-stat="${stat}"]`);
  const valEl = box.querySelector(".stat-val");
  const current = char[stat];
  const input = document.createElement("input");
  input.type = "number"; input.min = 1; input.max = 30;
  input.value = current;
  input.style.cssText = "width:3rem;font-size:1.2rem;background:#0f3460;border:1px solid #e94560;color:#e0e0e0;border-radius:4px;text-align:center;";
  valEl.replaceWith(input);
  input.focus();
  const save = async () => {
    const val = Math.min(30, Math.max(1, Number(input.value) || current));
    await patchChar({ [stat]: val });
    input.replaceWith(valEl);
    valEl.textContent = val;
    box.querySelector(".stat-mod").textContent = modifier(val);
  };
  input.onblur = save;
  input.onkeydown = e => { if (e.key === "Enter") save(); if (e.key === "Escape") { input.value = current; input.blur(); } };
}

// ── Rest Buttons ───────────────────────────────────────────────────────────────

async function doRest(type) {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/rest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type }),
  });
  if (!res.ok) return;

  // Reload character data and re-render everything
  const updated = await fetch(`/api/characters/${CHARACTER_ID}`);
  char = await updated.json();
  renderCharacter();
  loadAbilities();  // ability uses_remaining may have changed

  const label = type === "short" ? "Short rest taken." : "Long rest taken — HP, abilities, and hit dice restored.";
  const fb = document.getElementById("rest-feedback");
  fb.textContent = label;
  fb.hidden = false;
  setTimeout(() => { fb.hidden = true; }, 3000);
}

document.getElementById("short-rest-btn").onclick = () => doRest("short");
document.getElementById("long-rest-btn").onclick = async () => {
  if (!confirm("Take a long rest? This will restore HP, all abilities, and recover hit dice.")) return;
  doRest("long");
};

// Delete character
document.getElementById("delete-char-btn").onclick = async () => {
  if (!confirm(`Delete ${char.name}? This cannot be undone.`)) return;
  await fetch(`/api/characters/${CHARACTER_ID}`, { method: "DELETE" });
  window.location.href = "/";
};

// ── Abilities ──────────────────────────────────────────────────────────────────

async function loadAbilities() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/abilities`);
  const abilities = await res.json();
  const list = document.getElementById("abilities-list");
  list.innerHTML = "";
  if (abilities.length === 0) {
    list.innerHTML = `<p style="color:var(--muted);font-size:.85rem">No abilities yet.</p>`;
    return;
  }
  abilities.forEach(a => list.appendChild(renderAbilityCard(a)));
}

const RECHARGE_LABEL = { short: "short rest", long: "long rest" };

function renderAbilityCard(a) {
  const div = document.createElement("div");
  div.className = "ability-card";
  const rem = a.uses_remaining ?? a.uses_max;
  const usesText = a.uses_max != null ? `${rem} / ${a.uses_max}` : "";
  const rechargeBadge = a.recharge
    ? `<span class="recharge-badge recharge-${a.recharge}">${RECHARGE_LABEL[a.recharge]}</span>`
    : "";
  div.innerHTML = `
    <div class="ability-card-header">
      <div>
        <span class="ability-name">${escHtml(a.name)}</span>
        <span class="ability-type">${escHtml(a.type)}</span>
        ${rechargeBadge}
      </div>
      <div class="card-actions">
        ${a.uses_max != null ? `<button class="use-btn" data-id="${a.id}" data-rem="${rem}">Use</button>` : ""}
        <button class="edit-ability-btn" data-id="${a.id}">Edit</button>
        <button class="del-ability-btn" data-id="${a.id}">✕</button>
      </div>
    </div>
    ${a.description ? `<div class="ability-desc">${escHtml(a.description)}</div>` : ""}
    ${usesText ? `<div class="ability-uses">Uses: ${usesText}</div>` : ""}
  `;

  div.querySelector(".edit-ability-btn")?.addEventListener("click", () => openAbilityModal(a));
  div.querySelector(".del-ability-btn")?.addEventListener("click", async () => {
    await fetch(`/api/abilities/${a.id}`, { method: "DELETE" });
    loadAbilities();
  });
  div.querySelector(".use-btn")?.addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    const rem = Number(btn.dataset.rem);
    if (rem <= 0) return;
    const newRem = rem - 1;
    await fetch(`/api/abilities/${a.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ uses_remaining: newRem }),
    });
    btn.dataset.rem = newRem;
    div.querySelector(".ability-uses").textContent = `Uses: ${newRem} / ${a.uses_max}`;
  });

  return div;
}

const abilityModal = document.getElementById("ability-modal");
const abilityForm = document.getElementById("ability-form");

function openAbilityModal(ability = null) {
  abilityForm.reset();
  document.getElementById("ability-modal-title").textContent = ability ? "Edit Ability" : "Add Ability";
  if (ability) {
    abilityForm.id_field = ability.id;
    abilityForm.name.value = ability.name;
    abilityForm.type.value = ability.type;
    abilityForm.description.value = ability.description;
    abilityForm.uses_max.value = ability.uses_max ?? "";
    abilityForm.recharge.value = ability.recharge ?? "";
  } else {
    abilityForm.id_field = null;
  }
  abilityModal.showModal();
}

document.getElementById("add-ability-btn").onclick = () => openAbilityModal();
document.getElementById("cancel-ability").onclick = () => abilityModal.close();

abilityForm.onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(abilityForm);
  const body = Object.fromEntries(fd.entries());
  if (body.uses_max === "") body.uses_max = null;
  else body.uses_max = Number(body.uses_max);
  if (body.recharge === "") body.recharge = null;

  if (abilityForm.id_field) {
    body.uses_remaining = body.uses_max;
    await fetch(`/api/abilities/${abilityForm.id_field}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } else {
    await fetch(`/api/characters/${CHARACTER_ID}/abilities`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  }
  abilityModal.close();
  loadAbilities();
};

// ── Inventory ──────────────────────────────────────────────────────────────────

function calcAC(items) {
  const equipped = items.filter(i => i.equipped);
  const armor = equipped.find(i => i.sets_base_ac);
  const base = armor ? armor.ac_bonus : 10 + Math.floor((char.dex - 10) / 2);
  const bonuses = equipped.reduce((s, i) => s + (i.sets_base_ac ? 0 : (i.ac_bonus || 0)), 0);
  return base + bonuses + (char.flat_ac_bonus || 0);
}

function acBreakdown(items) {
  const equipped = items.filter(i => i.equipped && i.ac_bonus);
  const armor = equipped.find(i => i.sets_base_ac);
  const parts = [];
  if (armor) parts.push(`${armor.ac_bonus} (${armor.name})`);
  else parts.push(`${10 + Math.floor((char.dex - 10) / 2)} (unarmored)`);
  equipped.filter(i => !i.sets_base_ac).forEach(i => parts.push(`+${i.ac_bonus} (${i.name})`));
  if (char.flat_ac_bonus) parts.push(`+${char.flat_ac_bonus} (misc)`);
  return parts.join(" ");
}

async function loadInventory() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/inventory`);
  const items = await res.json();
  const list = document.getElementById("inventory-list");
  list.innerHTML = "";
  if (items.length === 0) {
    list.innerHTML = `<p style="color:var(--muted);font-size:.85rem">No items yet.</p>`;
    document.getElementById("weight-total").textContent = "";
  } else {
    items.sort((a, b) => b.equipped - a.equipped || a.name.localeCompare(b.name));
    items.forEach(i => list.appendChild(renderItemCard(i)));
    const total = items.reduce((s, i) => s + i.weight * i.quantity, 0);
    document.getElementById("weight-total").textContent = `Total weight: ${total.toFixed(1)} lbs`;
  }

  // Recompute and display AC
  const ac = calcAC(items);
  document.getElementById("ac-val").textContent = ac;
  document.getElementById("ac-breakdown").textContent = acBreakdown(items);
  if (ac !== char.ac) {
    char.ac = ac;
    fetch(`/api/characters/${CHARACTER_ID}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ac }),
    });
  }
}

function renderItemCard(item) {
  const div = document.createElement("div");
  div.className = "item-card";
  div.innerHTML = `
    <div class="item-card-header">
      <span class="item-name">${escHtml(item.name)}</span>
      <div class="card-actions">
        <button class="equip-btn ${item.equipped ? "is-equipped" : ""}" data-id="${item.id}">${item.equipped ? "Equipped" : "Equip"}</button>
        <button class="edit-item-btn" data-id="${item.id}">Edit</button>
        <button class="del-item-btn" data-id="${item.id}">✕</button>
      </div>
    </div>
    <div class="item-meta">
      <span>Qty: ${item.quantity}</span>
      <span>${item.weight} lbs ea.</span>
    </div>
    ${item.description ? `<div class="item-desc">${escHtml(item.description)}</div>` : ""}
  `;

  div.querySelector(".equip-btn").addEventListener("click", async () => {
    await fetch(`/api/inventory/${item.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ equipped: !item.equipped }),
    });
    loadInventory();
  });
  div.querySelector(".edit-item-btn").addEventListener("click", () => openItemModal(item));
  div.querySelector(".del-item-btn").addEventListener("click", async () => {
    await fetch(`/api/inventory/${item.id}`, { method: "DELETE" });
    loadInventory();
  });
  return div;
}

const itemModal = document.getElementById("item-modal");
const itemForm = document.getElementById("item-form");

function openItemModal(item = null) {
  itemForm.reset();
  document.getElementById("item-modal-title").textContent = item ? "Edit Item" : "Add Item";
  if (item) {
    itemForm.id_field = item.id;
    itemForm.name.value = item.name;
    itemForm.quantity.value = item.quantity;
    itemForm.weight.value = item.weight;
    itemForm.description.value = item.description;
    itemForm.ac_bonus.value = item.ac_bonus || 0;
    itemForm.sets_base_ac.checked = !!item.sets_base_ac;
    itemForm.equipped.checked = !!item.equipped;
  } else {
    itemForm.id_field = null;
  }
  itemModal.showModal();
}

document.getElementById("add-item-btn").onclick = () => openItemModal();
document.getElementById("cancel-item").onclick = () => itemModal.close();

itemForm.onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(itemForm);
  const body = Object.fromEntries(fd.entries());
  body.quantity = Number(body.quantity);
  body.weight = Number(body.weight);
  body.ac_bonus = Number(body.ac_bonus) || 0;
  body.sets_base_ac = !!body.sets_base_ac;
  body.equipped = !!body.equipped;

  if (itemForm.id_field) {
    await fetch(`/api/inventory/${itemForm.id_field}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } else {
    await fetch(`/api/characters/${CHARACTER_ID}/inventory`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  }
  itemModal.close();
  loadInventory();
};

// ── Boot ───────────────────────────────────────────────────────────────────────
loadCharacter();
