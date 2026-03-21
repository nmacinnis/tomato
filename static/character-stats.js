// Stats, HP, hit dice, death saves, goodberries, notes, rest, delete.

function editName() {
  const el = document.getElementById("char-name");
  const current = char.name;
  const input = document.createElement("input");
  input.type = "text";
  input.value = current;
  input.style.cssText =
    "font-size:inherit;font-weight:inherit;font-family:inherit;background:#0f3460;border:1px solid var(--accent);color:var(--text);border-radius:4px;padding:0 4px;width:12rem;";
  el.replaceWith(input);
  input.focus();
  input.select();
  const save = async () => {
    const val = input.value.trim() || current;
    await patchChar({ name: val });
    input.replaceWith(el);
    el.textContent = val;
    document.title = val;
  };
  input.onblur = save;
  input.onkeydown = (e) => {
    if (e.key === "Enter") save();
    if (e.key === "Escape") {
      input.value = current;
      input.blur();
    }
  };
}

function renderCharacter() {
  document.title = char.name;
  const nameEl = document.getElementById("char-name");
  nameEl.textContent = char.name;
  nameEl.style.cursor = "pointer";
  nameEl.onclick = editName;
  document.getElementById("char-subtitle").textContent =
    `${char.race} ${char.class} — Level ${char.level}`;

  const prof = profBonus(char.level);

  ["str", "dex", "con", "int", "wis", "cha"].forEach((stat) => {
    const box = document.querySelector(`.stat-box[data-stat="${stat}"]`);
    box.querySelector(".stat-val").textContent = char[stat];
    box.querySelector(".stat-mod").textContent = modifier(char[stat]);
    box.onclick = () => editStat(stat);
  });

  renderSaves();

  updateHpDisplay();
  updateThpDisplay();
  document.getElementById("ac-val").textContent = char.ac;
  document.getElementById("speed-val").textContent = `${char.speed} ft`;
  document.getElementById("level-val").textContent = char.level;
  document.getElementById("notes-area").value = char.notes || "";

  const dexMod = Math.floor((char.dex - 10) / 2);
  const wisMod = Math.floor((char.wis - 10) / 2);
  document.getElementById("prof-val").textContent = `+${prof}`;
  document.getElementById("init-val").textContent =
    dexMod >= 0 ? `+${dexMod}` : `${dexMod}`;
  document.getElementById("perc-val").textContent = 10 + wisMod + prof;
  const strMod = Math.floor((char.str - 10) / 2);
  document.getElementById("maneuver-dc-val").textContent =
    8 + prof + Math.max(strMod, dexMod);
  document.getElementById("alignment-val").textContent = abbreviateAlignment(
    char.alignment || ""
  );
  document.getElementById("size-val").textContent = char.size || "";
  document.getElementById("height-val").textContent = char.height || "";
  document.getElementById("weight-val").textContent = char.weight || "";

  renderMoney();
  renderHdPips();
  renderDeathSaves();
  renderTomatoes();
}

// ── Death save odds ──────────────────────────────────────────────────────────

function computeDeathSurvival(s, f, saveBonus, hasAdvantage) {
  const threshold = Math.min(20, Math.max(2, 10 - saveBonus));
  const failBase = (threshold - 1) / 20;
  let p20, pS, pF, pF2;
  if (hasAdvantage) {
    p20 = 1 - Math.pow(19 / 20, 2);
    pS = Math.pow(19 / 20, 2) - Math.pow(failBase, 2);
    pF2 = Math.pow(1 / 20, 2);
    pF = Math.pow(failBase, 2) - pF2;
  } else {
    p20 = 1 / 20;
    pS = (19 - threshold + 1) / 20;
    pF2 = 1 / 20;
    pF = (threshold - 2) / 20;
  }
  const memo = {};
  function P(sv, fl) {
    if (sv >= 3) return 1;
    if (fl >= 3) return 0;
    const key = sv * 4 + fl;
    if (key in memo) return memo[key];
    return (memo[key] =
      p20 + pS * P(sv + 1, fl) + pF * P(sv, fl + 1) + pF2 * P(sv, fl + 2));
  }
  return P(s, f);
}

function updateDeathSaveOdds() {
  const el = document.getElementById("ds-odds");
  if (!el) return;
  const s = char?.death_save_successes ?? 0;
  const f = char?.death_save_failures ?? 0;
  if (s >= 3 || f >= 3) {
    el.textContent = "";
    return;
  }
  const totalSaveBonus = [...itemSaveParts, ...abilitySaveParts].reduce(
    (sum, p) => sum + p.save_bonus,
    0
  );
  const advBadge = document.getElementById("ds-adv-badge");
  const hasAdv = !!advBadge && !advBadge.hidden;
  const pLive = computeDeathSurvival(s, f, totalSaveBonus, hasAdv);
  el.textContent = `${(pLive * 100).toFixed(1)}% chance of survival`;
}

// ── Saves ────────────────────────────────────────────────────────────────────

