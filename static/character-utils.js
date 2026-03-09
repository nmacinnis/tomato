// Shared mutable state (accessible as globals across all character-*.js files)
let char = null;
let currentItems = [];
let superiorityDie = null;
let secondWind = null;

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

// ── Alignment abbreviation ───────────────────────────────────────────────────

const ALIGNMENT_ABBR = {
  "lawful good":      "LG", "neutral good":  "NG", "chaotic good":    "CG",
  "lawful neutral":   "LN", "true neutral":  "N",  "chaotic neutral": "CN",
  "lawful evil":      "LE", "neutral evil":  "NE", "chaotic evil":    "CE",
  "unaligned":        "U",
};

function abbreviateAlignment(a) {
  return ALIGNMENT_ABBR[a.toLowerCase().trim()] ?? a;
}

// ── Shared utilities ────────────────────────────────────────────────────────

function profBonus(level) {
  return Math.floor((level - 1) / 4) + 2;
}

// ── Dice SVG icons ──────────────────────────────────────────────────────────
// d8  — symmetric diamond (octahedron front view)
// d10 — asymmetric kite   (equator sits at ~70% height)

function dieSvg(type) {
  const base = `fill="none" xmlns="http://www.w3.org/2000/svg" width="18" height="20" aria-hidden="true"`;
  if (type === 'd6') return `<svg viewBox="0 0 16 16" ${base}>
    <rect x="1.5" y="1.5" width="13" height="13" rx="2.5" stroke="currentColor" stroke-width="1.5"/>
  </svg>`;
  if (type === 'd8') return `<svg viewBox="0 0 16 18" ${base}>
    <polygon points="8,1 15,9 8,17 1,9" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
    <line x1="1" y1="9" x2="15" y2="9" stroke="currentColor" stroke-width="1" stroke-linecap="round"/>
    <line x1="8" y1="1" x2="8"  y2="17" stroke="currentColor" stroke-width="1" stroke-linecap="round"/>
  </svg>`;
  return `<svg viewBox="0 0 16 18" ${base}>
    <polygon points="8,1 15,13 8,17 1,13" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
    <line x1="1" y1="13" x2="15" y2="13" stroke="currentColor" stroke-width="1" stroke-linecap="round"/>
    <line x1="8" y1="1"  x2="8"  y2="17" stroke="currentColor" stroke-width="1" stroke-linecap="round"/>
  </svg>`;
}
