from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('maestro', 'Maestro'),
        ('alumno', 'Alumno'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='alumno')
    nombre_completo = models.CharField(max_length=100, blank=True)
    correo = models.EmailField(blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',
        blank=True
    )