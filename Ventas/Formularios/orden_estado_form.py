from django import forms
from Ventas.models import Orden

class OrdenEstadoForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['estado']
        labels = {
            'estado': 'Estado de la Orden',
        }
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-select block w-full mt-1',
                'id': 'id_estado'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)