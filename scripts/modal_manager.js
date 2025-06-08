function insertModal() {
    const modalHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Редактирование пары</h3>
                    <span class="modal-close">×</span>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label>Предмет:</label>
                        <select class="subject-select">
                            <option value="">-- Выберите предмет --</option>
                            <!-- Динамически заполняется -->
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Аудитория:</label>
                        <select class="room-select">
                            <option value="">-- Выберите аудиторию --</option>
                            <!-- Динамически заполняется -->
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Преподаватель:</label>
                        <select class="teacher-select">
                            <option value="">-- Выберите преподавателя --</option>
                            <!-- Динамически заполняется -->
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="clear-btn">Удалить пару</button>
                    <button class="cancel-btn">Отмена</button>
                    <button class="save-btn">Сохранить</button>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Экспортируем функцию для использования в других файлах
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { insertModal };
} else {
    window.insertModal = insertModal;
}