from django.urls import path
from . import views

urlpatterns = [
    path('', views.reporte_hh, name='reporte_hh'),
]
