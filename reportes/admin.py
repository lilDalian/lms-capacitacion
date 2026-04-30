from django.contrib import admin
from .models import ReporteHH

@admin.register(ReporteHH)
class ReporteHHAdmin(admin.ModelAdmin):
    list_display = ('id', 'departamento', 'mes', 'anio', 'total_hh', 'total_practicas')
    list_filter = ('departamento', 'anio', 'mes')
