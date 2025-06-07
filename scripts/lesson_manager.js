// Модуль управления парами в расписании
const LessonManager = (function() {
    let currentCell = null;
    let currentDayIdx = null;
    let currentLessonIdx = null;

    // Получить ключ для хранения пары
    function getLessonKey(weekStartISO, dayIdx, lessonIdx) {
        return `${weekStartISO}_${dayIdx}_${lessonIdx}`;
    }

    // Получить все пары для недели
    function getLessonsForWeek(weekStartISO) {
        return JSON.parse(localStorage.getItem(`lessons_${weekStartISO}`) || '{}');
    }

    // Сохранить все пары для недели
    function saveLessonsForWeek(weekStartISO, lessons) {
        localStorage.setItem(`lessons_${weekStartISO}`, JSON.stringify(lessons));
    }

    // Открыть модальное окно и заполнить его данными
    function openModal(cell, dayIdx, lessonIdx) {
        currentCell = cell;
        currentDayIdx = dayIdx;
        currentLessonIdx = lessonIdx;

        const weekStartISO = window.weekManager.getCurrentWeekStartISO();
        const lessons = getLessonsForWeek(weekStartISO);
        const key = getLessonKey(weekStartISO, dayIdx, lessonIdx);
        const data = lessons[key] || {};

        document.querySelector('.subject-select').value = data.subject || "";
        document.querySelector('.room-select').value = data.room || "";
        document.querySelector('.teacher-select').value = data.teacher || "";

        document.querySelector('.modal-overlay').classList.add('active');
    }

    // Сохранить изменения пары
    function saveLesson() {
        if (currentCell === null) return;
        const weekStartISO = window.weekManager.getCurrentWeekStartISO();
        const lessons = getLessonsForWeek(weekStartISO);

        const subject = document.querySelector('.subject-select').value;
        const room = document.querySelector('.room-select').value;
        const teacher = document.querySelector('.teacher-select').value;

        const key = getLessonKey(weekStartISO, currentDayIdx, currentLessonIdx);

        if (subject || room || teacher) {
            lessons[key] = { subject, room, teacher };
        } else {
            delete lessons[key];
        }
        saveLessonsForWeek(weekStartISO, lessons);

        renderLessons();
        closeModal();
    }

    // Удалить пару
    function clearLesson() {
        if (currentCell === null) return;
        if (!confirm('Вы уверены, что хотите удалить пару?')) return;
        const weekStartISO = window.weekManager.getCurrentWeekStartISO();
        const lessons = getLessonsForWeek(weekStartISO);
        const key = getLessonKey(weekStartISO, currentDayIdx, currentLessonIdx);
        delete lessons[key];
        saveLessonsForWeek(weekStartISO, lessons);

        renderLessons();
        closeModal();
    }

    // Закрыть модальное окно
    function closeModal() {
        document.querySelector('.modal-overlay').classList.remove('active');
        currentCell = null;
    }

    // Отрисовать пары в расписании
    function renderLessons() {
        const weekStartISO = window.weekManager.getCurrentWeekStartISO();
        const lessons = getLessonsForWeek(weekStartISO);
        const table = document.querySelector('.timetable');
        if (!table) return;
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((tr, lessonIdx) => {
            if (tr.classList.contains('break')) return;
            const cells = tr.querySelectorAll('.lesson');
            
            cells.forEach((cell, dayIdx) => {
                const key = getLessonKey(weekStartISO, dayIdx, lessonIdx);
                const data = lessons[key];
                if (data && (data.subject || data.room || data.teacher)) {
                    let html = '';
                    if (data.subject) html += `<div><b>Предмет:</b> ${data.subject}</div>`;
                    if (data.room) html += `<div><b>Аудитория:</b> ${data.room}</div>`;
                    if (data.teacher) html += `<div><b>Преподаватель:</b> ${data.teacher}</div>`;
                    cell.innerHTML = `<div class="lesson-content">${html}</div>`;
                } else {
                    cell.innerHTML = `<div class="lesson-content"></div>`;
                }
            });
        });
    }

    // Навесить обработчики на расписание и модальное окно
    function init() {
        // Открытие модального окна по клику на ячейку
        document.querySelector('.timetable').addEventListener('click', function(e) {
            const cell = e.target.closest('.lesson');
            if (cell) {
                // Определяем индексы
                const tr = cell.parentElement;
                const tbody = tr.parentElement;
                const lessonIdx = Array.from(tbody.children).filter(row => !row.classList.contains('break')).indexOf(tr);
                const dayIdx = Array.from(tr.children).indexOf(cell) - 1; // -1, т.к. первый столбец — время
                openModal(cell, dayIdx, lessonIdx);
            }
        });

        // Сохранение
        document.querySelector('.save-btn').addEventListener('click', saveLesson);

        // Удаление
        document.querySelector('.clear-btn').addEventListener('click', clearLesson);

        // Закрытие
        document.querySelector('.modal-close').addEventListener('click', closeModal);
        document.querySelector('.cancel-btn').addEventListener('click', closeModal);

        // Перерисовывать при смене недели
        document.querySelector('.prev-week').addEventListener('click', () => setTimeout(renderLessons, 0));
        document.querySelector('.next-week').addEventListener('click', () => setTimeout(renderLessons, 0));

        // Перерисовать после генерации расписания
        renderLessons();
    }

    // Экспортируем только init
    return {
        init,
        renderLessons
    };
})();

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    LessonManager.init();
});

document.addEventListener('weekChanged', function(e) {
    LessonManager.renderLessons();
});