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

function renderCharacter() {
  document.title = char.name;
  document.getElementById("char-name").textContent = char.name;
  document.getElementById("char-subtitle").textContent =
    `${char.race} ${char.class} — Level ${char.level}`;

  ["str", "dex", "con", "int", "wis", "cha"].forEach(stat => {
    const box = document.querySelector(`.stat-box[data-stat="${stat}"]`);
    box.querySelector(".stat-val").textContent = char[stat];
    box.querySelector(".stat-mod").textContent = modifier(char[stat]);
    box.onclick = () => editStat(stat);
  });

  updateHpDisplay();
  document.getElementById("ac-val").textContent = char.ac;
  document.getElementById("speed-val").textContent = `${char.speed} ft`;
  document.getElementById("level-val").textContent = char.level;
  document.getElementById("notes-area").value = char.notes || "";
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

function renderAbilityCard(a) {
  const div = document.createElement("div");
  div.className = "ability-card";
  const usesText = a.uses_max != null
    ? `Uses: ${a.uses_remaining ?? a.uses_max} / ${a.uses_max}`
    : "";
  div.innerHTML = `
    <div class="ability-card-header">
      <div>
        <span class="ability-name">${escHtml(a.name)}</span>
        <span class="ability-type">${escHtml(a.type)}</span>
      </div>
      <div class="card-actions">
        ${a.uses_max != null ? `<button class="use-btn" data-id="${a.id}" data-rem="${a.uses_remaining ?? a.uses_max}">Use</button>` : ""}
        <button class="edit-ability-btn" data-id="${a.id}">Edit</button>
        <button class="del-ability-btn" data-id="${a.id}">✕</button>
      </div>
    </div>
    ${a.description ? `<div class="ability-desc">${escHtml(a.description)}</div>` : ""}
    ${usesText ? `<div class="ability-uses">${usesText}</div>` : ""}
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

async function loadInventory() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/inventory`);
  const items = await res.json();
  const list = document.getElementById("inventory-list");
  list.innerHTML = "";
  if (items.length === 0) {
    list.innerHTML = `<p style="color:var(--muted);font-size:.85rem">No items yet.</p>`;
    document.getElementById("weight-total").textContent = "";
    return;
  }
  items.forEach(i => list.appendChild(renderItemCard(i)));
  const total = items.reduce((s, i) => s + i.weight * i.quantity, 0);
  document.getElementById("weight-total").textContent = `Total weight: ${total.toFixed(1)} lbs`;
}

function renderItemCard(item) {
  const div = document.createElement("div");
  div.className = "item-card";
  div.innerHTML = `
    <div class="item-card-header">
      <span class="item-name">${escHtml(item.name)}${item.equipped ? ' <span class="equipped-badge">[equipped]</span>' : ""}</span>
      <div class="card-actions">
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
