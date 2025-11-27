document.querySelector('.form').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('uname').value;
    const email = document.getElementById('umail').value;
    const password = document.getElementById('upass').value;

    const data = {
        username: username,
        email: email,
        password: password
    };

    fetch('http://127.0.0.1:8000/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Registration failed');
        }
        return response.json();
    })
    .then(data => {
        const token = data.access_token;

        document.cookie = `jwt=${token}; path=/; HttpOnly; Secure; SameSite=Strict`;
        console.log(token)
        console.log(data)
        //window.location.href = 'schedule.html';
    })
    .catch(error => {
        alert(error.message);
    });
});