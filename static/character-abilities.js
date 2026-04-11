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
      const abilMod = w.finesse
        ? Math.max(strMod, dexMod)
        : w.is_melee ? strMod : dexMod;
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

const SLOT_ORDINALS = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th"];

function renderSlotPips(ability, containerId) {
  if (!ability) return;
  renderCombatPips(containerId, ability, "dot", (a) => {
    document
      .querySelectorAll(`.ability-pips[data-id="${a.id}"]`)
      .forEach((c) => renderAbilityPips(c, a));
  });
}

// Consume one spell slot at `level` and refresh its pips.
async function useSpellSlot(level) {
  const slot = spellSlots[level];
  if (!slot || slot.uses_remaining <= 0) {
    showToast(`No ${SLOT_ORDINALS[level - 1]}-level spell slots remaining.`);
    return false;
  }
  const next = slot.uses_remaining - 1;
  const res = await apiFetch(
    `/api/abilities/${slot.id}`,
    { method: "PUT", body: { uses_remaining: next } },
    "Failed to use spell slot."
  );
  if (!res) return false;
  slot.uses_remaining = next;
  renderSlotPips(slot, `slots-${level}-pips`);
  document
    .querySelectorAll(`.ability-pips[data-id="${slot.id}"]`)
    .forEach((c) => renderAbilityPips(c, slot));
  return true;
}

// ── Ability cards ────────────────────────────────────────────────────────────

const SP_SLOT_COST = { 1: 2, 2: 3, 3: 5, 4: 6, 5: 7 };

