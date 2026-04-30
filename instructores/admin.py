from django.contrib import admin
from .models import Instructor

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'departamento', 'correo', 'activo')
    search_fields = ('nombre_completo', 'correo')
    list_filter = ('departamento', 'activo', 'puede_programar')
