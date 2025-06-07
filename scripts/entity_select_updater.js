/**
 * Универсальный менеджер для обновления выпадающих списков в модальном окне:
 * - Предметы (subjects)
 * - Аудитории (rooms)
 * - Преподаватели (teachers)
 */

function updateEntitySelect(selector, storageKey, placeholder) {
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
    // Получаем значения из localStorage
    const items = JSON.parse(localStorage.getItem(storageKey) || '[]');
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
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