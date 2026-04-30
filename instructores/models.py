from django.db import models
from departamentos.models import Departamento

class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=150)
    correo = models.EmailField()
    activo = models.BooleanField(default=True)
    puede_programar = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_completo