function renderSaves() {
  const prof = profBonus(char.level);
  const saveProfs = new Set(
    (char.save_proficiencies || "")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
  );
  const totalSaveBonus =
    itemSaveParts.reduce((s, p) => s + p.save_bonus, 0) +
    abilitySaveParts.reduce((s, p) => s + p.save_bonus, 0);
  ["str", "dex", "con", "int", "wis", "cha"].forEach((stat) => {
    const box = document.querySelector(`.stat-box[data-stat="${stat}"]`);
    const mod = Math.floor((char[stat] - 10) / 2);
    const proficient = saveProfs.has(stat);
    const saveVal = mod + (proficient ? prof : 0) + totalSaveBonus;
    const saveEl = box.querySelector(".stat-save");
    saveEl.textContent = `save ${saveVal >= 0 ? "+" : ""}${saveVal}`;
    saveEl.className = "stat-save" + (proficient ? " save-proficient" : "");
  });
  updateSaveBonusDisplay();
}

function updateSaveBonusDisplay() {
  const allParts = [...itemSaveParts, ...abilitySaveParts];
  const total = allParts.reduce((s, p) => s + p.save_bonus, 0);
  const el = document.getElementById("save-bonus-val");
  if (el) el.textContent = total ? `+${total}` : "—";
  const bd = document.getElementById("save-bonus-breakdown");
  if (bd) {
    bd.innerHTML = allParts
      .map(
        (p) =>
          `<button class="ac-link" data-type="${p.type}" data-id="${p.id}">${escHtml(`+${p.save_bonus} (${p.name})`)}</button>`
      )
      .join(" ");
  }
  const ds = document.getElementById("ds-save-bonus");
  if (!ds) return;
  if (!total) {
    ds.innerHTML = "";
    ds.onclick = null;
    return;
  }
  const detail = allParts
    .map(
      (p) =>
        `<button class="ac-link" data-type="${p.type}" data-id="${p.id}">${escHtml(`+${p.save_bonus} (${p.name})`)}</button>`
    )
    .join(" ");
  ds.innerHTML = `<span class="ac-equation">+${total} to rolls</span><span class="ac-detail" hidden>${detail}</span>`;
  ds.onclick = (e) => {
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
    ds.querySelector(".ac-equation").hidden ^= true;
    ds.querySelector(".ac-detail").hidden ^= true;
  };
}

document.getElementById("save-bonus-breakdown")?.addEventListener("click", (e) => {
  const btn = e.target.closest(".ac-link");
  if (!btn) return;
  const { type, id } = btn.dataset;
  const selector =
    type === "item"
      ? `.del-item-btn[data-id="${id}"]`
      : `.del-ability-btn[data-id="${id}"]`;
  const card = document
    .querySelector(selector)
    ?.closest(type === "item" ? ".item-card" : ".ability-card");
  if (!card) return;
  card.scrollIntoView({ behavior: "smooth", block: "nearest" });
  card.classList.add("ac-highlight");
  setTimeout(() => card.classList.remove("ac-highlight"), 1200);
});

// ── Money ────────────────────────────────────────────────────────────────────

function renderMoney() {
  ["pp", "gp", "sp", "cp"].forEach((coin) => {
    const el = document.getElementById(`money-${coin}`);
    el.textContent = char[`coins_${coin}`] ?? 0;
  });
}

function editCoin(el) {
  const coin = el.dataset.coin;
  const current = char[coin] ?? 0;
  const input = document.createElement("input");
  input.type = "number";
  input.min = 0;
  input.value = current;
  input.style.cssText =
    "width:4rem;font-size:1.2rem;font-weight:bold;background:#0f3460;border:1px solid var(--accent);color:var(--accent2);border-radius:4px;text-align:center;";
  el.replaceWith(input);
  input.focus();
  input.select();
  const save = async () => {
    const val = Math.max(0, parseInt(input.value, 10) || 0);
    await patchChar({ [coin]: val });
    input.replaceWith(el);
    el.textContent = val;
  };
  input.onblur = save;
  input.onkeydown = (e) => {
    if (e.key === "Enter") save();
    if (e.key === "Escape") { input.value = current; input.blur(); }
  };
}

document.querySelectorAll(".money-val").forEach((el) => {
  el.style.cursor = "pointer";
  el.addEventListener("click", () => editCoin(el));
});

// ── Hit Dice ────────────────────────────────────────────────────────────────

function renderHdPips() {
  const dieType = char.hit_die || "d10";
  document.getElementById("hd-label").textContent = `Hit Dice (${dieType})`;
  const container = document.getElementById("hd-pips");
  container.innerHTML = "";
  for (let i = 0; i < char.level; i++) {
    const filled = i < char.hit_dice_remaining;
    const btn = document.createElement("button");
    btn.className = `die-pip ${dieType}-pip` + (filled ? " die-filled" : "");
    btn.title = filled ? `Spend die ${i + 1}` : `Recover die ${i + 1}`;
    btn.innerHTML = dieSvg(dieType);
    btn.addEventListener("click", async () => {
      const next = filled ? i : i + 1;
      await patchChar({ hit_dice_remaining: next });
      renderHdPips();
    });
    container.appendChild(btn);
  }
}

