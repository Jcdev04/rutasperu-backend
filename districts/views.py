from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rutasperu_backend.firebase_config import db

# Create your views here.
@api_view(['GET'])
def districts_list(request):
    # Lee todos los documentos de la colección “districts”
    docs = db.collection('districts').stream()
    data = [doc.to_dict() for doc in docs]
    return Response(data)