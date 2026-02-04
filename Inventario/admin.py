from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Ingrediente)
admin.site.register(Proveedor)
admin.site.register(CompraInsumo)
admin.site.register(CierreDia)