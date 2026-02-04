from django.db import models
from django.contrib.auth.models import User


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    contacto_nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    dias_visita = models.CharField(max_length=100, blank=True, help_text="Ej: Lunes y Jueves")

    def __str__(self):
        return self.nombre_empresa

class Ingrediente(models.Model):
    UNIDADES = [
        ('kg', 'Kilogramos'),
        ('gr', 'Gramos'),
        ('lt', 'Litros'),
        ('ml', 'Mililitros'),
        ('pz', 'Piezas'),
    ]
    nombre = models.CharField(max_length=100)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=3) # 3 decimales para precisión en gramos
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=3)
    unidad_medida = models.CharField(max_length=5, choices=UNIDADES)
    ultimo_costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    proveedor_principal = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    def alerta_stock(self):
        return self.stock_actual <= self.stock_minimo

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual} {self.unidad_medida})"

class CompraInsumo(models.Model):
    """
    Registra cuando compras insumos para aumentar el stock.
    Fundamental para el Módulo de Proveedores y Finanzas.
    """
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    factura_ref = models.CharField(max_length=50, blank=True, help_text="Folio de factura o ticket")

    def save(self, *args, **kwargs):
        # Lógica simple: Al guardar una compra, sumamos al stock
        if not self.pk: # Solo si es nueva compra
            self.ingrediente.stock_actual += self.cantidad
            self.ingrediente.ultimo_costo = self.costo_total / self.cantidad
            self.ingrediente.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra {self.ingrediente.nombre} - {self.fecha_compra.date()}"
    
class CierreDia(models.Model):
    """
    Para la funcionalidad de Cierre de Turno.
    Compara lo que el sistema dice que vendiste vs lo que cuentas físicamente.
    """
    fecha = models.DateField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    
    ventas_totales_sistema = models.DecimalField(max_digits=10, decimal_places=2)
    efectivo_en_caja = models.DecimalField(max_digits=10, decimal_places=2)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, help_text="Efectivo - Sistema")
    
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Cierre {self.fecha} - {self.responsable.username}"
    