function insertSidebar(activeIndex = 0) {
    const sidebarHTML = `
    <div class="sidebar">
        <div class="sidebar-flex">
            <button class="toggle-sidebar"><i class="fas fa-bars"></i></button>
            <div class="logo">Расписание Факультета</div>
        </div>
        <ul>
            <li><i class="fas fa-calendar-alt"></i> <p id="slable">Расписание</p></li>
            <li><i class="fas fa-book"></i> <p id="slable">Предметы</p></li>
            <li><i class="fas fa-chalkboard-teacher"></i> <p id="slable">Преподаватели</p></li>
            <li><i class="fas fa-building"></i> <p id="slable">Аудитории</p></li>
            <li><i class="fas fa-cog"></i> <p id="slable">Настройки</p></li>
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
        document.getElementById('slable').classList.toggle("offsl");
    });
}