// Abilities panel — loading, rendering, superiority dice, and modal.

const ABILITY_GROUPS = [
  { key: "action", label: "Action" },
  { key: "bonus_action", label: "Bonus Action" },
  { key: "reaction", label: "Reaction" },
  { key: "free_action", label: "Free Action" },
  { key: "passive", label: "Passive" },
];

const STANDARD_ACTIONS = [
  { name: "Dash", desc: "Double your speed this turn." },
  {
    name: "Disengage",
    desc: "Your movement doesn't provoke opportunity attacks for the rest of the turn.",
  },
  {
    name: "Dodge",
    desc: "Until the start of your next turn, attacks against you have Disadvantage and you have Advantage on DEX saves.",
  },
  {
    name: "Help",
    desc: "Give an ally Advantage on their next ability check or attack roll.",
  },
  { name: "Hide", desc: "Make a Stealth check to become hidden." },
  {
    name: "Ready",
    desc: "Prepare a reaction to trigger on a specified condition before your next turn.",
  },
  {
    name: "Search",
    desc: "Make a Perception or Investigation check to locate something.",
  },
];

const RECHARGE_LABEL = { short: "short rest", long: "long rest" };

// Map legacy type values to display groups
function normalizeType(type) {
  if (type === "active" || type === "spell") return "action";
  return type;
}

// ── Standard Actions ─────────────────────────────────────────────────────────

