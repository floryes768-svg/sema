from django.db import models
from clases.models import Clase
from usuarios.models import Usuario

class Asistencia(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Presente'),
        ('A', 'Ausente'),
        ('R', 'Retardo'),
    ]

    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='asistencias')
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')

    class Meta:
        unique_together = ['clase', 'alumno', 'fecha']

    def __str__(self):
        return f"{self.alumno.username} - {self.fecha} - {self.estado}"
