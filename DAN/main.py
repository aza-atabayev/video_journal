from flask import Flask, request, jsonify

from demo import get_prediction, Model

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png','jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        video_path = request.args.get('path')
        print("-----------------------")
        print(video_path)
        #file = request.files.get('file')
        #if file is None or file.filename == "":
        #    return jsonify({'error': 'no file'})
        #if not allowed_file(file.filename):
        #    return jsonify({'error': 'not supported'})
    #return jsonify({'result':1})

  #  try:
    prediction = get_prediction(video_path)
    data = {'prediction': prediction}
    return jsonify(data)

   # except:
    #    return jsonify({'error': 'error during prediction'})