// ── Death Saves ─────────────────────────────────────────────────────────────

function renderDeathSaves() {
  ["success", "failure"].forEach((type) => {
    const count =
      type === "success" ? char.death_save_successes : char.death_save_failures;
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
  const next = idx < current ? idx : idx + 1;
  await patchChar({ death_save_successes: Math.min(3, next) });
  renderDeathSaves();
  updateDeathSaveOdds();
});

document.getElementById("ds-failures").addEventListener("click", async (e) => {
  const pip = e.target.closest(".ds-pip");
  if (!pip) return;
  const idx = Number(pip.dataset.idx);
  const current = char.death_save_failures;
  const next = idx < current ? idx : idx + 1;
  await patchChar({ death_save_failures: Math.min(3, next) });
  renderDeathSaves();
  updateDeathSaveOdds();
});

document.getElementById("reset-death-saves").onclick = async () => {
  await patchChar({ death_save_successes: 0, death_save_failures: 0 });
  renderDeathSaves();
  updateDeathSaveOdds();
};

// ── Goodberries ─────────────────────────────────────────────────────────────

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
      const next = i < count ? i : i + 1;
      await patchChar({ goodberries: next });
      renderTomatoes();
      document.getElementById("tomato-count").textContent = char.goodberries;
    });
    container.appendChild(btn);
  }
  document.getElementById("tomato-count").textContent = count;
}

// ── HP / Temp HP ────────────────────────────────────────────────────────────

function updateHpDisplay() {
  document.getElementById("hp-display").textContent = char.hp;
  document.getElementById("hp-max-display").textContent = `${char.max_hp} max`;
}

function updateThpDisplay() {
  document.getElementById("thp-display").textContent = char.temp_hp ?? 0;
}

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

document.getElementById("thp-down").onclick = async () => {
  if ((char.temp_hp ?? 0) <= 0) return;
  await patchChar({ temp_hp: char.temp_hp - 1 });
  updateThpDisplay();
};

document.getElementById("thp-up").onclick = async () => {
  await patchChar({ temp_hp: (char.temp_hp ?? 0) + 1 });
  updateThpDisplay();
};

// ── Notes ───────────────────────────────────────────────────────────────────

document.getElementById("save-notes-btn").onclick = async () => {
  await patchChar({ notes: document.getElementById("notes-area").value });
  document.getElementById("save-notes-btn").textContent = "Saved!";
  setTimeout(() => {
    document.getElementById("save-notes-btn").textContent = "Save Notes";
  }, 1500);
};

// ── Inline stat edit ────────────────────────────────────────────────────────

function editStat(stat) {
  const box = document.querySelector(`.stat-box[data-stat="${stat}"]`);
  const valEl = box.querySelector(".stat-val");
  const current = char[stat];
  const input = document.createElement("input");
  input.type = "number";
  input.min = 1;
  input.max = 30;
  input.value = current;
  input.style.cssText =
    "width:3rem;font-size:1.2rem;background:#0f3460;border:1px solid #e94560;color:#e0e0e0;border-radius:4px;text-align:center;";
  valEl.replaceWith(input);
  input.focus();
  const save = async () => {
    const val = Math.min(30, Math.max(1, Number(input.value) || current));
    await patchChar({ [stat]: val });
    input.replaceWith(valEl);
    valEl.textContent = val;
    box.querySelector(".stat-mod").textContent = modifier(val);
    renderSkills();
  };
  input.onblur = save;
  input.onkeydown = (e) => {
    if (e.key === "Enter") save();
    if (e.key === "Escape") {
      input.value = current;
      input.blur();
    }
  };
}

// ── Rest ────────────────────────────────────────────────────────────────────

async function doRest(type) {
  const res = await apiFetch(
    `/api/characters/${CHARACTER_ID}/rest`,
    { method: "POST", body: { type } },
    "Rest failed — check your connection."
  );
  if (!res) return;

  const updated = await fetch(`/api/characters/${CHARACTER_ID}`);
  char = await updated.json();
  renderCharacter();
  loadAbilities();

  const label =
    type === "short"
      ? "Short rest taken."
      : "Long rest taken — HP, abilities, and hit dice restored.";
  const fb = document.getElementById("rest-feedback");
  fb.textContent = label;
  fb.hidden = false;
  setTimeout(() => {
    fb.hidden = true;
  }, 3000);
}

document.getElementById("short-rest-btn").onclick = () => doRest("short");
document.getElementById("long-rest-btn").onclick = async () => {
  if (
    !confirm(
      "Take a long rest? This will restore HP, all abilities, and recover hit dice."
    )
  )
    return;
  doRest("long");
};

// ── Delete character ─────────────────────────────────────────────────────────

document.getElementById("delete-char-btn").onclick = async () => {
  if (!confirm(`Delete ${char.name}? This cannot be undone.`)) return;
  const res = await apiFetch(
    `/api/characters/${CHARACTER_ID}`,
    { method: "DELETE" },
    "Failed to delete character."
  );
  if (!res) return;
  window.location.href = "/";
};
