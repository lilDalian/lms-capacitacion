from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_practicas, name='lista_practicas'),
    path('nueva/', views.nueva_cedula, name='nueva_cedula'),
    path('detalle/<int:id>/', views.detalle_practica, name='detalle_practica'),
]
