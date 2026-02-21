from django import forms
from .models import Ingrediente, CompraInsumo, CierreDia

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

class CompraInsumoForm(forms.ModelForm):
    class Meta:
        model = CompraInsumo
        fields = ['proveedor', 'ingrediente', 'cantidad', 'costo_total', 'factura_ref']
        labels = {
            'proveedor': 'Proveedor',
            'ingrediente': 'Insumo a comprar',
            'cantidad': 'Cantidad Comprada',
            'costo_total': 'Costo Total ($)',
            'factura_ref': 'Referencia / Ticker'
        }
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-green-500 outline-none cursor-pointer text-lg'}),
            'ingrediente': forms.Select(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-green-500 outline-none cursor-pointer text-lg'}),
            'cantidad': forms.NumberInput(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-green-500 outline-none text-lg', 
                                                 'step': '0.001'}),
            'costo_total': forms.NumberInput(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-green-500 outline-none text-lg', 
                                                    'step': '0.01'}),
            'factura_ref': forms.TextInput(attrs={'class': 'block w-full bg-gray-800 border-gray-700 text-white rounded p-3 focus:border-green-500 outline-none',
                                                  'placeholder': 'Opcional'}),
        }

class CierreDiaForm(forms.ModelForm):
    class Meta:
        model = CierreDia
        fields = ['ventas_totales_sistema', 'efectivo_en_caja', 'observaciones']
        labels = {
            'ventas_totales_sistema': 'Total de Ventas del Dia ($)',
            'efectivo_en_caja': 'Efectivo En Caja ($)',
            'observaciones': 'Notas del Cierre (Opcional)'
        }
        widgets = {
            'ventas_totales_sistema': forms.NumberInput(attrs={'class':'block w-full bg-gray-700 border-gray-600 text-gray-300 rouded p-3 text-lg font-mono cursor-not-allowed', 'readonly': 'readonly'}),
            'efectivo_en_caja': forms.NumberInput(attrs={'class':'block w-full bg-gray-800 border-green-500 text-white rounded p-4 text-2xl font-bold focus:ring-2 focus:ring-green-500 outline-none',
                                                        'placeholder': ' 0.00',
                                                        'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class':'block w-full bg-gray-700 text-white rounded p-3 focus:border-blue-500 outline-none',
                                                    'rows': 3,
                                                    'placeholder': 'Ej: Faltaron 50$ en caja, se compro pan de emergencia'}),        
        }

