async function loadSections() {
  const res = await fetch('/api/sections');
  const sections = await res.json();
  const grid = document.getElementById('sections');
  grid.innerHTML = sections.map(s => `
    <div class="card" onclick="location.href='/public/sections/${s.id}'">
      <h3>${s.title}</h3>
    </div>
  `).join('');
}
loadSections();