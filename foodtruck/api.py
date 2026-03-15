from rest_framework import viewsets
from .models import ConfiguracionNegocio, Categoria, Producto, Receta
from .serializers import(
    ConfiguracionNegocioSerializer,
    CategoriaSerializer,
    ProductoSerializer,
    RecetaSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer

class ConfiguracionNegocioViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionNegocio.objects.all()
    serializer_class = ConfiguracionNegocioSerializer

