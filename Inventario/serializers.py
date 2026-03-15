from rest_framework import serializers
from .models import *

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class IngredienteSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor_principal.nombre_empresa')

    class Meta:
        model = Ingrediente
        fields = '__all__'

class CompraInsumoSerializer(serializers.ModelSerializer):
    ingrediente_nombre = serializers.ReadOnlyField(source='ingrediente.nombre')
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.nombre_proveedor')

    class Meta:
        model = CompraInsumo
        fields = '__all__'

class CierreDiaSerializer(serializers.ModelSerializer):
    responsable_nombre = serializers.ReadOnlyField(source='responsable.username')

    class Meta:
        model = CierreDia
        fields = '__all__'

