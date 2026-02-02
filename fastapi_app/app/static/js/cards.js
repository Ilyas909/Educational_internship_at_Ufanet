// Глобальные переменные (объявляем, но не инициализируем до DOMContentLoaded)
let currentCardId = null;
let titleEl, companyEl, promoEl, commissionEl, startEl, endEl, saveBtn, modal;

// ======================
// ФУНКЦИИ ВАЛИДАЦИИ
// ======================

function showError(fieldId, message) {
    const errorEl = document.getElementById(`${fieldId}-error`);
    if (errorEl) errorEl.textContent = message;
    const input = document.getElementById(fieldId);
    if (input) input.style.border = '2px solid var(--danger)';
}

function hideError(fieldId) {
    const errorEl = document.getElementById(`${fieldId}-error`);
    if (errorEl) errorEl.textContent = '';
    const input = document.getElementById(fieldId);
    if (input) input.style.border = '';
}

function validateForm() {
    let isValid = true;

    // Название
    if (!titleEl.value.trim()) {
        showError('title', 'Обязательное поле');
        isValid = false;
    } else {
        hideError('title');
    }

    // Компания
    if (!companyEl.value.trim()) {
        showError('company', 'Обязательное поле');
        isValid = false;
    } else {
        hideError('company');
    }

    // Скидка
    const commissionValue = commissionEl.value.trim();
    if (!commissionValue) {
        showError('commission', 'Обязательное поле');
        isValid = false;
    } else {
        const num = parseFloat(commissionValue);
        if (isNaN(num) || num < 0) {
            showError('commission', 'Должно быть число ≥ 0');
            isValid = false;
        } else {
            hideError('commission');
            commissionEl.value = num.toString(); // нормализация
        }
    }

    // Дата начала
if (!startEl.value) {
    showError('start', 'Укажите дату начала');
    isValid = false;
} else {
    hideError('start');
}

// Дата окончания
if (!endEl.value) {
    showError('end', 'Укажите дату окончания');
    isValid = false;
} else {
    hideError('end');
}

// Сравнение дат и проверка против "сегодня"
if (startEl.value && endEl.value) {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // обнуляем время для корректного сравнения

    const startDate = new Date(startEl.value);
    const endDate = new Date(endEl.value);

    // 1. Окончание не может быть раньше начала
    if (startDate > endDate) {
        showError('start', 'Дата начала не может быть позже окончания');
        showError('end', 'Дата окончания не может быть раньше начала');
        isValid = false;
    } else {
        hideError('start');
        hideError('end');
    }

    // 2. Окончание не может быть раньше сегодня
    if (endDate < today) {
        showError('end', 'Дата окончания не может быть в прошлом');
        isValid = false;
    } else {
        // Только если предыдущая ошибка не активна
        if (!document.getElementById('end-error').textContent.includes('раньше начала')) {
            hideError('end');
        }
    }
}

    return isValid;
}

// ======================
// МОДАЛЬНЫЕ ОКНА И УПРАВЛЕНИЕ ФОРМОЙ
// ======================

function resetValidation() {
    [titleEl, companyEl, commissionEl, startEl, endEl].forEach(el => {
        if (el) el.style.border = '';
    });
    ['title', 'company', 'commission', 'start', 'end'].forEach(id => {
        const err = document.getElementById(`${id}-error`);
        if (err) err.textContent = '';
    });
    if (saveBtn) saveBtn.disabled = true;
}

function openModal(card) {
    currentCardId = card.id;
    modal.classList.remove('hidden');
    resetValidation();

    titleEl.value = card.title || '';
    companyEl.value = card.company_name || '';
    promoEl.value = card.promo_code || '';
    commissionEl.value = card.commission != null ? String(card.commission) : '';
    startEl.value = card.discount_start || '';
    endEl.value = card.discount_end || '';

    setTimeout(() => {
        const isNowValid = validateForm();
        if (saveBtn) saveBtn.disabled = !isNowValid;
    }, 0);
}

function addCard() {
    currentCardId = null;
    modal.classList.remove('hidden');
    resetValidation();

    titleEl.value = '';
    companyEl.value = '';
    promoEl.value = '';
    commissionEl.value = '';
    startEl.value = '';
    endEl.value = '';
}

function closeModal(e) {
    if (e.target.id === 'modal') {
        modal.classList.add('hidden');
        currentCardId = null;
    }
}

// ======================
// РАБОТА С ДАННЫМИ
// ======================

async function loadCards() {
    try {
        const res = await fetch(`/api/cards/section/${SECTION_ID}`);
        const cards = await res.json();

        const grid = document.getElementById('cards');
        grid.innerHTML = '';

        cards.forEach(c => {
            const card = document.createElement('div');
            card.className = 'card';

            card.innerHTML = `
                <h3>${c.title}</h3>
                <p>${c.company_name}</p>
                <p>${c.commission ?? ''}</p>
                <button onclick="deleteCard(${c.id}, event)">🗑</button>
            `;

            card.onclick = () => openModal(c);
            grid.appendChild(card);
        });
    } catch (err) {
        console.error('Ошибка загрузки карточек:', err);
        alert('Не удалось загрузить карточки.');
    }
}

async function saveCard() {
    const data = {
        title: titleEl.value.trim(),
        company_name: companyEl.value.trim(),
        promo_code: promoEl.value.trim() || null,
        commission: parseFloat(commissionEl.value),
        discount_start: startEl.value,
        discount_end: endEl.value,
        section_id: SECTION_ID
    };

    try {
        if (currentCardId) {
            await fetch(`/api/cards/${currentCardId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            await fetch('/api/cards', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        modal.classList.add('hidden');
        loadCards();
    } catch (err) {
        console.error('Ошибка сохранения:', err);
        alert('Не удалось сохранить карточку.');
    }
}

async function deleteCard(id, e) {
    e.stopPropagation();
    if (!confirm("Удалить карточку?")) return;

    try {
        await fetch(`/api/cards/${id}`, { method: 'DELETE' });
        loadCards();
    } catch (err) {
        console.error('Ошибка удаления:', err);
        alert('Не удалось удалить карточку.');
    }
}

// ======================
// ИНИЦИАЛИЗАЦИЯ ПОСЛЕ ЗАГРУЗКИ DOM
// ======================

document.addEventListener('DOMContentLoaded', () => {
    // Получаем ссылки на элементы
    titleEl = document.getElementById('title');
    companyEl = document.getElementById('company');
    promoEl = document.getElementById('promo');
    commissionEl = document.getElementById('commission');
    startEl = document.getElementById('start');
    endEl = document.getElementById('end');
    saveBtn = document.getElementById('save-btn');
    modal = document.getElementById('modal');

    // Привязываем обработчики ввода
    [titleEl, companyEl, commissionEl, startEl, endEl].forEach(el => {
        if (el) {
            el.addEventListener('input', () => {
                const isNowValid = validateForm();
                if (saveBtn) saveBtn.disabled = !isNowValid;
            });
        }
    });

    // Загружаем карточки
    loadCards();
});


