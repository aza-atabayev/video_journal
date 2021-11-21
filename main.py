from flask import Flask, request, jsonify

import  sys

from DAN.demo import get_prediction, Model

app = Flask(__name__)

#@app.route('/', methods=['GET'])
#def index():

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        video_path = request.args.get('path')

    try:
        prediction = get_prediction(video_path)
        data = {'prediction': prediction}
        return jsonify(data)

    except:
        return jsonify({'error': 'error during prediction'})