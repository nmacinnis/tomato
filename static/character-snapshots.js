// Snapshots (take / restore / delete) and Level-up (preview, then confirm).
// See GLOSSARY.md: a Snapshot holds Play state (not notes); Level-up moves to the
// next level the Sheet describes and is undone by restoring its automatic Snapshot.

const ORDINAL = ["", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"];
const FIELD_LABELS = {
  level: "Level",
  hp: "HP",
  max_hp: "Max HP",
  hit_dice_remaining: "Hit dice",
  ac: "AC",
  speed: "Speed",
  str: "STR",
  dex: "DEX",
  con: "CON",
  int: "INT",
  wis: "WIS",
  cha: "CHA",
  uses_max: "Max uses",
  uses_remaining: "Uses",
};

function fieldLabel(field) {
  const slot = field.match(/^spell_slots_(\d)_(max|remaining)$/);
  if (slot) return `${ORDINAL[slot[1]]}-level slots${slot[2] === "max" ? " (max)" : ""}`;
  return FIELD_LABELS[field] ?? field.replace(/_/g, " ");
}

function formatTakenAt(iso) {
  return new Date(iso).toLocaleString(undefined, {
    weekday: "short",
    day: "numeric",
    month: "short",
    hour: "numeric",
    minute: "2-digit",
  });
}

async function refreshAfterStateChange() {
  await loadCharacter();
  await Promise.all([loadSnapshots(), loadLevelUp()]);
}

// ── Snapshots ────────────────────────────────────────────────────────────────

async function loadSnapshots() {
  const res = await apiFetch(`/api/characters/${CHARACTER_ID}/snapshots`, {}, "Couldn't load snapshots.");
  if (!res) return;
  const snaps = await res.json();
  const list = document.getElementById("snapshot-list");
  if (!snaps.length) {
    list.innerHTML = `<li class="snapshot-empty">No snapshots yet.</li>`;
    return;
  }
  list.innerHTML = snaps
    .map(
      (s) => `
    <li class="snapshot-item${s.automatic ? " snapshot-auto" : ""}">
      <div class="snapshot-info">
        <span class="snapshot-label">${escHtml(s.label || "Snapshot")}</span>
        <span class="snapshot-meta">${escHtml(formatTakenAt(s.taken_at))} · Level ${s.level}</span>
      </div>
      <button class="btn btn-sm" data-restore="${s.id}">Restore</button>
      <button class="btn btn-sm btn-danger" data-delete="${s.id}" title="Delete snapshot">✕</button>
    </li>`
    )
    .join("");
  list.querySelectorAll("[data-restore]").forEach((btn) => {
    const s = snaps.find((x) => x.id === Number(btn.dataset.restore));
    btn.onclick = () => restoreSnapshot(s);
  });
  list.querySelectorAll("[data-delete]").forEach((btn) => {
    const s = snaps.find((x) => x.id === Number(btn.dataset.delete));
    btn.onclick = () => deleteSnapshot(s);
  });
}

document.getElementById("snapshot-form").onsubmit = async (e) => {
  e.preventDefault();
  const input = e.target.label;
  const res = await apiFetch(
    `/api/characters/${CHARACTER_ID}/snapshots`,
    { method: "POST", body: { label: input.value } },
    "Couldn't take snapshot."
  );
  if (!res) return;
  input.value = "";
  showToast("Snapshot taken.", "success");
  loadSnapshots();
};

async function restoreSnapshot(s) {
  const name = s.label ? `“${s.label}”` : "this snapshot";
  const when = `${formatTakenAt(s.taken_at)}, level ${s.level}`;
  if (!confirm(`Restore ${name} (${when})?\n\nYour current state will be snapshotted first.`)) return;
  const res = await fetch(`/api/snapshots/${s.id}/restore`, { method: "POST" });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    showToast(body.error || "Restore failed.");
    return;
  }
  showToast(`Restored ${name}.`, "success");
  refreshAfterStateChange();
}

async function deleteSnapshot(s) {
  const name = s.label ? `“${s.label}”` : `the snapshot from ${formatTakenAt(s.taken_at)}`;
  if (!confirm(`Delete ${name}? This cannot be undone.`)) return;
  const res = await apiFetch(`/api/snapshots/${s.id}`, { method: "DELETE" }, "Couldn't delete snapshot.");
  if (res) loadSnapshots();
}

// ── Level-up ─────────────────────────────────────────────────────────────────

let levelUpPreview = null;

async function loadLevelUp() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/level-up`);
  const btn = document.getElementById("level-up-btn");
  if (!res.ok) {
    btn.hidden = true;
    return;
  }
  const body = await res.json();
  levelUpPreview = body.preview;
  btn.hidden = !body.available;
  if (body.available) btn.textContent = `Level up → ${levelUpPreview.to_level}`;
}

function renderChangeList(title, changes) {
  if (!changes.length) return "";
  const rows = changes
    .map(
      (c) =>
        `<li><span>${escHtml(fieldLabel(c.field))}</span> <span class="lu-before">${escHtml(String(c.before ?? "—"))}</span> → <strong>${escHtml(String(c.after ?? "—"))}</strong></li>`
    )
    .join("");
  return `<h3>${escHtml(title)}</h3><ul class="lu-changes">${rows}</ul>`;
}

function renderRowChanges(noun, rows) {
  let html = "";
  if (rows.gained.length)
    html += `<h3>New ${noun}</h3><ul class="lu-changes">${rows.gained.map((n) => `<li class="lu-gained">+ ${escHtml(n)}</li>`).join("")}</ul>`;
  if (rows.retired.length)
    html += `<h3>Retired ${noun}</h3><ul class="lu-changes">${rows.retired.map((n) => `<li class="lu-retired">− ${escHtml(n)}</li>`).join("")}</ul>`;
  rows.changed.forEach((r) => {
    html += renderChangeList(r.name, r.changes);
  });
  return html;
}

function renderLevelUpPreview(p) {
  const play = new Set(["hp", "hit_dice_remaining", ...ORDINAL.slice(1).map((_, i) => `spell_slots_${i + 1}_remaining`)]);
  const sheet = p.character.filter((c) => !play.has(c.field) && c.field !== "level");
  const current = p.character.filter((c) => play.has(c.field));
  return (
    renderChangeList("Sheet", sheet) +
    renderChangeList("Current values after levelling", current) +
    renderRowChanges("abilities", p.abilities) +
    renderRowChanges("items", p.items) || "<p>Nothing changes at this level.</p>"
  );
}

document.getElementById("level-up-btn").onclick = async () => {
  await loadLevelUp(); // fresh preview: current values may have changed since page load
  if (!levelUpPreview) return;
  document.getElementById("level-up-title").textContent =
    `Level ${levelUpPreview.from_level} → ${levelUpPreview.to_level}`;
  document.getElementById("confirm-level-up").textContent = `Level up to ${levelUpPreview.to_level}`;
  document.getElementById("level-up-preview").innerHTML = renderLevelUpPreview(levelUpPreview);
  document.getElementById("level-up-modal").showModal();
};

document.getElementById("cancel-level-up").onclick = () => document.getElementById("level-up-modal").close();

document.getElementById("confirm-level-up").onclick = async () => {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/level-up`, { method: "POST" });
  document.getElementById("level-up-modal").close();
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    showToast(body.error || "Level-up failed.");
    return;
  }
  const done = await res.json();
  showToast(`Reached level ${done.to_level}!`, "success");
  refreshAfterStateChange();
};

loadSnapshots();
loadLevelUp();
