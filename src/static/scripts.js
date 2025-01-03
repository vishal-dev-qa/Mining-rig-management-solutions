function callApi(ip, endpoint) {
    fetch('/api/trigger', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: ip, endpoint: endpoint })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Error: ' + error;
    });
}
