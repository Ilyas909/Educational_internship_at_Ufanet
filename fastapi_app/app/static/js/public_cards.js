async function loadCards() {
  const secRes = await fetch(`/api/sections/${SECTION_ID}`);
  const section = await secRes.json();
  document.getElementById('section-title').textContent = section.title;

  const res = await fetch(`/api/cards/section/${SECTION_ID}`);
  const cards = await res.json();
  const grid = document.getElementById('cards');
  grid.innerHTML = cards.map(c => `
    <div class="card" onclick="location.href='/public/cards/${c.id}'">
      <h3>${c.title}</h3>
      <p>${c.company_name}</p>
      <p class="discount">${c.commission}% скидка</p>
    </div>
  `).join('');
}
loadCards();