import requests

resp = requests.post("http://localhost:5000/predict?path=../data/pexels-mikhail-nilov-6706798.mp4")

print(resp.text)