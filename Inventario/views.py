from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from Inventario.models import *
from .forms import IngredienteForm

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