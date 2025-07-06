from django.urls import path
from .views import districts_list

urlpatterns = [
    path('', districts_list, name='districts-list'),
]