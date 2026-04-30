from django.urls import path
from . import views

urlpatterns = [
    path('', views.permisos, name='permisos'),
    path('toggle/<int:id>/', views.toggle_permiso, name='toggle_permiso'),
]
