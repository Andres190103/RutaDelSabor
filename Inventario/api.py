from rest_framework import viewsets
from .models import *
from .serializers import *

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

class CompraInsumoViewSet(viewsets.ModelViewSet):
    queryset = CompraInsumo.objects.all()
    serializer_class = CompraInsumoSerializer

class CierreDiaViewSet(viewsets.ModelViewSet):
    queryset = CierreDia.objects.all()
    serializer_class = CierreDiaSerializer

