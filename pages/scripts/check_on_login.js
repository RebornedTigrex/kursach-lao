import {getUsername} from '../scripts/storageSync.js';

function showCenteredFrame(message) {
    const overlay = document.createElement('div');
    overlay.id = 'centered-frame-overlay';
    Object.assign(overlay.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: '9999'
    });

    const frame = document.createElement('div');
    Object.assign(frame.style, {
        backgroundColor: 'white',
        padding: '40px',
        fontSize: '24px',
        fontWeight: 'bold',
        borderRadius: '10px',
        maxWidth: '60%',
        textAlign: 'center'
    });

    const htmlforlog = `
    <p><a href="http://127.0.0.1:3000/registration.html">Зарегестрируйтесь</a> или <a href="http://127.0.0.1:3000/login.html">Войдите</a> в аккаунт чтобы получить доступ к интерфейсу</p>
    `

    //frame.innerText = message;
    frame.innerHTML = htmlforlog;
    overlay.appendChild(frame);
    document.body.appendChild(overlay);
}

async function checkCacheAndRequest() {
    let session = await getUsername();
    session = session.detail;
    
    if (session == "Invalid token" || session == "Token expired") {
        showCenteredFrame('Missing JWT token. Please log in.');
    }
    //if (!jwt) {
    //    showCenteredFrame('Missing JWT token. Please log in.');
    //}
    //try {
    //    const response = await fetch(url, {
    //        method: 'GET',
    //        headers: {
    //        'Authorization': `Bearer ${jwt}`
    //    }
    //});
    //if (response.status === 403) {
    //    showCenteredFrame('403 Not Authorized');
    //} else {
    //    // Handle successful response if needed
    //    // const data = await response.json();
    //}
    //} catch (error) {
    //    console.error('Request failed:', error);
    //    showCenteredFrame('Error occurred during request.');
    //}
}

checkCacheAndRequest();