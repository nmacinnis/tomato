// Inventory panel — AC calculation, item rendering, and modal.

function calcAC(items) {
  const equipped = items.filter((i) => i.equipped);
  const armor = equipped.find((i) => i.sets_base_ac);
  const base = armor ? armor.ac_bonus : 10 + Math.floor((char.dex - 10) / 2);
  const bonuses = equipped.reduce(
    (s, i) => s + (i.sets_base_ac ? 0 : i.ac_bonus || 0),
    0
  );
  return base + bonuses + (char.flat_ac_bonus || 0) + abilityAcBonus;
}

function acBreakdownParts(items) {
  const equipped = items.filter((i) => i.equipped && i.ac_bonus);
  const armor = equipped.find((i) => i.sets_base_ac);
  const parts = [];
  if (armor)
    parts.push({
      value: armor.ac_bonus,
      label: armor.name,
      type: "item",
      id: armor.id,
    });
  else
    parts.push({
      value: 10 + Math.floor((char.dex - 10) / 2),
      label: "unarmored",
      type: null,
    });
  equipped
    .filter((i) => !i.sets_base_ac)
    .forEach((i) =>
      parts.push({ value: i.ac_bonus, label: i.name, type: "item", id: i.id })
    );
  abilityAcBreakdown.forEach((p) =>
    parts.push({ value: p.ac_bonus, label: p.name, type: "ability", id: p.id })
  );
  if (char.flat_ac_bonus)
    parts.push({ value: char.flat_ac_bonus, label: "misc", type: null });
  return parts;
}

function updateAcDisplay() {
  const ac = calcAC(currentItems);
  document.getElementById("ac-val").textContent = ac;
  char.ac = ac;

  const parts = acBreakdownParts(currentItems);
  const equation =
    parts.map((p, i) => (i === 0 ? p.value : `+ ${p.value}`)).join(" ") + ` = ${ac}`;
  const detail = parts
    .map((p) => {
      const text = `${p.value} (${p.label})`;
      return p.type
        ? `<button class="ac-link" data-type="${p.type}" data-id="${p.id}">${escHtml(text)}</button>`
        : escHtml(text);
    })
    .join(" ");

  const bd = document.getElementById("ac-breakdown");
  bd.innerHTML = `<span class="ac-equation">${escHtml(equation)}</span><span class="ac-detail" hidden>${detail}</span>`;
  bd.onclick = (e) => {
    const link = e.target.closest(".ac-link");
    if (link) {
      const { type, id } = link.dataset;
      const sel =
        type === "item"
          ? `.del-item-btn[data-id="${id}"]`
          : `.del-ability-btn[data-id="${id}"]`;
      const card = document
        .querySelector(sel)
        ?.closest(type === "item" ? ".item-card" : ".ability-card");
      if (card) {
        card.scrollIntoView({ behavior: "smooth", block: "nearest" });
        card.classList.add("ac-highlight");
        setTimeout(() => card.classList.remove("ac-highlight"), 1200);
      }
      return;
    }
    bd.querySelector(".ac-equation").hidden ^= true;
    bd.querySelector(".ac-detail").hidden ^= true;
  };
}

// ── Load inventory ───────────────────────────────────────────────────────────

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
    items.forEach((i) => list.appendChild(renderItemCard(i)));
    const total = items.reduce((s, i) => s + i.weight * i.quantity, 0);
    document.getElementById("weight-total").textContent =
      `Total weight: ${total.toFixed(1)} lbs`;
  }

  currentItems = items;
  itemSaveParts = items
    .filter((i) => i.equipped && i.save_bonus)
    .map((i) => ({ type: "item", id: i.id, name: i.name, save_bonus: i.save_bonus }));
  renderSkills();
  await loadAbilities(); // computes abilityAcBonus/abilitySaveParts, then calls updateAcDisplay + renderSaves
}

// ── Item card ────────────────────────────────────────────────────────────────

function renderItemCard(item) {
  const div = document.createElement("div");
  div.className = "item-card";
  div.innerHTML = `
    <div class="item-card-header">
      <span class="item-name">${escHtml(item.name)}</span>
      <div class="card-actions">
        <button class="equip-btn ${item.equipped ? "is-equipped" : ""}" data-id="${item.id}">${item.equipped ? "Equipped" : "Equip"}</button>
        <button class="edit-item-btn" data-id="${item.id}">Edit</button>
        <button class="del-item-btn"  data-id="${item.id}">✕</button>
      </div>
    </div>
    <div class="item-meta">
      <span>Qty: ${item.quantity}</span>
      <span>${item.weight} lbs ea.</span>
    </div>
    ${item.description ? `<div class="item-desc">${escHtml(item.description)}</div>` : ""}
    ${item.flavor ? `<div class="item-flavor">${escHtml(item.flavor)}</div>` : ""}
  `;

  div.querySelector(".equip-btn").addEventListener("click", async () => {
    const res = await apiFetch(
      `/api/inventory/${item.id}`,
      { method: "PUT", body: { equipped: !item.equipped } },
      "Failed to update item."
    );
    if (!res) return;
    loadInventory();
  });

  div
    .querySelector(".edit-item-btn")
    .addEventListener("click", () => openItemModal(item));

  div.querySelector(".del-item-btn").addEventListener("click", async () => {
    const res = await apiFetch(
      `/api/inventory/${item.id}`,
      { method: "DELETE" },
      "Failed to delete item."
    );
    if (!res) return;
    loadInventory();
  });

  return div;
}

// ── Item modal ───────────────────────────────────────────────────────────────

const itemModal = document.getElementById("item-modal");
const itemForm = document.getElementById("item-form");

function openItemModal(item = null) {
  itemForm.reset();
  document.getElementById("item-modal-title").textContent = item
    ? "Edit Item"
    : "Add Item";
  if (item) {
    itemForm.id_field = item.id;
    itemForm.name.value = item.name;
    itemForm.quantity.value = item.quantity;
    itemForm.weight.value = item.weight;
    itemForm.description.value = item.description;
    itemForm.ac_bonus.value = item.ac_bonus || 0;
    itemForm.save_bonus.value = item.save_bonus || 0;
    itemForm.sets_base_ac.checked = !!item.sets_base_ac;
    itemForm.is_weapon.checked = !!item.is_weapon;
    document.getElementById("weapon-fields").hidden = !item.is_weapon;
    itemForm.damage_dice.value = item.damage_dice || "";
    itemForm.damage_type.value = item.damage_type || "";
    itemForm.magic_bonus.value = item.magic_bonus || 0;
    itemForm.is_melee.checked = item.is_melee !== 0;
    itemForm.damage_notes.value = item.damage_notes || "";
    itemForm.flavor.value = item.flavor || "";
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
  body.save_bonus = Number(body.save_bonus) || 0;
  body.sets_base_ac = !!body.sets_base_ac;
  body.is_weapon = !!body.is_weapon;
  body.magic_bonus = Number(body.magic_bonus) || 0;
  body.is_melee = !!body.is_melee;
  body.equipped = !!body.equipped;

  if (itemForm.id_field) {
    const res = await apiFetch(
      `/api/inventory/${itemForm.id_field}`,
      { method: "PUT", body },
      "Failed to update item."
    );
    if (!res) return;
  } else {
    const res = await apiFetch(
      `/api/characters/${CHARACTER_ID}/inventory`,
      { method: "POST", body },
      "Failed to add item."
    );
    if (!res) return;
  }
  itemModal.close();
  loadInventory();
};
