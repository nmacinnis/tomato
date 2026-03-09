// Abilities panel — loading, rendering, superiority dice, and modal.

const ABILITY_GROUPS = [
  { key: "action",       label: "Action" },
  { key: "bonus_action", label: "Bonus Action" },
  { key: "reaction",     label: "Reaction" },
  { key: "free_action",  label: "Free Action" },
  { key: "passive",      label: "Passive" },
];

const STANDARD_ACTIONS = [
  { name: "Dash",       desc: "Double your speed this turn." },
  { name: "Disengage",  desc: "Your movement doesn't provoke opportunity attacks for the rest of the turn." },
  { name: "Dodge",      desc: "Until the start of your next turn, attacks against you have Disadvantage and you have Advantage on DEX saves." },
  { name: "Help",       desc: "Give an ally Advantage on their next ability check or attack roll." },
  { name: "Hide",       desc: "Make a Stealth check to become hidden." },
  { name: "Ready",      desc: "Prepare a reaction to trigger on a specified condition before your next turn." },
  { name: "Search",     desc: "Make a Perception or Investigation check to locate something." },
];

const RECHARGE_LABEL = { short: "short rest", long: "long rest" };

// Map legacy type values to display groups
function normalizeType(type) {
  if (type === "active" || type === "spell") return "action";
  return type;
}

// ── Standard Actions ─────────────────────────────────────────────────────────

function renderStandardActions(list, items) {
  const weapons = items.filter(i => i.is_weapon && i.equipped && i.damage_dice);
  const prof = profBonus(char.level);
  const strMod = Math.floor((char.str - 10) / 2);
  const dexMod = Math.floor((char.dex - 10) / 2);

  const attackCard = document.createElement("div");
  attackCard.className = "ability-card standard-action-card";

  let weaponRows = "";
  if (weapons.length === 0) {
    weaponRows = `<div class="attack-weapon-row muted">No weapons equipped.</div>`;
  } else {
    weapons.forEach(w => {
      const abilMod = w.is_melee ? strMod : dexMod;
      const toHit = abilMod + prof + w.magic_bonus;
      const dmgBonus = abilMod + w.magic_bonus;
      const sign = dmgBonus >= 0 ? "+" : "";
      weaponRows += `
        <div class="attack-weapon-row">
          <span class="attack-weapon-name">${escHtml(w.name)}</span>
          <span class="attack-tohit">To-hit: ${toHit >= 0 ? "+" : ""}${toHit}</span>
          <span class="attack-dmg">${w.damage_dice}${sign}${dmgBonus} ${escHtml(w.damage_type)}</span>
          ${w.damage_notes ? `<span class="attack-notes">${escHtml(w.damage_notes)}</span>` : ""}
        </div>`;
    });
  }

  attackCard.innerHTML = `
    <div class="ability-card-header">
      <span class="ability-name">Attack</span>
      <span class="standard-action-note">Extra Attack: 2 per action</span>
    </div>
    <div class="attack-weapons">${weaponRows}</div>
  `;
  list.appendChild(attackCard);

  STANDARD_ACTIONS.forEach(({ name, desc }) => {
    const card = document.createElement("div");
    card.className = "ability-card standard-action-card";
    card.innerHTML = `
      <div class="ability-card-header">
        <span class="ability-name">${name}</span>
      </div>
      <div class="ability-desc">${desc}</div>
    `;
    list.appendChild(card);
  });
}

// ── Superiority Dice ─────────────────────────────────────────────────────────

function updateSdDisplay() {
  if (!superiorityDie) return;
  document.getElementById("sd-display").textContent =
    `${superiorityDie.uses_remaining} / ${superiorityDie.uses_max}`;
}

async function patchSuperiorityDie(uses_remaining) {
  const res = await apiFetch(
    `/api/abilities/${superiorityDie.id}`,
    { method: "PUT", body: { uses_remaining } },
    "Failed to update superiority dice."
  );
  if (!res) return;
  superiorityDie.uses_remaining = uses_remaining;
  updateSdDisplay();
}

document.getElementById("sd-down").onclick = async () => {
  if (!superiorityDie || superiorityDie.uses_remaining <= 0) return;
  await patchSuperiorityDie(superiorityDie.uses_remaining - 1);
};

document.getElementById("sd-up").onclick = async () => {
  if (!superiorityDie || superiorityDie.uses_remaining >= superiorityDie.uses_max) return;
  await patchSuperiorityDie(superiorityDie.uses_remaining + 1);
};

// ── Ability cards ────────────────────────────────────────────────────────────

