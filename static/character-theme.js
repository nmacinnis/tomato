// Theme loading, applying, and modal.

const THEME_FIELDS = ["accent", "accent2", "bg", "surface", "panel_color", "border"];

const PRESETS = [
  { name: "Default",  accent: "#e94560", accent2: "#c7a026", bg: "#1a1a2e", surface: "#16213e", panel_color: "#0f3460", border: "#2a3a5e" },
  { name: "Crimson",  accent: "#e84040", accent2: "#e8a020", bg: "#1a0a0a", surface: "#2a1010", panel_color: "#3d1515", border: "#5a2020" },
  { name: "Forest",   accent: "#4caf7d", accent2: "#a0c840", bg: "#0a1a0e", surface: "#102016", panel_color: "#153520", border: "#1e4a28" },
  { name: "Arcane",   accent: "#a855f7", accent2: "#e879f9", bg: "#0e0a1a", surface: "#160f28", panel_color: "#1e1040", border: "#3a1e60" },
  { name: "Ember",    accent: "#f97316", accent2: "#fbbf24", bg: "#1a1008", surface: "#241808", panel_color: "#342210", border: "#4a3010" },
  { name: "Steel",    accent: "#94a3b8", accent2: "#64748b", bg: "#0f1117", surface: "#161b27", panel_color: "#1e2535", border: "#2a3548" },
];

let currentTheme = {};

// ── Apply / load ─────────────────────────────────────────────────────────────

function applyTheme(theme) {
  const root = document.documentElement.style;
  root.setProperty("--accent",  theme.accent);
  root.setProperty("--accent2", theme.accent2);
  root.setProperty("--bg",      theme.bg);
  root.setProperty("--surface", theme.surface);
  root.setProperty("--panel",   theme.panel_color);
  root.setProperty("--border",  theme.border);
}

async function loadTheme() {
  const res = await fetch(`/api/characters/${CHARACTER_ID}/theme`);
  if (!res.ok) return;
  currentTheme = await res.json();
  applyTheme(currentTheme);
}

// ── Modal ────────────────────────────────────────────────────────────────────

const themeModal = document.getElementById("theme-modal");
const themeForm  = document.getElementById("theme-form");

function populatePresets() {
  const container = document.getElementById("theme-presets");
  PRESETS.forEach(preset => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theme-preset-btn";
    btn.title = preset.name;
    btn.style.cssText = `background:${preset.surface};border-color:${preset.accent};`;
    btn.innerHTML = `
      <span class="preset-swatch" style="background:${preset.accent}"></span>
      <span class="preset-swatch" style="background:${preset.accent2}"></span>
      <span class="preset-name">${preset.name}</span>
    `;
    btn.addEventListener("click", () => applyPresetToForm(preset));
    container.appendChild(btn);
  });
}

function applyPresetToForm(preset) {
  THEME_FIELDS.forEach(f => {
    const input = themeForm.elements[f];
    if (input) input.value = preset[f];
  });
  // Live preview
  applyTheme(preset);
}

function openThemeModal() {
  // Populate pickers with current theme values
  THEME_FIELDS.forEach(f => {
    const input = themeForm.elements[f];
    if (input) input.value = currentTheme[f] || "";
  });
  themeModal.showModal();
}

document.getElementById("theme-btn").onclick    = openThemeModal;
document.getElementById("cancel-theme").onclick = () => {
  applyTheme(currentTheme); // revert live preview
  themeModal.close();
};

// Live preview on color picker change
themeForm.addEventListener("input", () => {
  const preview = Object.fromEntries(
    THEME_FIELDS.map(f => [f, themeForm.elements[f]?.value || currentTheme[f]])
  );
  applyTheme(preview);
});

themeForm.onsubmit = async (e) => {
  e.preventDefault();
  const theme = Object.fromEntries(
    THEME_FIELDS.map(f => [f, themeForm.elements[f].value])
  );
  const res = await apiFetch(
    `/api/characters/${CHARACTER_ID}/theme`,
    { method: "PUT", body: theme },
    "Failed to save theme."
  );
  if (!res) { applyTheme(currentTheme); return; }
  currentTheme = theme;
  showToast("Theme saved!", "success");
  themeModal.close();
};

populatePresets();
loadTheme();
