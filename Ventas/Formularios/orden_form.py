from django import forms
from Ventas.models import DetalleOrden, Orden
from django.forms import inlineformset_factory

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = "__all__"
        labels = {
            'estado': 'Estado de la Orden',
            'total': 'Total a Pagar',
            'usuario': 'Cocinero Asignado',
        }
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }

DetalleOrdenFormSet = inlineformset_factory(
    Orden,
    DetalleOrden,
    fields=('producto', 'cantidad', 'notas'),
    extra=1,
    can_delete=True
    
)