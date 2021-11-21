import requests

resp = requests.post("http://localhost:5000/predict?path=data/test_video.mov")

print(resp.text)