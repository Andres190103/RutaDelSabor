from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Roles, PerfilUsuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'laste_name']

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    usuario_detalle = UserSerializer(source='usuario', read_only=True)
    rol_nombre = serializers.ReadOnlyField(source='rol.nombre')

    class Meta:
        model = PerfilUsuario
        fields = ['id', 'usuario', 'rol', 'usuario_detalle', 'rol_nombre' 'telefono']