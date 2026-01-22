import zipfile
import io

def extract_files_from_zip(zip_bytes):
    imagens = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_file:
        for name in zip_file.namelist():
            with zip_file.open(name) as file:
                imagens.append({
                    "filename": name,
                    "content": file.read()
                })
    return imagens


