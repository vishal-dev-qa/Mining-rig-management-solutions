import requests, json
from src.config.config import CG_PORT

def call_cgminer(ip, command):
    url = f"http://{ip}:{CG_PORT}"
    payload = {"command": command}

    try:
        response = requests.post(url, data=json.dumps(payload), timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Unable to connect to {ip}:{CG_PORT}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
