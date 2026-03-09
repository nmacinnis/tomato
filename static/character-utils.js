// Shared mutable state (accessible as globals across all character-*.js files)
let char = null;
let currentItems = [];
let superiorityDie = null;

// ── Toast ───────────────────────────────────────────────────────────────────

function showToast(msg, type = "error") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// ── Fetch helper ────────────────────────────────────────────────────────────
// Auto-stringifies object bodies, sets Content-Type, shows toast on failure.
// Returns the Response on success, or null on failure.

async function apiFetch(url, opts = {}, errorMsg = "Request failed.") {
  const init = { ...opts };
  if (init.body !== undefined && typeof init.body !== "string") {
    init.body = JSON.stringify(init.body);
    init.headers = { "Content-Type": "application/json", ...(init.headers || {}) };
  }
  const res = await fetch(url, init);
  if (!res.ok) { showToast(errorMsg); return null; }
  return res;
}

// ── Character patch ─────────────────────────────────────────────────────────

async function patchChar(fields) {
  const res = await apiFetch(
    `/api/characters/${CHARACTER_ID}`,
    { method: "PUT", body: fields },
    "Failed to save — check your connection."
  );
  if (!res) return;
  Object.assign(char, fields);
}

// ── Shared utilities ────────────────────────────────────────────────────────

function profBonus(level) {
  return Math.floor((level - 1) / 4) + 2;
}
