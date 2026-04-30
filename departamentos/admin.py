from django.contrib import admin
from .models import Departamento

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'enfoque')
    search_fields = ('nombre', 'enfoque')
    list_filter = ('enfoque',)
