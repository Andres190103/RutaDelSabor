from rest_framework import serializers
from .models import ConfiguracionNegocio, Categoria, Producto, Receta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields= '__all__'

class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # Se agregar este campo de lectira para que React reciba el nombre de la categoria, no solo el ID numerico
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = '__all__'

class ConfiguracionNegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionNegocio
        fields = '__all__'