from django.urls import path
from .views import ruta_precio, ruta_tiempo

urlpatterns = [
    path('price/', ruta_precio, name='ruta-precio'),
    path('time/', ruta_tiempo, name='ruta-tiempo'),
]