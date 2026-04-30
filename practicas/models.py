from django.db import models
from departamentos.models import Departamento
from instructores.models import Instructor

class Colaborador(models.Model):
    id = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=150)
    numero_colaborador = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.numero_colaborador} - {self.nombre_completo}"

class PracticaOperativa(models.Model):
    DURACION_CHOICES = [
        (15, '15 Minutos'),
        (30, '30 Minutos'),
        (60, '60 Minutos'),
    ]
    ESTATUS_CHOICES = [
        ('Programado', 'Programado'),
        ('Pendiente', 'Pendiente'),
        ('Completado', 'Completado'),
    ]

    id = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    nombre_curso = models.CharField(max_length=200)
    lugar = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_minutos = models.IntegerField(choices=DURACION_CHOICES)
    estatus = models.CharField(max_length=50, choices=ESTATUS_CHOICES, default='Programado')
    fecha_expiracion = models.DateField()
    objetivo = models.TextField(blank=True)
    descripcion_estandar = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_curso

class AsistenciaPractica(models.Model):
    id = models.AutoField(primary_key=True)
    practica = models.ForeignKey(PracticaOperativa, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    firma = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.colaborador} - {self.practica}"
