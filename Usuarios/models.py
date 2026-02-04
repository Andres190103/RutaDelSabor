from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Roles(models.Model):
    # Nota: Django ya tiene un sistema de Grupos/Permisos, pero mantenemos tu lógica
    # para fines didácticos del curso.
    nombre = models.CharField(max_length=50, unique=True) # Ej: Admin, Parrillero, Mesero

    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    # Usamos OneToOne para extender al usuario de Django de forma segura
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol.nombre if self.rol else 'Sin Rol'}"