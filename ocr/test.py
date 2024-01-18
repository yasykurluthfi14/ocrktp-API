from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
import easyocr
import os

app = Flask(__name__)

# Tentukan direktori untuk menyimpan file yang diunggah
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inisialisasi EasyOCR
reader = easyocr.Reader(['id'])

# Fungsi untuk memeriksa ekstensi file yang diizinkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

# Fungsi untuk melakukan OCR pada gambar
def perform_ocr(file_path):
    img = easyocr.Image(file_path)
    result = reader.readtext(img)
    return result

# API endpoint untuk melakukan OCR pada gambar yang diunggah
@app.route('/api/ocr', methods=['POST'])
def ocr_api():
    # Pastikan ada file yang diunggah
    if 'file' not in request.files:
        abort(400, 'No file part')

    file = request.files['file']

    # Pastikan nama file tidak kosong
    if file.filename == '':
        abort(400, 'No selected file')

    # Pastikan file yang diunggah memiliki ekstensi yang diizinkan
    if not allowed_file(file.filename):
        abort(400, 'Invalid file extension. Allowed extensions are jpg, jpeg, and png')

    # Pastikan direktori penyimpanan file eksis
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Simpan file yang diunggah
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Lakukan OCR pada gambar
    ocr_result = perform_ocr(file_path)

    # Hapus file yang diunggah setelah OCR selesai
    os.remove(file_path)

    # Format hasil OCR menjadi JSON
    result_json = {
        'filename': filename,
        'ocr_result': ocr_result
    }

    return jsonify(result_json)

if __name__ == '__main__':
    app.run(debug=True)
