from flask import Flask, request, jsonify, send_from_directory

import  sys
import datetime

from DAN.demo import get_prediction_video, Model
import scripts.google_full as model

from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
from pathlib import Path

app = Flask(__name__)


@app.route("/data/video/<path:filename>")
def download(filename):
    return send_from_directory("data/video", filename)

video_camera = None
global_frame = None

@app.route('/', methods=['POST', 'GET'])
def index():
    global now
    if request.method == "POST":
        f = request.files['audio_data']
        Path(f"data/audio/{now[0]}/").mkdir(parents=True, exist_ok=True)
        filename = f'data/audio/{now[0]}/{now[1]}.wav'
        with open(filename, 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        prediction = model.get_prediction_audio(filename)
        data = {'prediction': prediction}
        print(data)
        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")
        


@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera, now
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        now = str(datetime.datetime.now()).split(" ")
        video_camera.start_record(now)
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        video_path = request.args.get('path')

    try:
        prediction = get_prediction_video(video_path)
        data = {'prediction': prediction}
        return jsonify(data)

    except:
        return jsonify({'error': 'error during prediction'})