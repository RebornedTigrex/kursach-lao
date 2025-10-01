function insertSidebar(activeIndex = 0) {
    const sidebarHTML = `
    <div class="sidebar">
        <div class="sidebar-flex">
            <button class="toggle-sidebar"><i class="fas fa-bars"></i></button>
            <div class="spc logo">Расписание Факультета</div>
        </div>
        <ul>
            <li><i class="fas spc fa-calendar-alt"></i> <p class="slable">Расписание</p></li>
            <li><i class="fas spc fa-book"></i> <p class="slable">Предметы</p></li>
            <li><i class="fas spc fa-chalkboard-teacher"></i> <p class="slable">Преподаватели</p></li>
            <li><i class="fas spc fa-building"></i> <p class="slable">Аудитории</p></li>
            <li><i class="fas spc fa-cog"></i> <p class="slable">Настройки</p></li>
        </ul>
        <div class="login-card">
            <a class="login-card-a" href="registration.html">
                <div class="login-card-flex">
                    <div class="login-card-photo">
                        <img class="login-card-img" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.yvj61X0dbFFF8viA7fmKcAHaEV%3Fpid%3DApi&f=1&ipt=1ae4405c4e7067ae6eb24120bdff00d4d7ee5b09192b3a032a0f6614763abff3&ipo=images">
                    </div>
                    <p class="login-name slable">1111111111111111111111</p>
                </div>
            </a>
        </div>
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
        const elementsTextSL = document.querySelectorAll('.slable');
        const elementsSlidablePictures = document.querySelectorAll('.spc');
        const logoElements = document.getElementsByClassName('logo');
        const sflex = document.querySelector('.sidebar-flex');
        const lflex = document.querySelector('.login-card-flex');
        elementsTextSL.forEach(element => {
            if (window.getComputedStyle(element).display === 'none') {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        });
        Array.from(logoElements).forEach(function(element) {
        if (window.getComputedStyle(element).display === 'none') {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
        });
        elementsSlidablePictures.forEach(element => {
            if (window.getComputedStyle(element).marginRight === '0px') {
                sflex.style.justifyContent = '';
                lflex.style.justifyContent = '';
                element.style.margin = '0 10px 0 0';
            } else {
                sflex.style.justifyContent = 'flex-end';
                lflex.style.justifyContent = 'flex-end';
                element.style.margin = '0 0 0 auto';
            }
        });

    });
}