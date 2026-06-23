from django.db import models
from usuarios.models import Usuario
import random
import string

def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    maestro = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='materias')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['nombre', 'especialidad', 'maestro']

    def __str__(self):
        return f"{self.nombre} — {self.especialidad}"


class Clase(models.Model):
    SEMESTRE_CHOICES = [
        ('1-2A', '1er y 2do Semestre - Grupo A'),
        ('1-2B', '1er y 2do Semestre - Grupo B'),
        ('3-4A', '3er y 4to Semestre - Grupo A'),
        ('3-4B', '3er y 4to Semestre - Grupo B'),
        ('5-6A', '5to y 6to Semestre - Grupo A'),
        ('5-6B', '5to y 6to Semestre - Grupo B'),
    ]

    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='grupos', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)
    maestro = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='clases_creadas')
    codigo = models.CharField(max_length=6, unique=True, default=generar_codigo)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    alumnos = models.ManyToManyField(Usuario, related_name='clases_unidas', blank=True)
    semestre = models.CharField(max_length=4, choices=SEMESTRE_CHOICES, default='1-2A')

    def __str__(self):
        return f"{self.nombre} ({self.get_semestre_display()})"