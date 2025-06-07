/**
 * Генерирует расписание с заданным количеством пар и перерывов.
 * @param {string} startTime - Время начала первой пары, например "09:00"
 * @param {number} lessonsCount - Количество пар в дне
 * @param {number} lessonDuration - Длительность пары в минутах (например, 90)
 * @param {number} shortBreak - Короткий перерыв в минутах (например, 10)
 * @param {number} longBreak - Длинный перерыв в минутах (например, 30)
 */
function buildTimetable(startTime, lessonsCount, lessonDuration = 90, shortBreak = 10, longBreak = 30) {
    const days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
    const tbody = document.createElement('tbody');
    let [h, m] = startTime.split(':').map(Number);

    function pad(num) { return num.toString().padStart(2, '0'); }

    for (let i = 0; i < lessonsCount; i++) {
        // Время начала и конца пары
        let start = `${pad(h)}:${pad(m)}`;
        let endMinutes = h * 60 + m + lessonDuration;
        let endH = Math.floor(endMinutes / 60);
        let endM = endMinutes % 60;
        let end = `${pad(endH)}:${pad(endM)}`;

        // Строка пары
        const tr = document.createElement('tr');
        const tdTime = document.createElement('td');
        tdTime.className = 'time';
        tdTime.textContent = `${start} - ${end}`;
        tr.appendChild(tdTime);

        for (let d = 0; d < days.length; d++) {
            const td = document.createElement('td');
            td.className = 'lesson';
            td.innerHTML = `<div class="lesson-content"></div>`;
            tr.appendChild(td);
        }
        tbody.appendChild(tr);

        // Перерыв (кроме последней пары)
        if (i < lessonsCount - 1) {
            let breakDuration = ((i + 1) % 2 === 0) ? longBreak : shortBreak;
            let breakStart = end;
            let breakEndMinutes = endH * 60 + endM + breakDuration;
            let breakEndH = Math.floor(breakEndMinutes / 60);
            let breakEndM = breakEndMinutes % 60;
            let breakEnd = `${pad(breakEndH)}:${pad(breakEndM)}`;

            const trBreak = document.createElement('tr');
            trBreak.className = 'break';
            const tdBreak = document.createElement('td');
            tdBreak.colSpan = days.length + 1;
            tdBreak.textContent = `${breakStart} - ${breakEnd} — Перерыв${breakDuration === longBreak ? ' (большой)' : ''}`;
            trBreak.appendChild(tdBreak);
            tbody.appendChild(trBreak);

            // Обновляем время к следующей паре
            h = breakEndH;
            m = breakEndM;
        } else {
            // Последняя пара — просто обновляем время
            h = endH;
            m = endM;
        }
    }

    // Вставляем tbody в таблицу
    const table = document.querySelector('.timetable');
    // Очищаем старое содержимое
    table.innerHTML = `
        <thead>
            <tr>
                <th>Время</th>
                <th>Понедельник</th>
                <th>Вторник</th>
                <th>Среда</th>
                <th>Четверг</th>
                <th>Пятница</th>
                <th>Суббота</th>
            </tr>
        </thead>
    `;
    table.appendChild(tbody);
}