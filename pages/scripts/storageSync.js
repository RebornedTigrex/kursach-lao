function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [key, value] = cookie.trim().split('=');
      if (key === name) {
        return decodeURIComponent(value);
      }
    }
    return null;
  }

export async function getUsername() {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/ia", {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getCookie('jwt')}`,
            },
            
        });
        const result = await response.json()
        //const result = response;
        //console.log(result);
        return result;
    } catch (err) {
        console.log(err);
    }
}

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
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${getCookie('jwt')}`,
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
        // console.log(data);
        try{
            await fetch(this.backendUrl, {
                method: "POST",
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${getCookie('jwt')}`,
                },
                body: JSON.stringify(data)
            });
        // console.log(body)
        } catch (err) {
            console.log(err);
        }
    }

    async delFromBackend(index) {
        try{
            await fetch(this.backendUrl, {
                method: "DELETE",
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${getCookie('jwt')}`,
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