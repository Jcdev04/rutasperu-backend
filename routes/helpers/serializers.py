from rest_framework import serializers

class RutaParamsSerializer(serializers.Serializer):
    origen = serializers.CharField()
    destino = serializers.CharField()
    