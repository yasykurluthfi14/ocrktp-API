from flask import Flask, request, jsonify, abort
from werkzeug.datastructures import MultiDict
import os
from PIL import Image
import numpy as np
import json
import pytesseract
from waitress import serve
from configmodule import ProductionConfig

from authorization import generate_authorization_data, is_valid_authorization, authorization_codes
from image_processing import calculate_accuracy
from file_handling import generate_unique_filename
from text_categorization import categorize_text
from config import app_config

app = Flask(__name__)
app.config.from_object(ProductionConfig)
app.config['UPLOAD_FOLDER'] = app_config['UPLOAD_FOLDER']
app.config['RESULT_FOLDER'] = app_config['RESULT_FOLDER']
app.config['RESTORED_FOLDER'] = 'restored'
app.config['AUTHORIZATION'] = app_config['AUTHORIZATION']

def check_api_key():
    if request.path == '/generate-authorization-code':
        if 'Authorization' not in request.headers or request.headers['Authorization'] != app.config['AUTHORIZATION']:
            abort(401)

@app.route('/generate-authorization-code', methods=['POST'])
def generate_authorization():
    check_api_key() 
    
    authorization_code, expiry_time = generate_authorization_data()

    form_data = MultiDict([('authorization_code', authorization_code), ('expiry_time', expiry_time.isoformat())])
    return jsonify(form_data)

@app.route('/api/process', methods=['POST'])
def api_process():
    authorization_code = request.form.get('authorization_code')

    if not is_valid_authorization(authorization_code, authorization_codes.get(authorization_code)):
        return jsonify({'message': 'Kode otorisasi tidak valid atau sudah kedaluwarsa', 'status': 'False'}), 401

    if 'file' not in request.files:
        return jsonify({'message': 'No file part', 'status': 'False'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file', 'status': 'False'}), 400

    allowed_extensions = {'jpg', 'png', 'jpeg'}
    
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        filename = generate_unique_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        img = Image.open(file_path).convert('RGB')
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(np.array(img), config=custom_config, lang="ind")
        
        print(text)

        reference_text = "NIK NAMA Tempat/Tgl Lahir Alamat RT/RW Kel/Desa Kecamatan Agama Status Perkawinan Pekerjaan Kewarganegaraan Berlaku Hingga"
        categorized_text = categorize_text(text)
        print(categorized_text)
        accuracy = calculate_accuracy(reference_text, text)

        ocr_result = {
            "Status": "TRUE" if categorized_text else "FALSE",
            "Text": categorized_text,
            "Accuracy": accuracy
        }

        result_filename = os.path.join(app.config['RESULT_FOLDER'], f'OCR_{filename}.json')
        with open(result_filename, 'w') as json_file:
            json.dump(ocr_result, json_file, ensure_ascii=False, indent=4)

        return jsonify(ocr_result)

    return jsonify({'message': 'Invalid file extension. Allowed extensions are jpg, png, and jpeg.', 'status': 'False'}), 400
    
mode = 'prod'

if __name__ == '__main__':
    if mode == 'prod':
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        if not os.path.exists(app.config['RESULT_FOLDER']):
            os.makedirs(app.config['RESULT_FOLDER'])
        
        app.run(host='0.0.0.0', port=50100)
    else:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        if not os.path.exists(app.config['RESULT_FOLDER']):
            os.makedirs(app.config['RESULT_FOLDER'])
        
        serve(app, host='0.0.0.0', port=50100, threads=2, url_prefix="/my-app")
