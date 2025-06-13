/**
 * Универсальный менеджер для обновления выпадающих списков в модальном окне:
 * - Предметы (subjects)
 * - Аудитории (rooms)
 * - Преподаватели (teachers)
 */

// Импорт StorageSync для использования в этом модуле
import StorageSync from './storageSync.js';

// Универсальные хранилища для всех сущностей
const subjectStorage = new StorageSync('subjects', 'http://localhost:8000/api/subjects/');
const roomStorage = new StorageSync('rooms', 'http://localhost:8000/api/rooms/');
const teacherStorage = new StorageSync('teachers', 'http://localhost:8000/api/teachers/');

// Универсальный рендер списка с кнопками удаления
function renderEntityList(containerSelector, storageKey, placeholder) {
    const container = document.querySelector(containerSelector);
    if (!container) return;
    let items = [];
    if (storageKey === 'subjects') items = subjectStorage.getAll();
    if (storageKey === 'rooms') items = roomStorage.getAll();
    if (storageKey === 'teachers') items = teacherStorage.getAll();
    container.innerHTML = '';
    if (items.length === 0 && placeholder) {
        const p = document.createElement('p');
        p.textContent = placeholder;
        container.appendChild(p);
    }
    const ul = document.createElement('ul');
    items.forEach((item, idx) => {
        const li = document.createElement('li');
        li.textContent = typeof item === 'string' ? item : (item.name || item.number || item.full_name || '');
        // Кнопка удаления
        const delBtn = document.createElement('button');
        delBtn.textContent = 'Удалить';
        delBtn.className = 'delete-entity-btn';
        delBtn.onclick = function() {
            if (storageKey === 'subjects') subjectStorage.remove(idx);
            if (storageKey === 'rooms') roomStorage.remove(idx);
            if (storageKey === 'teachers') teacherStorage.remove(idx);
            renderEntityList(containerSelector, storageKey, placeholder);
        };
        li.appendChild(delBtn);
        ul.appendChild(li);
    });
    container.appendChild(ul);
}

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
    if (storageKey === 'subjects') items = subjectStorage.getAll();
    if (storageKey === 'rooms') items = roomStorage.getAll();
    if (storageKey === 'teachers') items = teacherStorage.getAll();
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