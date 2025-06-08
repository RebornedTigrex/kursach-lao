function insertSidebar(activeIndex = 0) {
    const sidebarHTML = `
    <div class="sidebar">
        <div class="logo">Расписание Факультета</div>
        <button class="toggle-sidebar"><i class="fas fa-bars"></i></button>
        <ul>
            <li><i class="fas fa-calendar-alt"></i> Расписание</li>
            <li><i class="fas fa-book"></i> Предметы</li>
            <li><i class="fas fa-chalkboard-teacher"></i> Преподаватели</li>
            <li><i class="fas fa-building"></i> Аудитории</li>
            <li><i class="fas fa-cog"></i> Настройки</li>
        </ul>
    </div>
    `;
    const main = document.querySelector('.main-content');
    if (main) {
        main.insertAdjacentHTML('beforebegin', sidebarHTML);
    } else {
        document.body.insertAdjacentHTML('afterbegin', sidebarHTML);
    }

    // Подсветка активного пункта
    if (activeIndex >= 0) {
        document.querySelectorAll('.sidebar ul li')[activeIndex].classList.add('active');
    }

    // Обработчики переходов
    const links = [
        'schedule.html',
        'subjects.html',
        'teachers.html',
        'rooms.html',
        'settings.html'
    ];
    document.querySelectorAll('.sidebar ul li').forEach((li, idx) => {
        li.addEventListener('click', () => window.location.href = links[idx]);
    });

    // Кнопка сворачивания
    document.querySelector('.toggle-sidebar').addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('collapsed');
    });
}