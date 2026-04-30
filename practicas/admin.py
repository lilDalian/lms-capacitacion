from django.contrib import admin
from .models import PracticaOperativa, Colaborador, AsistenciaPractica

@admin.register(PracticaOperativa)
class PracticaOperativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_curso', 'instructor', 'departamento', 'fecha_inicio', 'estatus')
    search_fields = ('nombre_curso',)
    list_filter = ('estatus', 'departamento', 'instructor')

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_colaborador', 'nombre_completo', 'departamento')
    search_fields = ('numero_colaborador', 'nombre_completo')
    list_filter = ('departamento',)

@admin.register(AsistenciaPractica)
class AsistenciaPracticaAdmin(admin.ModelAdmin):
    list_display = ('id', 'practica', 'colaborador', 'firma', 'fecha_registro')
    search_fields = ('colaborador__nombre_completo', 'practica__nombre_curso')
    list_filter = ('firma', 'practica__departamento')
