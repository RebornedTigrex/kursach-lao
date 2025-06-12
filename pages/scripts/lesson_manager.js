// Глобальная переменная для выбора источника данных: "localstorage" или "sql"
window.DATA_SOURCE = window.DATA_SOURCE || "localstorage"; // или "sql"

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

        if (window.DATA_SOURCE === "localstorage") {
            this.loadFromStorage();
        } else {
            // При старте загружаем расписание с backend для текущей недели
            this.loadFromDB(window.weekManager?.getCurrentWeekStartISO());
        }

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
            if (window.DATA_SOURCE === "localstorage") {
                this.renderLessons(e.detail.weekStartISO);
            } else {
                this.loadFromDB(e.detail.weekStartISO);
            }
        });

        // Первичная отрисовка
        if (window.DATA_SOURCE === "localstorage") {
            this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
        } else {
            this.loadFromDB(window.weekManager?.getCurrentWeekStartISO());
        }
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
    async openModal(cell) {
        this.currentCell = cell;
        this.currentKey = this.getCellKey(cell);

        // Заполнить select'ы актуальными значениями из БД
        await updateModalSelects();

        // Заполнить select'ы текущими значениями
        let lesson = {};
        if (window.DATA_SOURCE === "localstorage") {
            lesson = this.lessons[this.currentKey] || {};
        } else {
            lesson = cell._lessonData || {};
        }
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
    async saveLesson() {
        if (!this.currentKey) return;
        const data = {
            subject: this.subjectSelect.value,
            room: this.roomSelect.value,
            teacher: this.teacherSelect.value
        };
        if (window.DATA_SOURCE === "localstorage") {
            this.lessons[this.currentKey] = data;
            this.saveToStorage();
            this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
            this.closeModal();
        } else {
            // Отправить на backend
            await this.saveToDB(this.currentCell, data);
            await this.loadFromDB(window.weekManager?.getCurrentWeekStartISO());
            this.closeModal();
        }
    },

    // Очистить данные о паре
    async clearLesson() {
        if (!this.currentKey) return;
        if (window.DATA_SOURCE === "localstorage") {
            delete this.lessons[this.currentKey];
            this.saveToStorage();
            this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
            this.closeModal();
        } else {
            // Удалить с backend
            await this.deleteFromDB(this.currentCell);
            await this.loadFromDB(window.weekManager?.getCurrentWeekStartISO());
            this.closeModal();
        }
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

    // Методы для интеграции с БД
    async loadFromDB(weekStartISO) {
        try {
            const resp = await fetch(`http://localhost:8000/api/schedule/?week_start=${weekStartISO}`);
            const data = await resp.json();
            // Сохраняем данные в lessons по ключу, чтобы renderLessons мог их отрисовать
            this.lessons = {};
            // Очищаем все lessonData
            this.tbody.querySelectorAll('.lesson').forEach(cell => {
                cell._lessonData = undefined;
            });
            data.forEach(item => {
                const row = item.row, col = item.col;
                // Ключ как в renderLessons
                const key = `${weekStartISO}_${row}_${col}`;
                this.lessons[key] = {
                    subject: item.subject,
                    room: item.room,
                    teacher: item.teacher
                };
                // Для открытия модального окна с данными
                const cell = this.tbody.rows[row]?.cells[col];
                if (cell) cell._lessonData = item;
            });
            this.renderLessons(weekStartISO);
        } catch (e) {
            alert('Ошибка загрузки расписания с сервера');
        }
    },

    async saveToDB(cell, data) {
        const row = cell.parentElement.rowIndex;
        const col = cell.cellIndex;
        const weekISO = window.weekManager?.getCurrentWeekStartISO() || 'unknown';
        const key = `${weekISO}_${row}_${col}`;
        try {
            await fetch(`http://localhost:8000/api/schedule/${key}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    subject: data.subject,
                    room: data.room,
                    teacher: data.teacher
                })
            });
        } catch (e) {
            alert('Ошибка сохранения данных на сервере');
        }
    },

    async deleteFromDB(cell) {
        const row = cell.parentElement.rowIndex;
        const col = cell.cellIndex;
        const weekISO = window.weekManager?.getCurrentWeekStartISO() || 'unknown';
        const key = `${weekISO}_${row}_${col}`;
        try {
            await fetch(`http://localhost:8000/api/schedule/${key}/`, {
                method: 'DELETE'
            });
        } catch (e) {
            alert('Ошибка удаления данных с сервера');
        }
    },

    // Локальное хранилище
    saveToStorage() {
        localStorage.setItem('lessons', JSON.stringify(this.lessons));
    },

    loadFromStorage() {
        const data = localStorage.getItem('lessons');
        if (data) {
            this.lessons = JSON.parse(data);
            this.renderLessons(window.weekManager?.getCurrentWeekStartISO());
        }
    }
};

LessonManager.init();