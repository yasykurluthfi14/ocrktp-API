def categorize_text(text):
    data = {
        "Provinsi": "",
        "Kabupaten": "",
        "Jenis Kelamin": "",
        "NIK": "",
        "Nama": "",
        "Tempat Lahir": "",
        "Tanggal Lahir": "",
        "Alamat": "",
        "RT/RW": "",
        "Kel/Desa": "",
        "Kecamatan": "",
        "Agama": "",
        "Status Perkawinan": "",
        "Pekerjaan": "",
        "Kewarganegaraan": "",
        "Berlaku Hingga": ""
    }

    lines = text.split('\n')

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Split each line into words
        words = line.split()

        for i, word in enumerate(words):
            # Menentukan kategori berdasarkan kata kunci
            if "PROVINSI" in word:
                data["Provinsi"] = ' '.join(words[i+1:])
            elif "KABUPATEN" in word:
                data["Kabupaten"] = ' '.join(words[i+1:])
            elif "Jenis Kelamin" in word:
                data["Jenis Kelamin"] = ' '.join(words[i+2:])
            elif "NIK" in word:
                data["NIK"] = ' '.join(words[i+1:])
            elif "Nama" in word:
                data["Nama"] = ' '.join(words[i+1:])
            elif "Tempat Lahir" in word:
                data["Tempat Lahir"] = ' '.join(words[i+2:])
            elif "Tanggal Lahir" in word:
                data["Tanggal Lahir"] = ' '.join(words[i+2:])
            elif "Alamat" in word:
                data["Alamat"] = ' '.join(words[i+1:])
            elif "RT/RW" in word:
                data["RT/RW"] = ' '.join(words[i+1:])
            elif "Kel/Desa" in word:
                data["Kel/Desa"] = ' '.join(words[i+1:])
            elif "Kecamatan" in word:
                data["Kecamatan"] = ' '.join(words[i+1:])
            elif "Agama" in word:
                data["Agama"] = ' '.join(words[i+1:])
            elif "Status Perkawinan" in word:
                data["Status Perkawinan"] = ' '.join(words[i+2:])
            elif "Pekerjaan" in word:
                data["Pekerjaan"] = ' '.join(words[i+1:])
            elif "Kewarganegaraan" in word:
                data["Kewarganegaraan"] = ' '.join(words[i+1:])
            elif "Berlaku Hingga" in word:
                data["Berlaku Hingga"] = ' '.join(words[i+2:])

    return data
