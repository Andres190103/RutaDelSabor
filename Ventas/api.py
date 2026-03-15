from rest_framework import viewsets
from .models import *
from .serializers import *

class DetalleOrdenViewSet(viewsets.ModelSiewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

