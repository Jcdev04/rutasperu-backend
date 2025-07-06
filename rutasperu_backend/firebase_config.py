import os
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings

# Ruta al JSON; si usas GOOGLE_APPLICATION_CREDENTIALS, firebase-admin lo detecta solo
cred_path = os.path.join(settings.BASE_DIR, 'service_key.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()
