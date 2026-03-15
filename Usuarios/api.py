from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Roles, PerfilUsuario
from .serializers import UserSerializer, RolesSerializer, PerfilUsuarioSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all()
    query_class = PerfilUsuarioSerializer

