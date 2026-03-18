from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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

class LoginPersonalizado(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        rol_nombre = "Sin Rol"
        if hasattr(user, 'perfil') and user.perfil.rol:
            rol_nombre = user.perfil.rol.nombre

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'rol': rol_nombre
        })
    
