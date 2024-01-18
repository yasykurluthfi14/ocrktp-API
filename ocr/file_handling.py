import os
import secrets
from datetime import datetime
import json

def generate_unique_filename(original_filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_hex = secrets.token_hex(8)
    file_extension = original_filename.rsplit('.', 1)[1] if '.' in original_filename else 'jpg'
    return f"{timestamp}_{random_hex}.{file_extension}"

def save_result_to_file(result, result_folder, filename):
    result_filename = os.path.join(result_folder, filename)
    
    with open(result_filename, 'w') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

# Fungsi-fungsi berikut dapat ditambahkan di sini jika diperlukan
# - Fungsi untuk penghapusan file jika diperlukan
# - Fungsi untuk memeriksa keberadaan file di direktori
