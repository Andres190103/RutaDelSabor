from django.contrib import admin
from .models import Orden
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

#admin.site.register(Orden)
#admin.site.register(DetalleOrden)

class OrdenResource(resources.ModelResource):
    class Meta:
        model = Orden
        fields = ('id', 'cliente_nombre', 'total', 'estado', 'creado_en')

class OrdenAdmin(ImportExportModelAdmin):
    resource_class = OrdenResource
    list_display = ('id', 'cliente_nombre', 'total', 'estado', 'creado_en')

admin.site.register(Orden, OrdenAdmin)