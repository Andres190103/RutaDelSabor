from django.db import models
from django.contrib.auth.models import User
from foodtruck.models import Producto  # <--- Importamos el producto para venderlo

class Orden(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Preparando', 'En preparación'),
        ('Listo', 'Listo para entregar'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Quién tomó la orden")
    cliente_nombre = models.CharField(max_length=100, default="Cliente General") # Para llamar al cliente
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    inventario_descontado = models.BooleanField(default=False, help_text="Evita doble descuento")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Tiempos para analíticas
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True) # Sirve para ver cuánto tardó en salir
    
    def tiempo_espera(self):
        return self.actualizado_en - self.creado_en

    def __str__(self):
        return f"Orden #{self.id} - {self.estado}"
    
    def actualizar_total(self):
        # Calculamos la suma de los subtotales de los productos relacionados
        nuevo_total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = nuevo_total
        self.save()

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.CharField(max_length=200, blank=True, help_text="Ej: Sin cebolla")

    def save(self, *args, **kwargs):
        # Calcular subtotal automáticamente
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
    
    def save(self, *args, **kwargs):
        # Aseguramos que el subtotal siempre sea precio * cantidad
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)