from django import forms
from .models import Ingrediente

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'stock_actual', 'stock_minimo', 'unidad_medida', 'proveedor_principal']
        
        labels = {
            'nombre': 'Nombre del Insumo',
            'stock_actual': 'Stock Inicial',
            'stock_minimo': 'Alerta de Mínimo',
            'unidad_medida': 'Unidad de Medida',
            'proveedor_principal': 'Proveedor (Opcional)'
        }
        
        widgets = {
            'unidad_medida': forms.Select(attrs={
                'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-blue-500 outline-none cursor-pointer'
            }),

            'proveedor_principal': forms.Select(attrs={
                'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-blue-500 outline-none cursor-pointer'
            }),
            
            'nombre': forms.TextInput(attrs={
                'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-blue-500 outline-none',
                'placeholder': 'Ej: Tomate Bola'
            }),
            
            'stock_actual': forms.NumberInput(attrs={
                'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-blue-500 outline-none',
                'step': '0.001'
            }),
            
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-blue-500 outline-none',
                'step': '0.001'
            }),
        }