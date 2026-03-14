from django.db import models
import Inventario
from Inventario.models import Ingrediente  
from decimal import Decimal

class ConfiguracionNegocio(models.Model):
    nombre_foodtruck = models.CharField(max_length=100)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    ultima_actualizacion_ubicacion = models.DateTimeField(auto_now=True)
    mensaje_cierre = models.CharField(max_length=255, blank=True, help_text="Mensaje para redes sociales")

    def __str__(self):
        return self.nombre_foodtruck

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100, blank=True, help_text="Nombre del icono para el frontend")

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='platillos/', null=True, blank=True) # Para Cloudinary
    activo = models.BooleanField(default=True) # Para mostrar/ocultar en menú QR sin borrar
    ingredientes = models.ManyToManyField(Inventario.models.Ingrediente, through='Receta')
    porcentaje_ganancia = models.DecimalField(
        max_digits=5, decimal_places=2, default=30.00
    )
    porcentaje_iva = models.DecimalField(
        max_digits=5, decimal_places=2, default=16.00
    )
    @property
    def costo_base_escandallo(self):
        costo_total = Decimal('0.00')
        for receta in self.receta_set.all():
            if receta.ingrediente.ultimo_costo:
                costo_total += (receta.ingrediente.ultimo_costo * receta.cantidad_necesaria)
        return round(costo_total, 2)
    @property
    def precio_sugerido(self):
        costo = self.costo_base_escandallo

        if costo == 0:
            return Decimal('0.00')
        
        ganancia = costo * (self.porcentaje_ganancia / Decimal('100.00'))

        subtotal = costo + ganancia

        iva = subtotal * (self.porcentaje_iva / Decimal('100.00'))

        return round(subtotal + iva, 2)
    
    def __str__(self):
        return self.nombre

class Receta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Inventario.models.Ingrediente, on_delete=models.CASCADE)
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=3, help_text="Cantidad a descontar por venta")

    def __str__(self):
        return f"{self.producto.nombre} usa {self.cantidad_necesaria} de {self.ingrediente.nombre}"