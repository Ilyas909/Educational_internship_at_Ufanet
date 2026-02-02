async function loadCard() {
  const res = await fetch(`/api/cards/${CARD_ID}`);
  const card = await res.json();

  const start = new Date(card.discount_start).toLocaleDateString('ru-RU');
  const end = new Date(card.discount_end).toLocaleDateString('ru-RU');

  document.getElementById('card-detail').innerHTML = `
    <h2>${card.title}</h2>
    <p><span class="label">Компания:</span> <span class="value">${card.company_name}</span></p>
    <p><span class="label">Скидка:</span> <span class="value">${card.commission}%</span></p>
    ${card.promo_code ? `<p><span class="label">Промокод:</span> <span class="promo-code">${card.promo_code}</span></p>` : ''}
    <p><span class="label">Период действия:</span> <span class="value">с ${start} по ${end}</span></p>
  `;
}
loadCard();