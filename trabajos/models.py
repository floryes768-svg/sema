from django.db import models
from usuarios.models import Usuario
from clases.models import Clase

class Trabajo(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='trabajos')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_entrega = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='trabajos/', blank=True, null=True)

    def __str__(self):
        return self.titulo

class EntregaTrabajo(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='entregas')
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='entregas')
    comentario = models.TextField(blank=True)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.trabajo.titulo} - {self.alumno.username}"
