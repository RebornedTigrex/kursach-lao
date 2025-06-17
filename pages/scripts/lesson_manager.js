// Класс для работы с ячейками пар

const LessonManager = {
    lessons: {}, // { 'YYYY-MM-DD_row_col': {subject, room, teacher} }
    tbody: null,
    modal: null,
    subjectSelect: null,
    roomSelect: null,
    teacherSelect: null,
    saveBtn: null,
    cancelBtn: null,
    clearBtn: null,
    closeBtn: null,
    currentCell: null,
    currentKey: null,

    // Инициализация: навешиваем обработчики на ячейки и кнопки модального окна
    init() {
        this.tbody = document.querySelector('.timetable tbody');
        this.modal = document.querySelector('.modal-overlay');
        this.subjectSelect = document.querySelector('.subject-select');
        this.roomSelect = document.querySelector('.room-select');
        this.teacherSelect = document.querySelector('.teacher-select');
        this.saveBtn = document.querySelector('.save-btn');
        this.cancelBtn = document.querySelector('.cancel-btn');
        this.clearBtn = document.querySelector('.clear-btn');
        this.closeBtn = document.querySelector('.modal-close');

        this.currentCell = null;
        this.currentKey = null;

        this.loadFromStorage();
   
        // Навешиваем обработчик на все ячейки расписания
        this.tbody.addEventListener('click', (e) => {
            const cell = e.target.closest('.lesson');
            if (cell) this.openModal(cell);
        });

        this.saveBtn.addEventListener('click', () => this.saveLesson());
        this.cancelBtn.addEventListener('click', () => this.closeModal());
        this.closeBtn.addEventListener('click', () => this.closeModal());
        this.clearBtn.addEventListener('click', () => this.clearLesson());

        // Перерисовывать пары при смене недели
        document.addEventListener('weekChanged', (e) => {
            this.renderLessons(e.detail.weekStartISO);
        });

        // Первичная отрисовка
        this.renderLessons(window.weekManager?.getCurrentWeekStartISO());

    },

    // Генерация уникального ключа для ячейки (можно заменить на id из БД)
    getCellKey(cell) {
        // Пример: "2024-06-07_2_3" (неделя_строка_день)
        const weekISO = window.weekManager?.getCurrentWeekStartISO() || 'unknown';
        const row = cell.parentElement.rowIndex;
        const col = cell.cellIndex;
        return `${weekISO}_${row}_${col}`;
    },

    // Открыть модальное окно для ячейки
    openModal(cell) {
        this.currentCell = cell;
        this.currentKey = this.getCellKey(cell);

        // Заполнить select'ы текущими значениями
        let lesson = {};
        lesson = this.lessons[this.currentKey] || {};

        this.subjectSelect.value = lesson.subject || '';
        this.roomSelect.value = lesson.room || '';
        this.teacherSelect.value = lesson.teacher || '';
        this.modal.classList.add('active');
    },

    // Закрыть модальное окно
    closeModal() {
        this.modal.classList.remove('active');
        this.currentCell = null;
        this.currentKey = null;
    },

    // Сохранить данные о паре
    saveLesson() {
        if (!this.currentKey) return;
        const data = {
            subject: this.subjectSelect.value,
            room: this.roomSelect.value,
            teacher: this.teacherSelect.value
        };

        this.lessons[this.currentKey] = data;
        this.saveToStorage({[this.currentKey]: data});
        this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
        this.closeModal();
    },

    // Очистить данные о паре
    clearLesson() {
        if (!this.currentKey) return;
        delete this.lessons[this.currentKey];
        window.sheduleStorage.remove(this.currentKey)
        this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
        this.closeModal();
    },

    // Отрисовать пары в таблице
    renderLessons(weekStartISO) {
        if (!weekStartISO) return;
        this.tbody.querySelectorAll('.lesson').forEach(cell => {
            const key = this.getCellKey(cell);
            const data = this.lessons[key];
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
    },

    async saveToStorage(lesson) {
        await window.sheduleStorage.add(lesson)
    },

    async loadFromStorage() {
        const data = await window.sheduleStorage.getAll()
        console.log(data)
        if (data) {
            this.lessons = data;
        }
    }
};
