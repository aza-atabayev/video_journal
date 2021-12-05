from types import resolve_bases
from flask import Flask, request, jsonify, send_from_directory

import os
import  sys
import datetime
import time
from DAN.demo import get_prediction_video, Model
import scripts.google_full as model

from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
from pathlib import Path
import moviepy.editor as mpe
import ffmpeg
import numpy as np
import json

app = Flask(__name__)

emotion_coefficient = {
    'neutral': 0,
    'happy': 1,
    'anger': -0.4,
    'sad':-1,
    'fear': -0.8,
    'surprise': 0.5,
    'disgust': -0.2,
    'contempt': 0.3
}


@app.route("/data/video/<path:filename>")
def download(filename):
    return send_from_directory("data/video", filename)

@app.route("/data/images/<path:filename>")
def raw_video(filename):
    return send_from_directory("data/images", filename)

@app.route("/stylesheets/<path:filename>")
def styles(filename):
    return send_from_directory("stylesheets", filename)

app.route("/data/<path:filename>")
def download(filename):
    return send_from_directory("data", filename)

video_camera = None
global_frame = None

@app.route('/', methods=['POST', 'GET'])
def index():
    global now
    if request.method == "POST":
        f = request.files['audio_data']
        #Path(f"data/audio/{now[0]}/").mkdir(parents=True, exist_ok=True)
        filename = "{}{}".format(now[0], now[1].replace(":", "").replace(".", ""))
        with open(f"data/audio/{filename}.wav", 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        audio_prediction = model.get_prediction_audio(f'data/audio/{filename}.wav')
        print(audio_prediction)

        video_prediction = get_prediction_video(video_camera.file_path)

        data = []

        for audio in audio_prediction:
            video_scores = []
            sum_res = 0
            _, t_start, t_end, audio_res, confidence = audio.split('/')
            t_start, t_end = float(t_start), float(t_end)
            if audio_res == 'pos': audio_res = 1
            else: audio_res = -1
            if len(video_prediction) != 0:
                label, t = video_prediction[0]
                print(label)
                while t < t_end:
                    if t > t_start:
                        video_scores.append(emotion_coefficient[label])
                    video_prediction.pop(0)
                    if len(video_prediction) != 0:
                        label, t = video_prediction[0]
                final_res = audio_res + np.mean(video_scores)
            else:
                final_res = audio_res
            sum_res += final_res
            if len(data) > 0 and final_res * float(data[-1].split('/')[2]) >= 0:
                t_start = float(data[-1].split('/')[0])
                final_res = final_res + float(data[-1].split('/')[2]) 
                data.pop(-1)
            data.append(f'{t_start}/{t_end}/{final_res}')
    
        print(data)
        f = open(f"data/res/{filename}.txt", "w+")
        for line in data:
            f.write(line + '\n')
        f.close
        save_ffmpeg(filename, sum_res)
        
        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")
        
def save_ffmpeg(filename, sum_res):
    video  = ffmpeg.input(f"data/images/{filename}.avi").video # get only video channel
    audio  = ffmpeg.input(f"data/audio/{filename}.wav").audio # get only audio channel
    if sum_res >= 0: filename = str(1) + filename 
    else: filename = str(0) + filename
    output = ffmpeg.output(video, audio, f"data/video/{filename}.mp4", vcodec='libx264', acodec='aac', strict='experimental')
    ffmpeg.run(output)

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

@app.route('/journal', methods = ['GET'])
def send_all():
    list_dir = os.listdir('data/video')
    state = []
    for item in list_dir:
        state.append(item[0])
        if item[-4:] != '.mp4':
            list_dir.remove(item)
        # else:
        #     list_dir[i] = list_dir[i][1:-4] + '.avi'
        #list_dir = zip(list_dir, state)
    return render_template('results.html', result=list_dir)

@app.route('/report', methods=['GET'])
def report():
    video_link = request.args.get('video')
    print(video_link)
    f=open(f"data/res/{video_link[1:-4]}.txt", "r")
    results = f.readlines()
    f.close()
    video_data = []
    for result in results:
        t_start, t_end, res = result.split('/')
        t_start, t_end, res = float(t_start), float(t_end), float(res[:-1])
        video_data.append({
            't_start':t_start,
            't_end':t_end,
            'res': res
        })
    data = {
        'link':video_link,
        'video_data': video_data
        }
    return render_template('report.html', data = data)

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

# @app.route('/results')
# def results():
#     return render_template('results.html')