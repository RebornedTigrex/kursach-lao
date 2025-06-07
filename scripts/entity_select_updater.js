/**
 * Универсальный менеджер для обновления выпадающих списков в модальном окне:
 * - Предметы (subjects)
 * - Аудитории (rooms)
 * - Преподаватели (teachers)
 */

async function updateEntitySelect(selector, storageKey, placeholder) {
    const select = document.querySelector(selector);
    if (!select) return;
    // Сохраняем первую опцию (заглушку)
    const firstOption = select.querySelector('option[value=""]');
    select.innerHTML = '';
    if (firstOption) select.appendChild(firstOption);
    else if (placeholder) {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = placeholder;
        select.appendChild(opt);
    }
    let items = [];
    if (window.DATA_SOURCE === "localstorage") {
        items = JSON.parse(localStorage.getItem(storageKey) || '[]');
    } else {
        // Получаем значения из backend
        let url = '';
        if (storageKey === 'subjects') url = 'http://localhost:8000/api/subjects/';
        if (storageKey === 'rooms') url = 'http://localhost:8000/api/rooms/';
        if (storageKey === 'teachers') url = 'http://localhost:8000/api/teachers/';
        try {
            const resp = await fetch(url);
            items = await resp.json();
        } catch (e) {
            items = [];
        }
    }
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = typeof item === 'string' ? item : (item.name || item.number || item.full_name || '');
        option.textContent = typeof item === 'string' ? item : (item.name || item.number || item.full_name || '');
        select.appendChild(option);
    });
}

// Обновить все списки
function updateAllEntitySelects() {
    updateEntitySelect('.subject-select', 'subjects', '-- Выберите предмет --');
    updateEntitySelect('.room-select', 'rooms', '-- Выберите аудиторию --');
    updateEntitySelect('.teacher-select', 'teachers', '-- Выберите преподавателя --');
}

// Вызывать при открытии модального окна:
document.addEventListener('DOMContentLoaded', function() {
    // Открытие модального окна — обновляем все списки
    document.querySelector('.timetable').addEventListener('click', function(e) {
        const lesson = e.target.closest('.lesson');
        if (lesson) {
            updateAllEntitySelects();
        }
    });

    // Слушаем обновления из других вкладок/окон
    window.addEventListener('storage', function(e) {
        if (['subjects', 'rooms', 'teachers'].includes(e.key)) {
            updateAllEntitySelects();
        }
    });
});