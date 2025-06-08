// Получить понедельник для любой даты
function getMonday(date) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - ((day + 6) % 7); // понедельник = 1, воскресенье = 0
    return new Date(d.setDate(diff));
}

// Получить массив дат недели (понедельник-воскресенье)
function getWeekDates(monday) {
    const dates = [];
    for (let i = 0; i < 7; i++) {
        const d = new Date(monday);
        d.setDate(monday.getDate() + i);
        dates.push(d);
    }
    return dates;
}

// Форматировать диапазон дат недели для отображения
function formatWeekRange(weekDates) {
    const months = [
        "Января", "Февраля", "Марта", "Апреля", "Мая", "Июня",
        "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"
    ];
    const start = weekDates[0];
    const end = weekDates[6];
    // Если месяц совпадает, не повторяем его
    if (start.getMonth() === end.getMonth()) {
        return `${start.getDate()}–${end.getDate()} ${months[start.getMonth()]} ${start.getFullYear()}`;
    } else {
        return `${start.getDate()} ${months[start.getMonth()]} – ${end.getDate()} ${months[end.getMonth()]} ${start.getFullYear()}`;
    }
}

// Получить ISO-дату начала недели (для backend)
function getWeekStartISO(monday) {
    return monday.toISOString().slice(0, 10); // 'YYYY-MM-DD'
}

// Управление неделями
class WeekManager {
    constructor(selector) {
        this.currentMonday = getMonday(new Date());
        this.display = document.querySelector(selector);
        this.updateDisplay();
        this.addListeners();
    }

    updateDisplay() {
        const weekDates = getWeekDates(this.currentMonday);
        this.display.textContent = formatWeekRange(weekDates);
        // Генерируем событие о смене недели
        document.dispatchEvent(new CustomEvent('weekChanged', {
            detail: { weekStartISO: this.getCurrentWeekStartISO() }
        }));
    }

    nextWeek() {
        this.currentMonday.setDate(this.currentMonday.getDate() + 7);
        this.updateDisplay();
    }

    prevWeek() {
        this.currentMonday.setDate(this.currentMonday.getDate() - 7);
        this.updateDisplay();
    }

    goToCurrentWeek() {
        this.currentMonday = getMonday(new Date());
        this.updateDisplay();
    }

    addListeners() {
        document.querySelector('.prev-week').addEventListener('click', () => this.prevWeek());
        document.querySelector('.next-week').addEventListener('click', () => this.nextWeek());
        this.display.addEventListener('click', () => this.goToCurrentWeek());
    }

    getCurrentWeekStartISO() {
        return getWeekStartISO(this.currentMonday);
    }
}