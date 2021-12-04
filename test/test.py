import requests

resp = requests.get("http://localhost:5000/journal")

print(resp.text)