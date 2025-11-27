document.querySelector('.form').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('uname').value;
    const password = document.getElementById('upass').value;

    const data = {
        username: username,
        password: password
    };

    fetch('http://127.0.0.1:8000/api/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(data => {
        const token = data.access_token;
        //console.log(token)
        //console.log(data)
        document.cookie = `jwt=${token}; path=/; HttpOnly; Secure; SameSite=Strict`;

        window.location.href = 'schedule.html';
    })
    .catch(error => {
        alert(error.message);
    });
});