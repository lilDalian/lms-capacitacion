from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_practicas, name='lista_practicas'),
    path('nueva/', views.nueva_cedula, name='nueva_cedula'),
]
