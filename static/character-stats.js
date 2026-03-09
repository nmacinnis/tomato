// Stats, HP, hit dice, death saves, goodberries, notes, rest, delete.

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
  updateThpDisplay();
  document.getElementById("ac-val").textContent = char.ac;
  document.getElementById("speed-val").textContent = `${char.speed} ft`;
  document.getElementById("level-val").textContent = char.level;
  document.getElementById("notes-area").value = char.notes || "";

  const dexMod = Math.floor((char.dex - 10) / 2);
  const wisMod = Math.floor((char.wis - 10) / 2);
  document.getElementById("prof-val").textContent = `+${prof}`;
  document.getElementById("init-val").textContent = dexMod >= 0 ? `+${dexMod}` : `${dexMod}`;
  document.getElementById("perc-val").textContent = 10 + wisMod + prof;
  const strMod = Math.floor((char.str - 10) / 2);
  document.getElementById("maneuver-dc-val").textContent = 8 + prof + Math.max(strMod, dexMod);
  document.getElementById("alignment-val").textContent = abbreviateAlignment(char.alignment || "");
  document.getElementById("size-val").textContent = char.size || "";
  document.getElementById("height-val").textContent = char.height || "";
  document.getElementById("weight-val").textContent = char.weight || "";

  renderHdPips();
  renderDeathSaves();
  renderTomatoes();
}

// ── Hit Dice ────────────────────────────────────────────────────────────────

function renderHdPips() {
  const container = document.getElementById("hd-pips");
  container.innerHTML = "";
  for (let i = 0; i < char.level; i++) {
    const filled = i < char.hit_dice_remaining;
    const btn = document.createElement("button");
    btn.className = "die-pip d10-pip" + (filled ? " die-filled" : "");
    btn.title = filled ? `Spend die ${i + 1}` : `Recover die ${i + 1}`;
    btn.innerHTML = dieSvg('d10');
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
  setTimeout(() => { document.getElementById("save-notes-btn").textContent = "Save Notes"; }, 1500);
};

// ── Inline stat edit ────────────────────────────────────────────────────────

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
    renderSkills();
  };
  input.onblur = save;
  input.onkeydown = e => { if (e.key === "Enter") save(); if (e.key === "Escape") { input.value = current; input.blur(); } };
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

// ── Delete character ─────────────────────────────────────────────────────────

document.getElementById("delete-char-btn").onclick = async () => {
  if (!confirm(`Delete ${char.name}? This cannot be undone.`)) return;
  const res = await apiFetch(`/api/characters/${CHARACTER_ID}`, { method: "DELETE" }, "Failed to delete character.");
  if (!res) return;
  window.location.href = "/";
};
