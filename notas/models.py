from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from usuarios.models import Usuario
from clases.models import Clase

class Nota(models.Model):
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notas')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='notas')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    calificacion = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.alumno.username}'