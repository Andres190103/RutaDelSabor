from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Receta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen', 'activo', 'porcentaje_ganancia', 'porcentaje_iva']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-orange-500 outline-none'}),
            'descripcion': forms.Textarea(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-orange-500 outline-none', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-orange-500 outline-none', 'step': '0.50'}),
            'categoria': forms.Select(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-orange-500 outline-none cursor-pointer'}),
            'imagen': forms.FileInput(attrs={'class': 'block w-full text-gray-400 bg-gray-800 border border-gray-700 rounded cursor-pointer'}),
            'activo': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-orange-600 rounded focus:ring-orange-500 bg-gray-800 border-gray-600'}),

            'porcentaje_ganancia': forms.NumberInput(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-orange-500 outline-none', 'step': '0.01'}),
            'porcentaje_iva': forms.NumberInput(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-orange-500 outline-none', 'step': '0.01'}),        }

RecetaFormSet = inlineformset_factory(
    Producto,
    Receta,
    fields=['ingrediente', 'cantidad_necesaria'],
    extra=1,
    can_delete=True,
    widgets={
        'ingrediente': forms.Select(attrs={'class': 'bg-gray-700 text-white border-gray-600 rounded p-2 w-full'}),
        'cantidad_necesaria': forms.NumberInput(attrs={'class': 'bg-gray-700 text-white border-gray-600 rounded p-2 w-24', 'step': '0.001', 'placeholder': 'Cant.'}),
    }
)