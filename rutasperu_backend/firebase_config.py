import os
import json
import tempfile
import firebase_admin
from firebase_admin import credentials, firestore

# Obtener el JSON desde la variable de entorno
json_str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if not json_str:
    raise ValueError("La variable de entorno 'GOOGLE_APPLICATION_CREDENTIALS_JSON' no está definida.")

# Convertir a diccionario
json_data = json.loads(json_str)

# Reemplazar los `\\n` por saltos de línea reales en la private_key
json_data["private_key"] = json_data["private_key"].replace("\\n", "\n")

# Guardar como archivo temporal válido
with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
    json.dump(json_data, temp_file)
    temp_file_path = temp_file.name

# Inicializar Firebase con el archivo temporal
cred = credentials.Certificate(temp_file_path)
firebase_admin.initialize_app(cred)
db = firestore.client()
