// Skills panel — standard skills and tool proficiencies from inventory.

const SKILLS = [
  { name: "Acrobatics",      key: "acrobatics",      stat: "dex" },
  { name: "Animal Handling", key: "animal_handling",  stat: "wis" },
  { name: "Arcana",          key: "arcana",           stat: "int" },
  { name: "Athletics",       key: "athletics",        stat: "str" },
  { name: "Deception",       key: "deception",        stat: "cha" },
  { name: "History",         key: "history",          stat: "int" },
  { name: "Insight",         key: "insight",          stat: "wis" },
  { name: "Intimidation",    key: "intimidation",     stat: "cha" },
  { name: "Investigation",   key: "investigation",    stat: "int" },
  { name: "Medicine",        key: "medicine",         stat: "wis" },
  { name: "Nature",          key: "nature",           stat: "int" },
  { name: "Perception",      key: "perception",       stat: "wis" },
  { name: "Performance",     key: "performance",      stat: "cha" },
  { name: "Persuasion",      key: "persuasion",       stat: "cha" },
  { name: "Religion",        key: "religion",         stat: "int" },
  { name: "Sleight of Hand", key: "sleight_of_hand",  stat: "dex" },
  { name: "Stealth",         key: "stealth",          stat: "dex" },
  { name: "Survival",        key: "survival",         stat: "wis" },
];

function renderSkills() {
  const grid = document.getElementById("skills-grid");
  if (!grid) return;
  const prof = profBonus(char.level);
  const skillProfs = new Set((char.skill_proficiencies || "").split(",").map(s => s.trim()).filter(Boolean));

  grid.innerHTML = "";

  SKILLS.forEach(skill => {
    const proficient = skillProfs.has(skill.key);
    const mod = Math.floor((char[skill.stat] - 10) / 2);
    const total = mod + (proficient ? prof : 0);
    const sign = total >= 0 ? "+" : "";

    const row = document.createElement("div");
    row.className = "skill-row" + (proficient ? " skill-proficient" : "");
    row.title = "Click to toggle proficiency";
    row.innerHTML = `
      <span class="skill-pip">${proficient ? "●" : "○"}</span>
      <span class="skill-name">${skill.name}</span>
      <span class="skill-stat">${skill.stat.toUpperCase()}</span>
      <span class="skill-val">${sign}${total}</span>
    `;
    row.addEventListener("click", async () => {
      const next = new Set(skillProfs);
      if (proficient) next.delete(skill.key); else next.add(skill.key);
      await patchChar({ skill_proficiencies: [...next].join(",") });
      renderSkills();
    });
    grid.appendChild(row);
  });

  const tools = currentItems.filter(i => i.tool_proficient);
  if (tools.length) {
    const divider = document.createElement("div");
    divider.className = "skill-divider";
    divider.textContent = "Tools";
    grid.appendChild(divider);

    tools.forEach(tool => {
      const row = document.createElement("div");
      row.className = "skill-row skill-proficient";
      row.innerHTML = `
        <span class="skill-pip">●</span>
        <span class="skill-name">${escHtml(tool.name)}</span>
        <span class="skill-stat">—</span>
        <span class="skill-val">+${prof}</span>
      `;
      grid.appendChild(row);
    });
  }
}
