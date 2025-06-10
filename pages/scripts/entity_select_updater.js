/**
 * Универсальный менеджер для обновления и удаления выпадающих списков в модальном окне:
 * - Предметы (subjects)
 * - Аудитории (rooms)
 * - Преподаватели (teachers)
 */

async function updateEntitySelect(selector, storageKey, placeholder, field) {
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
            if (!resp.ok) throw new Error(`HTTP error! Status: ${resp.status}`);
            items = await resp.json();
        } catch (e) {
            console.error(`Ошибка загрузки ${storageKey}:`, e);
            alert(`Не удалось загрузить ${storageKey}. Проверьте сервер.`);
            items = [];
        }
    }
    items.forEach(item => {
        const value = item[field] || item; // Используем указанное поле или сам объект
        const text = item[field] || item;  // Для совместимости со строками из localStorage
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        select.appendChild(option);
    });
}

// Обновить все списки
function updateAllEntitySelects() {
    updateEntitySelect('.subject-select', 'subjects', '-- Выберите предмет --', 'name');
    updateEntitySelect('.room-select', 'rooms', '-- Выберите аудиторию --', 'number');
    updateEntitySelect('.teacher-select', 'teachers', '-- Выберите преподавателя --', 'full_name');
}

// Удаление сущности
async function delEntity(entityType, value) {
    if (!entityType || !value) return;

    if (window.DATA_SOURCE === "localstorage") {
        let items = JSON.parse(localStorage.getItem(entityType) || '[]');
        items = items.filter(item => item !== value);
        localStorage.setItem(entityType, JSON.stringify(items));
        updateAllEntitySelects(); // Обновляем все списки
        window.dispatchEvent(new Event('storage')); // Уведомляем другие вкладки
    } else {
        let url = '';
        if (entityType === 'subjects') url = `http://localhost:8000/api/subjects/${encodeURIComponent(value)}/`;
        if (entityType === 'rooms') url = `http://localhost:8000/api/rooms/${encodeURIComponent(value)}/`;
        if (entityType === 'teachers') url = `http://localhost:8000/api/teachers/${encodeURIComponent(value)}/`;
        try {
            const response = await fetch(url, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            console.log(`${entityType} удалён: ${value}`);
            updateAllEntitySelects(); // Обновляем списки после удаления
        } catch (error) {
            console.error(`Ошибка при удалении ${entityType}:`, error);
            alert(`Не удалось удалить ${entityType}: ${value}. Проверьте сервер.`);
        }
    }
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

    // Обработчик удаления (например, если кнопки добавлены динамически)
    document.addEventListener('click', function(e) {
        const deleteBtn = e.target.closest('.delete-btn');
        if (deleteBtn) {
            const entityType = deleteBtn.dataset.entityType; // Предполагаем атрибут data-entity-type
            const value = deleteBtn.dataset.value; // Предполагаем атрибут data-value
            if (entityType && value) {
                delEntity(entityType, value);
            }
        }
    });
});