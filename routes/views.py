# routes/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .helpers.serializers import RutaParamsSerializer
from rutasperu_backend.firebase_config import db
from .services.routes_service import BuscadorRutas

@api_view(['GET'])
def ruta_tiempo(request):
    serializer = RutaParamsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    origen = serializer.validated_data['origen']
    destino = serializer.validated_data['destino']
    # Aquí tu lógica real para calcular tiempo
    return Response({'origen': origen, 'destino': destino, 'tiempo': "tiempo"})

@api_view(['GET'])
def ruta_precio(request):
    serializer = RutaParamsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    origen = serializer.validated_data['origen']
    destino = serializer.validated_data['destino']
    # Query Firestore for all routes with the given origen
    docs = db.collection('routes').stream()
    data = [doc.to_dict() for doc in docs]

    service = BuscadorRutas(data)
    result = service.buscar_ruta_optima(origen, destino)
    return Response(result)
