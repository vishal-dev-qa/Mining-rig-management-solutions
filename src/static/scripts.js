function callApi(ip, command) {
    fetch('/trigger', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: ip, command: command })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            document.getElementById('response').innerText = `Error: ${data.error}`;
        } else {
            document.getElementById('response').innerText = JSON.stringify(data, null, 2);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerText = `Error: ${error.message}`;
    });
}
