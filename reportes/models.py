from django.db import models
from departamentos.models import Departamento

class ReporteHH(models.Model):
    id = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    mes = models.IntegerField()
    anio = models.IntegerField()
    total_hh = models.DecimalField(max_digits=8, decimal_places=2)
    total_practicas = models.IntegerField(default=0)
    total_asistentes = models.IntegerField(default=0)

    def __str__(self):
        return f"Reporte {self.departamento} - {self.mes}/{self.anio}"
