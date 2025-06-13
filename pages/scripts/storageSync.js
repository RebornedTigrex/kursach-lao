// storageSync.js

class StorageSync {
    constructor(entityKey, backendUrl) {
        this.entityKey = entityKey; // например, 'rooms', 'subjects', 'teachers'
        this.backendUrl = backendUrl; // например, 'http://localhost:8000/api/rooms/'
        this.syncDelay = 2000; // задержка перед отправкой на сервер (мс)
        this.syncTimeout = null;
    }

    getAll() {
        return JSON.parse(localStorage.getItem(this.entityKey) || '[]');
    }

    saveAll(items) {
        localStorage.setItem(this.entityKey, JSON.stringify(items));
        this.scheduleSync();
    }

    add(item) {
        const items = this.getAll();
        items.push(item);
        this.saveAll(items);
    }

    remove(index) {
        const items = this.getAll();
        items.splice(index, 1);
        this.saveAll(items);
    }

    // Синхронизация с backend (отправка localStorage -> сервер)
    scheduleSync() {
        if (this.syncTimeout) clearTimeout(this.syncTimeout);
        this.syncTimeout = setTimeout(() => this.syncToBackend(), this.syncDelay);
    }

    async syncToBackend() {
        const items = this.getAll();
        try {
            await fetch(this.backendUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(items)
            });
        } catch (e) {
            // Ошибка синхронизации
        }
    }

    // Получение актуальных данных с backend (сервер -> localStorage)
    async updateFromBackend() {
        try {
            const resp = await fetch(this.backendUrl);
            const items = await resp.json();
            localStorage.setItem(this.entityKey, JSON.stringify(items));
        } catch (e) {
            // Ошибка обновления
        }
    }
}

// Пример использования:
// const roomStorage = new StorageSync('rooms', 'http://localhost:8000/api/rooms/');
// roomStorage.add('101');
// roomStorage.remove(0);
// roomStorage.updateFromBackend();

export default StorageSync;