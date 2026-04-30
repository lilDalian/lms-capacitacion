from django.db import models

class Departamento(models.Model):
    ENFOQUE_CHOICES = [
        ('Generales', 'Generales'),
        ('Cristal', 'Cristal'),
        ('Operación', 'Operación'),
        ('Institucionales', 'Institucionales'),
        ('Seguridad', 'Seguridad'),
        ('Servicio', 'Servicio'),
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    enfoque = models.CharField(max_length=50, choices=ENFOQUE_CHOICES)

    def __str__(self):
        return self.nombre
