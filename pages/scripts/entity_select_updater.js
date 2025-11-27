import StorageSync from 'http://127.0.0.1:3000/scripts/entity_select_updater.js';

// Универсальные хранилища для всех сущностей
const subjectStorage = new StorageSync('subjects', 'http://127.0.0.1:8000/api/subjects/');
const roomStorage = new StorageSync('rooms', 'http://127.0.0.1:8000/api/rooms/');
const teacherStorage = new StorageSync('teachers', 'http://127.0.0.1:8000/api/teachers/');


// ========================= ЛОГИКА МОДАЛЬНОГО ОКНА (Хз чё она здесь делает) =========================
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