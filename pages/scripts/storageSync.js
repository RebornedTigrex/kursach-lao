

class StorageSync {
    constructor(entityKey, backendUrl) {
        this.entityKey = entityKey; // например, 'rooms', 'subjects', 'teachers', 'shedule'
        this.backendUrl = backendUrl; // например, 'http://127.0.0.1:8000/api/rooms/'
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

    async getAllFromBackend() {
        try {
            const response = await fetch(this.backendUrl, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            });
            const result = await response.json()
            return result;
        } catch (err) {
            console.log(err);
            return [];
        }
    }
    

    async addToBackend(data){
        console.log(data)
        try{
            await fetch(this.backendUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data)
            });
        } catch (err) {
            console.log(err);
        }
    }

    async delFromBackend(index) {
        try{
            await fetch(this.backendUrl, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(index)
            });
        } catch (err) {
            console.log(err);
        }
    }

}

StorageSync.prototype.getAll = StorageSync.prototype.getAllFromBackend;
StorageSync.prototype.add = StorageSync.prototype.addToBackend;
StorageSync.prototype.remove = StorageSync.prototype.delFromBackend;

export default StorageSync;