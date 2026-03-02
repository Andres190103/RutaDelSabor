import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction # Importante para guardar receta y producto juntos

from .models import Producto
from Ventas.models import Orden, DetalleOrden
from Inventario.models import Ingrediente
from .forms import ProductoForm, RecetaFormSet
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        # SI ES UN SUPERUSUARIO SE LE DA ACCESO
        if user.is_superuser:
            return True
        # SI EL USUARIO ESTA REGISTRADO CON EL ROL DE ADMIN SE LE DA ACCESO TAMBIEN
        if hasattr(user, 'perfil') and user.perfil.rol:
            return user.perfil.rol.nombre.lower() == 'admin'
        # SI NO CUMPLE CON NINGUNA DE LAS ANTERIORES, SE LE NIEGA EL ACCESO
        return False

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'FoodTruck/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        es_admin = False
        es_chef = False
        es_cajero = False

        if user.is_superuser:
            es_admin = True
        elif hasattr(user, 'perfil') and user.perfil.rol:
            roll = user.perfil.rol.nombre
            if roll.lower() == 'admin': 
                es_admin = True
            elif roll.lower() == 'chef':
                es_chef = True
            elif roll.lower() == 'cajero':
                es_cajero = True

        context['es_admin'] = es_admin
        context['es_chef'] = es_chef
        context['es_cajero'] = es_cajero

        # DATOS PARA EL DASHBOARD
        if es_admin or es_chef or es_cajero:
            context['ordenes_pendientes'] = Orden.objects.filter(estado__in=['Pendiente', 'Preparando']).count()

        # ALERTAS DE STOCK PARA LA VISUALIZACION DE EL ADMIN
        if es_admin:
            from django.db.models import F
            context['alertas_stock'] = Ingrediente.objects.filter(stock_actual__lte=F('stock_minimo')).count()
        
        # DATOS PARA EL DASHBOARD ESTADISTICO
        if es_admin:
            hoy = timezone.now().date()

            # INGRESOS DEL DIA
            ordenes_hoy = Orden.objects.filter(creado_en__date=hoy, estado='Entregado')
            ventas_hoy = ordenes_hoy.exclude(estado='Cancelado').aggregate(Sum('total'))['total__sum']
            context['ingresos_hoy'] = ventas_hoy if ventas_hoy is not None else 0.00

            # GRAFICA DE LOS ULTIMOS 7 DIAS
            fechas_str = []
            ventas_diarias = []

            for i in range(6, -1, -1):
                dia = hoy - timedelta(days=i)
                fechas_str.append(dia.strftime('%d %b'))

                # Suma de ventas del día
                total_dia = Orden.objects.filter(
                    creado_en__date=dia
                ).exclude(estado='Cancelado').aggregate(Sum('total'))['total__sum']
                ventas_diarias.append(float(total_dia or 0.00))

                # CONVERTIMOS LAS LISTAS A JSON PARA QUE JAVASCRIPT LAS PUEDA LEER EN EL HTML
                context['fechas_chart'] = json.dumps(fechas_str)
                context['ventas_chart'] = json.dumps(ventas_diarias)

        return context


class MenuListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Producto
    template_name = 'FoodTruck/producto_list.html'
    context_object_name = 'productos'

class ProductoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'FoodTruck/producto_form.html'
    success_url = reverse_lazy('menu_list')

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

# EDITAR PLATILLO (Misma lógica pero con datos existentes)
class ProductoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
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
    
class ProductoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Producto
    template_name = 'FoodTruck/producto_confirm_delete.html'
    success_url = reverse_lazy('menu_list')
