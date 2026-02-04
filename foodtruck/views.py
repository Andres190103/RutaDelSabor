from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction # Importante para guardar receta y producto juntos

from .models import Producto
from .forms import ProductoForm, RecetaFormSet

# 1. LISTA DEL MENÚ
class MenuListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'FoodTruck/producto_list.html'
    context_object_name = 'productos'

# 2. CREAR PLATILLO (Aquí es donde estaba faltando la lógica del formset)
class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'FoodTruck/producto_form.html'
    success_url = reverse_lazy('menu_list')

    # ESTO ES LO QUE FALTABA: Enviar la tabla de ingredientes al HTML
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['receta_formset'] = RecetaFormSet(self.request.POST)
        else:
            data['receta_formset'] = RecetaFormSet()
        return data

    # Lógica para guardar ambas cosas (Producto + Ingredientes)
    def form_valid(self, form):
        context = self.get_context_data()
        recetas = context['receta_formset']
        
        with transaction.atomic():
            self.object = form.save() # 1. Guardamos el platillo
            
            if recetas.is_valid():
                recetas.instance = self.object # 2. Asignamos el platillo a los ingredientes
                recetas.save() # 3. Guardamos los ingredientes
            else:
                # Si hay error en los ingredientes, recargamos la página
                return self.render_to_response(self.get_context_data(form=form))
                
        return super().form_valid(form)

# 3. EDITAR PLATILLO (Misma lógica pero con datos existentes)
class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'FoodTruck/producto_form.html'
    success_url = reverse_lazy('menu_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['receta_formset'] = RecetaFormSet(self.request.POST, instance=self.object)
        else:
            # Aquí cargamos los ingredientes que ya existían en la base de datos
            data['receta_formset'] = RecetaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        recetas = context['receta_formset']
        
        with transaction.atomic():
            self.object = form.save()
            if recetas.is_valid():
                recetas.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))
                
        return super().form_valid(form)
    