function renderStandardActions(list, items) {
  const weapons = items.filter((i) => i.is_weapon && i.equipped && i.damage_dice);
  const prof = profBonus(char.level);
  const strMod = Math.floor((char.str - 10) / 2);
  const dexMod = Math.floor((char.dex - 10) / 2);

  const attackCard = document.createElement("div");
  attackCard.className = "ability-card standard-action-card";

  let weaponRows = "";
  if (weapons.length === 0) {
    weaponRows = `<div class="attack-weapon-row muted">No weapons equipped.</div>`;
  } else {
    weapons.forEach((w) => {
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

// ── Combat panel pip helper ───────────────────────────────────────────────────
// Renders clickable pips into a container, syncing with an ability object.
// dieType: a dieSvg() key ("d8", "d10", "dot", etc.)

function renderCombatPips(containerId, ability, dieType, onUpdate) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = "";
  for (let i = 0; i < ability.uses_max; i++) {
    const filled = i < ability.uses_remaining;
    const btn = document.createElement("button");
    btn.className = `die-pip ${dieType}-pip` + (filled ? " die-filled" : "");
    btn.title = filled ? `Use ${i + 1}` : `Recover ${i + 1}`;
    btn.innerHTML = dieSvg(dieType);
    btn.addEventListener("click", async () => {
      const next = filled ? i : i + 1;
      const res = await apiFetch(
        `/api/abilities/${ability.id}`,
        { method: "PUT", body: { uses_remaining: next } },
        "Failed to update."
      );
      if (!res) return;
      ability.uses_remaining = next;
      renderCombatPips(containerId, ability, dieType, onUpdate);
      if (onUpdate) onUpdate(ability);
    });
    container.appendChild(btn);
  }
}

// ── Superiority Dice ─────────────────────────────────────────────────────────

function renderSdPips() {
  if (!superiorityDie) return;
  const dieType = superiorityDie.die_type || "d8";
  document.getElementById("sd-label").textContent = `Sup. Dice (${dieType})`;
  renderCombatPips("sd-pips", superiorityDie, dieType, () => {});
}

async function patchSuperiorityDie(uses_remaining) {
  const res = await apiFetch(
    `/api/abilities/${superiorityDie.id}`,
    { method: "PUT", body: { uses_remaining } },
    "Failed to update superiority dice."
  );
  if (!res) return;
  superiorityDie.uses_remaining = uses_remaining;
  renderSdPips();
}

// ── Second Wind (combat panel) ───────────────────────────────────────────────

function renderSwPips() {
  if (!secondWind) return;
  const dieType = secondWind.die_type || "d10";
  document.getElementById("sw-label").textContent = `Second Wind (${dieType})`;
  renderCombatPips("sw-pips", secondWind, dieType, (a) => {
    document
      .querySelectorAll(`.ability-pips[data-id="${a.id}"]`)
      .forEach((c) => renderAbilityPips(c, a));
  });
}

// ── Sorcery Points (combat panel) ────────────────────────────────────────────

function renderSpPips() {
  if (!sorceryPoints) return;
  renderCombatPips("sp-pips", sorceryPoints, "dot", (a) => {
    document
      .querySelectorAll(`.ability-pips[data-id="${a.id}"]`)
      .forEach((c) => renderAbilityPips(c, a));
  });
}

// ── Spell Slots (combat panel) ───────────────────────────────────────────────

function renderSlotPips(ability, containerId) {
  if (!ability) return;
  renderCombatPips(containerId, ability, "dot", (a) => {
    document
      .querySelectorAll(`.ability-pips[data-id="${a.id}"]`)
      .forEach((c) => renderAbilityPips(c, a));
  });
}

// ── Ability cards ────────────────────────────────────────────────────────────

function renderAbilityCard(a) {
  const div = document.createElement("div");
  div.className = "ability-card";
  const isManeuver = a.name.startsWith("Maneuver:");
  const hasUses = a.uses_max != null;
  const hasDie = !!a.die_type;
  // Shared pool: no own uses but die_type matches an existing pool (e.g. Tactical Mind → Second Wind)
  const sharedPool =
    hasDie && !hasUses && secondWind && secondWind.die_type === a.die_type
      ? secondWind
      : null;
  // Abilities with a die type + own uses → show own clickable pip icons
  const showDiePips = hasDie && hasUses;
  const showUseBtn = !showDiePips && !sharedPool && (hasUses || isManeuver);
  const rem = a.uses_remaining ?? a.uses_max;
  const usesText = hasUses && !showDiePips ? `${rem} / ${a.uses_max}` : "";
  const rechargeBadge = a.recharge
    ? `<span class="recharge-badge recharge-${a.recharge}">${RECHARGE_LABEL[a.recharge]}</span>`
    : "";
  // Passive die type with no shared pool → static badge next to name
  const dieBadge =
    hasDie && !hasUses && !sharedPool
      ? `<span class="die-type-badge">${dieSvg(a.die_type)}</span>`
      : "";
  div.innerHTML = `
    <div class="ability-card-header">
      <div>
        <span class="ability-name">${escHtml(a.name)}</span>
        ${dieBadge}
        ${rechargeBadge}
      </div>
      <div class="card-actions">
        ${showUseBtn ? `<button class="use-btn" data-id="${a.id}" data-rem="${rem ?? 99}">Use</button>` : ""}
        <button class="edit-ability-btn" data-id="${a.id}">Edit</button>
        <button class="del-ability-btn" data-id="${a.id}">✕</button>
      </div>
    </div>
    ${(a.spell_range || a.duration || a.concentration || a.components) ? `
    <div class="ability-meta">
      ${a.spell_range ? `<span><span class="meta-label">Range:</span> ${escHtml(a.spell_range)}</span>` : ""}
      ${a.duration ? `<span><span class="meta-label">Duration:</span> ${escHtml(a.duration)}</span>` : ""}
      ${a.concentration ? `<span class="conc-badge">Concentration</span>` : ""}
      ${a.components ? `<span><span class="meta-label">Components:</span> ${escHtml(a.components)}</span>` : ""}
    </div>` : ""}
    ${a.description ? `<div class="ability-desc">${escHtml(a.description)}</div>` : ""}
    ${a.flavor ? `<div class="ability-flavor">${escHtml(a.flavor)}</div>` : ""}
    ${showDiePips || sharedPool ? `<div class="ability-pips" data-id="${(sharedPool ?? a).id}"></div>` : ""}
    ${usesText ? `<div class="ability-uses">Uses: ${usesText}</div>` : ""}
  `;

  div
    .querySelector(".edit-ability-btn")
    ?.addEventListener("click", () => openAbilityModal(a));

  div.querySelector(".del-ability-btn")?.addEventListener("click", async () => {
    const res = await apiFetch(
      `/api/abilities/${a.id}`,
      { method: "DELETE" },
      "Failed to delete ability."
    );
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

  if (showDiePips) {
    renderAbilityPips(div.querySelector(".ability-pips"), a);
  } else if (sharedPool) {
    renderAbilityPips(div.querySelector(".ability-pips"), sharedPool);
  }

  return div;
}

function renderAbilityPips(container, a) {
  container.innerHTML = "";
  const rem = a.uses_remaining ?? a.uses_max;
  for (let i = 0; i < a.uses_max; i++) {
    const filled = i < rem;
    const btn = document.createElement("button");
    btn.className = `die-pip ${a.die_type}-pip` + (filled ? " die-filled" : "");
    btn.title = filled ? `Use die ${i + 1}` : `Recover die ${i + 1}`;
    btn.innerHTML = dieSvg(a.die_type);
    btn.addEventListener("click", async () => {
      const next = filled ? i : i + 1;
      const res = await apiFetch(
        `/api/abilities/${a.id}`,
        { method: "PUT", body: { uses_remaining: next } },
        "Failed to update ability."
      );
      if (!res) return;
      a.uses_remaining = next;
      // Re-render all card pip containers tied to this pool
      document
        .querySelectorAll(`.ability-pips[data-id="${a.id}"]`)
        .forEach((c) => renderAbilityPips(c, a));
      if (secondWind && secondWind.id === a.id) renderSwPips();
    });
    container.appendChild(btn);
  }
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

  // ── Detect named abilities for combat panel widgets ──────────────────────

  const poolIdx = abilities.findIndex((a) => a.name === "Superiority Dice Pool (d8)");
  superiorityDie = poolIdx !== -1 ? abilities.splice(poolIdx, 1)[0] : null;
  document.getElementById("sd-box").hidden = !superiorityDie;
  document.getElementById("maneuver-dc-box").hidden = !superiorityDie;
  if (superiorityDie) renderSdPips();

  const swIdx = abilities.findIndex((a) => a.name === "Second Wind");
  secondWind = swIdx !== -1 ? abilities[swIdx] : null;
  document.getElementById("sw-box").hidden = !secondWind;
  if (secondWind) renderSwPips();

  const spIdx = abilities.findIndex((a) => a.name === "Sorcery Points");
  sorceryPoints = spIdx !== -1 ? abilities[spIdx] : null;
  document.getElementById("sp-box").hidden = !sorceryPoints;
  if (sorceryPoints) renderSpPips();

  const sl1Idx = abilities.findIndex((a) => a.name === "Spell Slots — 1st Level");
  spellSlotsL1 = sl1Idx !== -1 ? abilities[sl1Idx] : null;
  document.getElementById("slots-1-box").hidden = !spellSlotsL1;
  if (spellSlotsL1) renderSlotPips(spellSlotsL1, "slots-1-pips");

  const sl2Idx = abilities.findIndex((a) => a.name === "Spell Slots — 2nd Level");
  spellSlotsL2 = sl2Idx !== -1 ? abilities[sl2Idx] : null;
  document.getElementById("slots-2-box").hidden = !spellSlotsL2;
  if (spellSlotsL2) renderSlotPips(spellSlotsL2, "slots-2-pips");

  const hasGoodberry = abilities.some((a) =>
    a.name.toLowerCase().includes("goodberry")
  );
  document.getElementById("tomato-section").hidden = !hasGoodberry;

  // Compute AC contribution from abilities and refresh the AC display
  const acAbilities = abilities.filter((a) => a.ac_bonus);
  abilityAcBonus = acAbilities.reduce((s, a) => s + a.ac_bonus, 0);
  abilityAcBreakdown = acAbilities.map((a) => ({
    id: a.id,
    name: a.name,
    ac_bonus: a.ac_bonus,
  }));
  if (currentItems.length > 0) updateAcDisplay();

  abilitySaveParts = abilities
    .filter((a) => a.save_bonus)
    .map((a) => ({
      type: "ability",
      id: a.id,
      name: a.name,
      save_bonus: a.save_bonus,
    }));
  renderSaves();

  const advBadge = document.getElementById("ds-adv-badge");
  if (advBadge) {
    advBadge.hidden = !abilities.some(
      (a) =>
        a.description &&
        a.description.toLowerCase().includes("advantage on death saving throws")
    );
  }
  updateDeathSaveOdds();

  const grouped = {};
  ABILITY_GROUPS.forEach((g) => {
    grouped[g.key] = [];
  });
  abilities.forEach((a) => {
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
      grouped[key].forEach((a) => list.appendChild(renderAbilityCard(a)));
  });
}

// ── Ability modal ────────────────────────────────────────────────────────────

const abilityModal = document.getElementById("ability-modal");
const abilityForm = document.getElementById("ability-form");

function openAbilityModal(ability = null) {
  abilityForm.reset();
  document.getElementById("ability-modal-title").textContent = ability
    ? "Edit Ability"
    : "Add Ability";
  if (ability) {
    abilityForm.id_field = ability.id;
    abilityForm._uses_remaining = ability.uses_remaining;
    abilityForm.name.value = ability.name;
    abilityForm.type.value = ability.type;
    abilityForm.description.value = ability.description;
    abilityForm.uses_max.value = ability.uses_max ?? "";
    abilityForm.recharge.value = ability.recharge ?? "";
    abilityForm.die_type.value = ability.die_type ?? "";
    abilityForm.ac_bonus.value = ability.ac_bonus ?? 0;
    abilityForm.save_bonus.value = ability.save_bonus ?? 0;
    abilityForm.flavor.value = ability.flavor ?? "";
    abilityForm.components.value = ability.components ?? "";
    abilityForm.spell_range.value = ability.spell_range ?? "";
    abilityForm.duration.value = ability.duration ?? "";
    abilityForm.concentration.checked = !!ability.concentration;
  } else {
    abilityForm.id_field = null;
    abilityForm._uses_remaining = null;
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
  if (body.die_type === "") body.die_type = null;
  body.ac_bonus = Number(body.ac_bonus) || 0;
  body.save_bonus = Number(body.save_bonus) || 0;
  body.concentration = abilityForm.concentration.checked ? 1 : 0;

  if (abilityForm.id_field) {
    // Preserve existing uses_remaining; only cap it if uses_max shrank
    const prevRemaining = abilityForm._uses_remaining;
    if (body.uses_max != null) {
      body.uses_remaining =
        prevRemaining != null ? Math.min(prevRemaining, body.uses_max) : body.uses_max;
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
