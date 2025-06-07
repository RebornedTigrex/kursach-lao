/**
 * Обновляет список предметов в выпадающем меню модального окна.
 * Предметы берутся из localStorage (или можно заменить на fetch с backend).
 */
function updateSubjectSelect() {
    const select = document.querySelector('.subject-select');
    if (!select) return;
    // Сохраняем первую опцию (заглушку)
    const firstOption = select.querySelector('option[value=""]');
    select.innerHTML = '';
    if (firstOption) select.appendChild(firstOption);

    // Получаем предметы из localStorage
    const subjects = JSON.parse(localStorage.getItem('subjects') || '[]');
    subjects.forEach((subject, idx) => {
        const option = document.createElement('option');
        option.value = subject;
        option.textContent = subject;
        select.appendChild(option);
    });
}

// Вызывать при открытии модального окна:
document.addEventListener('DOMContentLoaded', function() {
    // Открытие модального окна — обновляем список предметов
    document.querySelector('.timetable').addEventListener('click', function(e) {
        const lesson = e.target.closest('.lesson');
        if (lesson) {
            updateSubjectSelect();
        }
    });

    // Слушаем обновления предметов из других вкладок/окон
    window.addEventListener('storage', function(e) {
        if (e.key === 'subjects') updateSubjectSelect();
    });
});