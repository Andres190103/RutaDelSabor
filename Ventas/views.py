from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from .models import Orden
from Ventas.Formularios.orden_form import OrdenForm
from Ventas.Formularios.orden_estado_form import OrdenEstadoForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.db import transaction

from Ventas.Formularios.orden_form import DetalleOrdenFormSet, OrdenForm
from Ventas.Formularios.orden_estado_form import OrdenEstadoForm

from foodtruck.models import Producto
import json
import csv
from django.http import HttpResponse


# Create your views here.

class listOrdenes(LoginRequiredMixin, ListView):
    model = Orden
    template_name = 'Ventas/orden_list.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser:
            # El "Dios" del sistema ve todo
            return Orden.objects.all().order_by('-creado_en')
        
        if not hasattr(user, 'perfil'):
            return Orden.objects.none()
        
        rol = user.perfil.rol.nombre

        if rol == 'Chef':
            return Orden.objects.filter(estado__in=['Pendiente', 'Preparando']).order_by('creado_en')
        
        return Orden.objects.all().order_by('creado_en')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_superuser:
            context['es_chef'] = False
            context['es_admin'] = True

        elif hasattr(user, 'perfil') and user.perfil.rol:
            context['es_chef'] = user.perfil.rol.nombre == 'Chef'
            context['es_admin'] = user.perfil.rol.nombre == 'Admin'
        
        return context

class CreateViewOrden(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = OrdenForm
    template_name = 'Ventas/orden_form.html'
    model = Orden
    success_url = reverse_lazy('orden_list')

    # 1. Enviar el Formset (la tabla de productos) al HTML
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Si el usuario envió datos, recargamos el formset con esa info
            data['detalles'] = DetalleOrdenFormSet(self.request.POST)
        else:
            # Si es la primera vez que entra, se muestra la tabla vacía
            data['detalles'] = DetalleOrdenFormSet()

        precios = {p.id: float(p.precio) for p in Producto.objects.all()}
        data['precios_json'] = json.dumps(precios) 

        return data

    # 2. Guardar todo junto (Orden + Productos)
    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['detalles']
        
        with transaction.atomic():
            # Primero se guarda la Orden (para que tenga un ID)
            self.object = form.save()
            
            if detalles.is_valid():
                # Asignamos la ID de la orden recién creada a los productos
                detalles.instance = self.object
                detalles.save()
                
                if hasattr(self.object, 'actualizar_total'):
                    self.object.actualizar_total()
            else:
                # Si los productos tienen error, volvemos a mostrar el formulario
                return self.render_to_response(self.get_context_data(form=form))
                
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
 
        if user.is_superuser:
            return True
            
        # Si es empleado normal, verificamos su rol
        if hasattr(user, 'perfil') and user.perfil.rol:
            return user.perfil.rol.nombre != 'Chef'
            
        # Si no es superusuario y no tiene perfil, bloqueamos
        return False
    
    def handle_no_permission(self):
        return redirect('orden_list')
        
class UpdateViewOrden(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Orden
    template_name = 'Ventas/orden_estado_form.html'
    form_class = OrdenEstadoForm
    success_url = reverse_lazy('orden_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        precios = {p.id: float(p.precio) for p in Producto.objects.all()}
        context['precios_json'] = json.dumps(precios)

        if user.is_superuser:
            context['es_chef'] = False
        elif hasattr(user, 'perfil') and user.perfil.rol:
            context['es_chef'] = user.perfil.rol.nombre == 'Chef'
        return context
        
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return hasattr(user, 'perfil') and user.perfil.rol is not None
    
class DeleteViewOrden(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Orden
    template_name = 'Ventas/orden_confirm_delete.html'
    success_url = reverse_lazy('orden_list')

    def test_func(self):
        user = self.request.user

        if user.is_superuser:
            return True
        
        if hasattr(user, 'perfil') and user.perfil.rol:
            return user.perfil.rol.nombre == 'Admin'
        return False

@login_required   
def exportar_csv(request):
    user = request.user
    es_admin = user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol and user.perfil.rol.nombre == 'Admin')
    
    if not es_admin:
        return redirect('start_home')

    # SE PREPARA LA RESPUESTA HTTP PARA QUE EL NAVEGADOR SEPA QUE ES UN ARCHIVO DESCARGABLE
    response = HttpResponse(content_type='text/csv')
    # SE LE ASIGNA EL NOMBRE AL ARCHIVO QUE SE VA A DESCARGAR
    response['Content-Disposition'] = 'attachment; filename="Reporte_Ventas_RutaDelSabor.csv"'
    # CREACION DEL OBJETO CSV WRITER PARA ESCRIBIR EN EL ARCHIVO
    writer = csv.writer(response)
    # SE ESCRIBE LA PRIMERA FILA CON LOS NOMBRES DE LAS COLUMNAS
    writer.writerow(['ID de Orden', 'Cliente', 'Estado de la Orden', 'Total ($)', 'Fecha y Hora'])
    # SE OBTIENEN TODAS LAS ORDENES DE LA BASE DE DATOS
    ordenes = Orden.objects.all().order_by('-creado_en')

    for orden in ordenes:
        fecha_formateada = orden.creado_en.strftime("%d/%m/%Y %H:%M")

        writer.writerow([
            orden.id,
            orden.cliente_nombre,
            orden.estado,
            orden.total,
            fecha_formateada
        ])
    return response