function renderAbilityCard(a) {
  const div = document.createElement("div");
  div.className = "ability-card";
  const isManeuver = a.name.startsWith("Maneuver:");
  const hasUses = a.uses_max != null;
  const showUseBtn = hasUses || isManeuver;
  const rem = a.uses_remaining ?? a.uses_max;
  const usesText = hasUses ? `${rem} / ${a.uses_max}` : "";
  const rechargeBadge = a.recharge
    ? `<span class="recharge-badge recharge-${a.recharge}">${RECHARGE_LABEL[a.recharge]}</span>`
    : "";
  div.innerHTML = `
    <div class="ability-card-header">
      <div>
        <span class="ability-name">${escHtml(a.name)}</span>
        ${rechargeBadge}
      </div>
      <div class="card-actions">
        ${showUseBtn ? `<button class="use-btn" data-id="${a.id}" data-rem="${rem ?? 99}">Use</button>` : ""}
        <button class="edit-ability-btn" data-id="${a.id}">Edit</button>
        <button class="del-ability-btn" data-id="${a.id}">✕</button>
      </div>
    </div>
    ${a.description ? `<div class="ability-desc">${escHtml(a.description)}</div>` : ""}
    ${usesText ? `<div class="ability-uses">Uses: ${usesText}</div>` : ""}
  `;

  div.querySelector(".edit-ability-btn")?.addEventListener("click", () => openAbilityModal(a));

  div.querySelector(".del-ability-btn")?.addEventListener("click", async () => {
    const res = await apiFetch(`/api/abilities/${a.id}`, { method: "DELETE" }, "Failed to delete ability.");
    if (!res) return;
    loadAbilities();
  });

  div.querySelector(".use-btn")?.addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    if (hasUses) {
      const cur = Number(btn.dataset.rem);
      if (cur <= 0) return;
      const next = cur - 1;
      const res = await apiFetch(
        `/api/abilities/${a.id}`,
        { method: "PUT", body: { uses_remaining: next } },
        "Failed to use ability."
      );
      if (!res) return;
      btn.dataset.rem = next;
      div.querySelector(".ability-uses").textContent = `Uses: ${next} / ${a.uses_max}`;
    }
    if (isManeuver && superiorityDie && superiorityDie.uses_remaining > 0) {
      await patchSuperiorityDie(superiorityDie.uses_remaining - 1);
    }
  });

  return div;
}

// ── Load abilities ───────────────────────────────────────────────────────────

async function loadAbilities() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/abilities`);
  const abilities = await res.json();
  const list = document.getElementById("abilities-list");
  list.innerHTML = "";

  if (abilities.length === 0) {
    list.innerHTML = `<p style="color:var(--muted);font-size:.85rem">No abilities yet.</p>`;
    return;
  }

  const poolIdx = abilities.findIndex(a => a.name === "Superiority Dice Pool (d8)");
  if (poolIdx !== -1) {
    superiorityDie = abilities.splice(poolIdx, 1)[0];
    updateSdDisplay();
  }

  const grouped = {};
  ABILITY_GROUPS.forEach(g => { grouped[g.key] = []; });
  abilities.forEach(a => {
    const key = normalizeType(a.type);
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(a);
  });

  ABILITY_GROUPS.forEach(({ key, label }) => {
    const header = document.createElement("div");
    header.className = "ability-group-header";
    header.textContent = label;
    list.appendChild(header);

    if (key === "action") renderStandardActions(list, currentItems);

    if (grouped[key] && grouped[key].length > 0)
      grouped[key].forEach(a => list.appendChild(renderAbilityCard(a)));
  });
}

// ── Ability modal ────────────────────────────────────────────────────────────

const abilityModal = document.getElementById("ability-modal");
const abilityForm  = document.getElementById("ability-form");

function openAbilityModal(ability = null) {
  abilityForm.reset();
  document.getElementById("ability-modal-title").textContent = ability ? "Edit Ability" : "Add Ability";
  if (ability) {
    abilityForm.id_field        = ability.id;
    abilityForm._uses_remaining = ability.uses_remaining;
    abilityForm.name.value        = ability.name;
    abilityForm.type.value        = ability.type;
    abilityForm.description.value = ability.description;
    abilityForm.uses_max.value    = ability.uses_max ?? "";
    abilityForm.recharge.value    = ability.recharge ?? "";
  } else {
    abilityForm.id_field        = null;
    abilityForm._uses_remaining = null;
  }
  abilityModal.showModal();
}

document.getElementById("add-ability-btn").onclick = () => openAbilityModal();
document.getElementById("cancel-ability").onclick  = () => abilityModal.close();

abilityForm.onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(abilityForm);
  const body = Object.fromEntries(fd.entries());
  if (body.uses_max === "") body.uses_max = null;
  else body.uses_max = Number(body.uses_max);
  if (body.recharge === "") body.recharge = null;

  if (abilityForm.id_field) {
    // Preserve existing uses_remaining; only cap it if uses_max shrank
    const prevRemaining = abilityForm._uses_remaining;
    if (body.uses_max != null) {
      body.uses_remaining = (prevRemaining != null)
        ? Math.min(prevRemaining, body.uses_max)
        : body.uses_max;
    }
    const res = await apiFetch(
      `/api/abilities/${abilityForm.id_field}`,
      { method: "PUT", body },
      "Failed to update ability."
    );
    if (!res) return;
  } else {
    const res = await apiFetch(
      `/api/characters/${CHARACTER_ID}/abilities`,
      { method: "POST", body },
      "Failed to add ability."
    );
    if (!res) return;
  }
  abilityModal.close();
  loadAbilities();
};
