async function loadSections() {
    const res = await fetch('/api/sections');
    const sections = await res.json();

    const grid = document.getElementById('sections');
    grid.innerHTML = '';

    sections.forEach(s => {
        const card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
            <h3>${s.title}</h3>
            <div class="section-actions">
                <button class="icon" onclick="openRenameModal(${s.id}, '${s.title}', event)">✏️</button>
                <button class="icon danger" onclick="deleteSection(${s.id}, event)">🗑</button>
            </div>
        `;

        card.onclick = () => {
            window.location = `/sections/${s.id}`;
        };

        grid.appendChild(card);
    });
}


async function deleteSection(id, e) {
    e.stopPropagation();
    if (!confirm("Удалить категорию?")) return;

    await fetch(`/api/sections/${id}`, {method: 'DELETE'});
    loadSections();
}


let currentSectionId = null;
function openRenameModal(id, title, e) {
    e.stopPropagation();

    currentSectionId = id;
    document.getElementById('section-title-input').value = title;
    document.getElementById('section-modal').classList.remove('hidden');
}
function closeSectionModal(e) {
    if (e.target.id === 'section-modal') {
        document.getElementById('section-modal').classList.add('hidden');
        currentSectionId = null;
    }
}
async function saveSectionTitle() {
    const title = document.getElementById('section-title-input').value.trim();
    if (!title) return;

    await fetch(`/api/sections/${currentSectionId}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title })
    });

    document.getElementById('section-modal').classList.add('hidden');
    currentSectionId = null;
    loadSections();
}


function openCreateSectionModal() {
    document.getElementById('new-section-title').value = '';
    document.getElementById('create-section-modal').classList.remove('hidden');
}
function closeCreateSectionModal(e) {
    if (e.target.id === 'create-section-modal') {
        document.getElementById('create-section-modal').classList.add('hidden');
    }
}

function validateCreateSection() {
    const title = document.getElementById('new-section-title').value.trim();
    const errorEl = document.getElementById('create-section-error');
    const btn = document.getElementById('create-section-btn');

    if (title === '') {
        errorEl.classList.remove('hidden');
        btn.disabled = true;
    } else {
        errorEl.classList.add('hidden');
        btn.disabled = false;
    }
}

async function createSection() {
    const title = document.getElementById('new-section-title').value.trim();

    // Дублируем проверку на случай, если кто-то вызовет функцию напрямую
    if (!title) {
        document.getElementById('create-section-error').classList.remove('hidden');
        return;
    }

    try {
        const res = await fetch('/api/sections', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ title })
        });

        if (!res.ok) throw new Error('Ошибка сервера');

        document.getElementById('create-section-modal').classList.add('hidden');
        loadSections();
    } catch (err) {
        alert('Не удалось создать секцию: ' + err.message);
    }
}


loadSections();
