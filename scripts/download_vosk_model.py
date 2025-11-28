import requests
from tqdm import tqdm
import zipfile
import os

url = 'https://alphacephei.com/vosk/models/vosk-model-small-es-0.22.zip'
out_path = os.path.join('assistant_data', 'models', 'vosk-model-small-es-0.22.zip')
extract_dir = os.path.join('assistant_data', 'models')

os.makedirs(extract_dir, exist_ok=True)

print('Descargando', url)
resp = requests.get(url, stream=True)
resp.raise_for_status()

total = int(resp.headers.get('content-length', 0))
with open(out_path, 'wb') as f, tqdm(total=total, unit='B', unit_scale=True, desc='Descarga') as pbar:
    for chunk in resp.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
            pbar.update(len(chunk))

print('Extrayendo a', extract_dir)
with zipfile.ZipFile(out_path, 'r') as z:
    z.extractall(extract_dir)

print('El modelo se extrajo en:', extract_dir)
print('Contenido:')
for name in os.listdir(extract_dir):
    print('-', name)