function renderAbilityCard(a) {
  const div = document.createElement("div");
  div.className = "ability-card";
  const isManeuver = a.name.startsWith("Maneuver:");
  const isMetamagic = a.name.startsWith("Metamagic:");
  const isFontSlotToSP = a.name === "Font of Magic: Slot → Sorcery Points";
  const isFontSPToSlot = a.name === "Font of Magic: Sorcery Points → Slot";
  const hasUses = a.uses_max != null;
  const hasDie = !!a.die_type;
  // Shared pool: no own uses but die_type matches an existing pool (e.g. Tactical Mind → Second Wind)
  const sharedPool =
    hasDie && !hasUses && secondWind && secondWind.die_type === a.die_type
      ? secondWind
      : null;
  // Abilities with a die type + own uses → show own clickable pip icons
  const showDiePips = hasDie && hasUses;
  const showUseBtn = !showDiePips && !sharedPool && (hasUses || isManeuver || isMetamagic);
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
  // Spell slot buttons
  const spellLevel = a.spell_level ? Number(a.spell_level) : null;
  const isSpell = spellLevel != null && spellLevel >= 1;
  const isActiveBaseAc = !!(a.sets_base_ac && a.active);
  let castBtns = "";
  if (isSpell && !isActiveBaseAc) {
    const ord = SLOT_ORDINALS[spellLevel - 1];
    castBtns += `<button class="cast-btn" data-level="${spellLevel}">Cast (${ord})</button>`;
    if (a.upcastable) {
      for (let lvl = spellLevel + 1; lvl <= 9; lvl++) {
        if (spellSlots[lvl]) {
          const upOrd = SLOT_ORDINALS[lvl - 1];
          castBtns += `<button class="cast-btn upcast-btn" data-level="${lvl}">↑ ${upOrd}</button>`;
        }
      }
    }
  }
  const isActivatable = !!a.activatable;
  const showActive = isActiveBaseAc || (isActivatable && a.active);
  const activeBadge = showActive ? `<span class="active-spell-badge">Active</span>` : "";
  const endBtn = showActive ? `<button class="end-spell-btn" data-id="${a.id}">End</button>` : "";

  // Font of Magic conversion buttons (built dynamically from current slot/SP state)
  let fontConvBtns = "";
  if (isFontSlotToSP) {
    [1, 2, 3, 4, 5].forEach((lvl) => {
      const slot = spellSlots[lvl];
      const spAtMax = sorceryPoints && sorceryPoints.uses_remaining >= sorceryPoints.uses_max;
      if (slot && slot.uses_remaining > 0 && !spAtMax) {
        const ord = SLOT_ORDINALS[lvl - 1];
        fontConvBtns += `<button class="cast-btn font-conv-btn" data-dir="to-sp" data-level="${lvl}">${ord} slot → ${lvl} SP</button>`;
      }
    });
    if (!fontConvBtns)
      fontConvBtns = `<span class="muted" style="font-size:.8rem">No slots available to convert.</span>`;
  }
  if (isFontSPToSlot) {
    const spRem = sorceryPoints ? (sorceryPoints.uses_remaining ?? 0) : 0;
    [1, 2, 3, 4, 5].forEach((lvl) => {
      const cost = SP_SLOT_COST[lvl];
      const slot = spellSlots[lvl];
      if (slot && slot.uses_remaining < slot.uses_max && spRem >= cost) {
        const ord = SLOT_ORDINALS[lvl - 1];
        fontConvBtns += `<button class="cast-btn font-conv-btn" data-dir="to-slot" data-level="${lvl}" data-cost="${cost}">${ord} slot (${cost} SP)</button>`;
      }
    });
    if (!fontConvBtns)
      fontConvBtns = `<span class="muted" style="font-size:.8rem">Insufficient SP or all slots full.</span>`;
  }

  div.innerHTML = `
    <div class="ability-card-header">
      <div>
        <span class="ability-name">${escHtml(a.name)}</span>
        ${dieBadge}
        ${rechargeBadge}
        ${activeBadge}
      </div>
      <div class="card-actions">
        ${showUseBtn ? `<button class="use-btn" data-id="${a.id}" data-rem="${rem ?? 99}">${isMetamagic ? "Use (1 SP)" : "Use"}</button>` : ""}
        ${endBtn}
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
    ${castBtns ? `<div class="cast-actions">${castBtns}</div>` : ""}
    ${fontConvBtns ? `<div class="cast-actions">${fontConvBtns}</div>` : ""}
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
      const body = { uses_remaining: next };
      if (isActivatable) body.active = 1;
      const res = await apiFetch(
        `/api/abilities/${a.id}`,
        { method: "PUT", body },
        "Failed to use ability."
      );
      if (!res) return;
      if (isActivatable) {
        a.active = 1;
        loadAbilities();
        return;
      }
      btn.dataset.rem = next;
      div.querySelector(".ability-uses").textContent = `Uses: ${next} / ${a.uses_max}`;
    }
    if (isManeuver && superiorityDie && superiorityDie.uses_remaining > 0) {
      await patchSuperiorityDie(superiorityDie.uses_remaining - 1);
    }
    if (isMetamagic) {
      if (!sorceryPoints || sorceryPoints.uses_remaining <= 0) {
        showToast("No sorcery points remaining.");
        return;
      }
      const next = sorceryPoints.uses_remaining - 1;
      const res = await apiFetch(
        `/api/abilities/${sorceryPoints.id}`,
        { method: "PUT", body: { uses_remaining: next } },
        "Failed to use sorcery point."
      );
      if (!res) return;
      sorceryPoints.uses_remaining = next;
      renderSpPips();
      document
        .querySelectorAll(`.ability-pips[data-id="${sorceryPoints.id}"]`)
        .forEach((c) => renderAbilityPips(c, sorceryPoints));
    }
  });

  div.querySelector(".end-spell-btn")?.addEventListener("click", async () => {
    const res = await apiFetch(
      `/api/abilities/${a.id}`,
      { method: "PUT", body: { active: 0 } },
      "Failed to end spell."
    );
    if (!res) return;
    a.active = 0;
    loadAbilities();
  });

  div.querySelectorAll(".font-conv-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const dir = btn.dataset.dir;
      const lvl = Number(btn.dataset.level);
      if (dir === "to-sp") {
        const slot = spellSlots[lvl];
        if (!slot || slot.uses_remaining <= 0) {
          showToast("No slots of that level remaining.");
          return;
        }
        if (!sorceryPoints || sorceryPoints.uses_remaining >= sorceryPoints.uses_max) {
          showToast("Sorcery points already at maximum.");
          return;
        }
        const spNext = Math.min(sorceryPoints.uses_remaining + lvl, sorceryPoints.uses_max);
        const r1 = await apiFetch(
          `/api/abilities/${slot.id}`,
          { method: "PUT", body: { uses_remaining: slot.uses_remaining - 1 } },
          "Failed to use spell slot."
        );
        if (!r1) return;
        const r2 = await apiFetch(
          `/api/abilities/${sorceryPoints.id}`,
          { method: "PUT", body: { uses_remaining: spNext } },
          "Failed to update sorcery points."
        );
        if (!r2) return;
        loadAbilities();
      } else {
        const cost = Number(btn.dataset.cost);
        const slot = spellSlots[lvl];
        if (!sorceryPoints || sorceryPoints.uses_remaining < cost) {
          showToast(`Not enough sorcery points (need ${cost}).`);
          return;
        }
        if (!slot || slot.uses_remaining >= slot.uses_max) {
          showToast("Spell slots already at maximum for that level.");
          return;
        }
        const r1 = await apiFetch(
          `/api/abilities/${sorceryPoints.id}`,
          { method: "PUT", body: { uses_remaining: sorceryPoints.uses_remaining - cost } },
          "Failed to use sorcery points."
        );
        if (!r1) return;
        const r2 = await apiFetch(
          `/api/abilities/${slot.id}`,
          { method: "PUT", body: { uses_remaining: slot.uses_remaining + 1 } },
          "Failed to update spell slot."
        );
        if (!r2) return;
        loadAbilities();
      }
    });
  });

  div.querySelectorAll(".cast-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const ok = await useSpellSlot(Number(btn.dataset.level));
      if (!ok) return;
      if (a.sets_base_ac) {
        const res = await apiFetch(
          `/api/abilities/${a.id}`,
          { method: "PUT", body: { active: 1 } },
          "Failed to activate spell."
        );
        if (!res) return;
        a.active = 1;
        loadAbilities();
      }
    });
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

  const isIdx = abilities.findIndex((a) => a.name === "Innate Sorcery");
  innateSorcery = isIdx !== -1 ? abilities[isIdx] : null;

  // Spell Save DC and Spell Attack Bonus (CHA-based caster, shown when sorcery points present)
  const hasSorcerer = !!sorceryPoints;
  document.getElementById("spell-dc-box").hidden = !hasSorcerer;
  document.getElementById("spell-atk-box").hidden = !hasSorcerer;
  if (hasSorcerer) {
    const prof = profBonus(char.level);
    const chaMod = Math.floor((char.cha - 10) / 2);
    const innateActive = !!(innateSorcery && innateSorcery.active);
    const dc = 8 + prof + chaMod + (innateActive ? 1 : 0);
    document.getElementById("spell-dc-val").innerHTML = innateActive
      ? `${dc} <span class="active-spell-badge">+1</span>`
      : `${dc}`;
    const atk = prof + chaMod;
    const atkStr = atk >= 0 ? `+${atk}` : `${atk}`;
    document.getElementById("spell-atk-val").innerHTML = innateActive
      ? `${atkStr} <span class="active-spell-badge">ADV</span>`
      : atkStr;
  }

  // Clear existing slot map
  for (let lvl = 1; lvl <= 9; lvl++) delete spellSlots[lvl];

  const SLOT_NAMES = [
    "Spell Slots — 1st Level",
    "Spell Slots — 2nd Level",
    "Spell Slots — 3rd Level",
    "Spell Slots — 4th Level",
    "Spell Slots — 5th Level",
    "Spell Slots — 6th Level",
    "Spell Slots — 7th Level",
    "Spell Slots — 8th Level",
    "Spell Slots — 9th Level",
  ];
  SLOT_NAMES.forEach((slotName, i) => {
    const lvl = i + 1;
    const idx = abilities.findIndex((a) => a.name === slotName);
    const slot = idx !== -1 ? abilities[idx] : null;
    // Keep L1/L2 legacy globals in sync
    if (lvl === 1) spellSlotsL1 = slot;
    if (lvl === 2) spellSlotsL2 = slot;
    if (slot) spellSlots[lvl] = slot;
    const box = document.getElementById(`slots-${lvl}-box`);
    if (box) box.hidden = !slot;
    if (slot) renderSlotPips(slot, `slots-${lvl}-pips`);
  });

  const hasGoodberry = abilities.some((a) =>
    a.name.toLowerCase().includes("goodberry")
  );
  document.getElementById("tomato-section").hidden = !hasGoodberry;

  // Compute AC contribution from abilities and refresh the AC display
  abilityBaseAcAbility = abilities.find((a) => a.sets_base_ac && a.active) || null;
  const acAbilities = abilities.filter((a) => a.ac_bonus && !a.sets_base_ac);
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
    abilityForm.sets_base_ac.checked = !!ability.sets_base_ac;
    abilityForm.activatable.checked = !!ability.activatable;
    abilityForm.spell_level.value = ability.spell_level ?? "";
    abilityForm.upcastable.checked = !!ability.upcastable;
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
  body.sets_base_ac = abilityForm.sets_base_ac.checked ? 1 : 0;
  body.activatable = abilityForm.activatable.checked ? 1 : 0;
  body.spell_level = body.spell_level !== "" ? Number(body.spell_level) : null;
  body.upcastable = abilityForm.upcastable.checked ? 1 : 0;

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
