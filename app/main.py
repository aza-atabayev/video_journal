from flask import Flask, request, jsonify

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png','jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify('error': 'no file')
        if not allowed_file(file.filename):
            return jsonify('error': 'not supported')
    return jsonify({'result':1})


    try:
        img_bytes = file.read()
        tensor = transform_image(img_bytes)
        prediction = get_prediction(tensor)
        data = {'prediction': prediction.item(), 'class_name'L str(prediction.item())}


    except:
        return jsonify({'error': 'error during prediction'})