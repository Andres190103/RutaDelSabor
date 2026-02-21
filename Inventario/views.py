from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from Inventario.models import *
from .forms import IngredienteForm, CompraInsumoForm, CierreDiaForm
from Ventas.models import Orden

# Create your views here.

class CreateViewIngrediente(LoginRequiredMixin, CreateView):
    form_class = IngredienteForm
    model = Ingrediente
    template_name = 'Inventario/ingrediente_form.html'
    success_url = reverse_lazy('ingrediente_create')

class IngredienteListView(LoginRequiredMixin, ListView):
    model = Ingrediente
    template_name = 'Inventario/ingrediente_list.html'
    context_object_name = 'ingredientes'

    def get_queryset(self):
        return Ingrediente.objects.all().order_by('nombre')
    
class IngredienteUpdateView(UpdateView):
    form_class = IngredienteForm
    model = Ingrediente
    template_name = 'Inventario/ingrediente_form.html'
    success_url = reverse_lazy('ingrediente_list')

class IngredienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingrediente
    template_name = 'Inventario/ingrediente_confirm_delete.html'
    success_url = reverse_lazy('ingrediente_list')

class CompraInsumoCreateView(LoginRequiredMixin, CreateView):
    model = CompraInsumo
    form_class = CompraInsumoForm
    template_name = 'Inventario/compra_form.html'
    success_url = reverse_lazy('ingrediente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'ingrediente_id' in self.request.GET:
            context['ingrediente_preseleccionado'] = int(self.request.GET.get('ingrediente_id'))
        return context
    
class CierreDiaCreateView(LoginRequiredMixin, CreateView):
    model = CierreDia
    form_class = CierreDiaForm
    template_name = 'Inventario/cierre_form.html'
    success_url = reverse_lazy('cierre_list')

    def get_initial(self):
        # Calculo de el total vendido en el dia
        today = timezone.now().date()
        # Filtrar ordenes Pagadas/entregadas en el dia
        ventas_today = Orden.objects.filter(
            creado_en__date=today,
            estado='Entregado'
        ).aggregate(total_dia=Sum('total'))

        total = ventas_today['total_dia'] or 0.00

        return {
            'ventas_totales_sistema': total
        }
    
    def form_valid(self, form):
        # Calcular la diferencia automaticamente antes de guardar
        cierre = form.save(commit=False)
        cierre.responsable = self.request.user # Se guarga el usuario que hizo el corte
        # Calculo de la diferencia entre lo que hay en caja vs las ventas totales registrados
        cierre.diferencia = cierre.efectivo_en_caja - cierre.ventas_totales_sistema
        cierre.save()
        return super().form_valid(form)
    
class CierreDiaListView(LoginRequiredMixin, ListView):
    model = CierreDia
    template_name = 'Inventario/cierre_list.html'
    context_object_name = 'cierres'

    def get_queryset(self):
        return CierreDia.objects.all().order_by('-fecha')