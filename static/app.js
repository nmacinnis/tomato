// Shared utilities used by both index and character pages

async function loadCharacters() {
  const grid = document.getElementById("characters-grid");
  const emptyMsg = document.getElementById("empty-msg");
  if (!grid) return;

  const res = await fetch("/api/characters");
  const chars = await res.json();

  if (chars.length === 0) {
    emptyMsg.hidden = false;
    return;
  }

  emptyMsg.hidden = true;
  grid.innerHTML = "";

  chars.forEach(c => {
    const card = document.createElement("div");
    card.className = "char-card";
    card.innerHTML = `
      <h3>${escHtml(c.name)}</h3>
      <p>${escHtml(c.race)} ${escHtml(c.class)} — Level ${c.level}</p>
      <p>HP: ${c.hp} / ${c.max_hp} &nbsp;|&nbsp; AC: ${c.ac}</p>
    `;
    card.onclick = () => (window.location.href = `/character/${c.id}`);
    grid.appendChild(card);
  });
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function modifier(score) {
  const mod = Math.floor((score - 10) / 2);
  return mod >= 0 ? `+${mod}` : `${mod}`;
}
