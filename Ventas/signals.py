from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Orden
from Inventario.models import Ingrediente
from foodtruck.models import Receta

@receiver(post_save, sender=Orden)
def descontar_stock_al_entregar(sender, instance, created, **kwargs):
    """
    Al cambiar el estado de una orden a 'Entregado', descontar los ingredientes del inventario.
    Solo si no se ha descontado antes (evitar doble descuento).
    """
    if not created and instance.estado == 'Entregado' and not instance.inventario_descontado:
        """
    Se ejecuta cada vez que se guarda una Orden.
    Verifica si el estado es 'Entregado' y si aún no se ha descontado stock.
    """
    
    # Solo procedemos si la orden está 'Entregada' y NO se ha descontado antes
    if instance.estado == 'Entregado' and not instance.inventario_descontado:
        
        # Se usa 'atomic' para asegurar que si algo falla, no se descuente nada a medias
        with transaction.atomic():
            
            # 1. Obtenemos todos los platillos (detalles) de esta orden
            detalles = instance.detalles.all()
            
            for detalle in detalles:
                producto = detalle.producto
                cantidad_vendida = detalle.cantidad
                
                # 2. Buscamos la receta de cada producto
                # (relación inversa: producto.receta_set.all() o filtrando Receta)
                recetas_del_producto = Receta.objects.filter(producto=producto)
                
                for receta in recetas_del_producto:
                    insumo = receta.ingrediente
                    cantidad_unitaria = receta.cantidad_necesaria
                    
                    # 3. Calculamos cuánto descontar
                    # (Lo que lleva 1 hamburguesa * cuántas hamburguesas se vendieron)
                    total_a_descontar = cantidad_unitaria * cantidad_vendida
                    
                    # 4. Actualizamos el stock del ingrediente
                    insumo.stock_actual -= total_a_descontar
                    insumo.save()
                    
                    print(f"Descontado {total_a_descontar} {insumo.unidad_medida} de {insumo.nombre}")

            # 5. Marcamos la orden como procesada para no volver a descontar
            instance.inventario_descontado = True
            instance.save(update_fields=['inventario_descontado'])
