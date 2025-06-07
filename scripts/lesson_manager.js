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
        const lesson = this.lessons[this.currentKey] || {};
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
        this.lessons[this.currentKey] = {
            subject: this.subjectSelect.value,
            room: this.roomSelect.value,
            teacher: this.teacherSelect.value
        };
        this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
        this.closeModal();
    },

    // Очистить данные о паре
    clearLesson() {
        if (!this.currentKey) return;
        delete this.lessons[this.currentKey];
        this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
        this.closeModal();
    },

    // Отрисовать пары в таблице
    renderLessons(weekStartISO) {
        if (!weekStartISO) return;
        this.tbody.querySelectorAll('.lesson').forEach(cell => {
            const key = this.getCellKey(cell);
            const lesson = this.lessons[key];
            if (lesson) {
                cell.innerHTML = `
                    <div class="lesson-content">
                        <strong>Предмет:</strong> ${lesson.subject || ''}<br>
                        <strong>Аудитория:</strong> ${lesson.room || ''}<br>
                        <strong>Преподаватель:</strong> ${lesson.teacher || ''}
                    </div>
                `;
            } else {
                cell.innerHTML = `<div class="lesson-content"></div>`;
            }
        });
    },

    // Методы для интеграции с БД (пример)
    async loadFromDB(weekStartISO) {
        // Здесь можно сделать fetch к backend и заполнить this.lessons
        // Пример:
        // const data = await fetch(...);
        // this.lessons = ...;
        // this.renderLessons(weekStartISO);
    },
    async saveToDB() {
        // Здесь можно отправить this.lessons на backend
    }
};

// После построения таблицы вызовите LessonManager.init();