from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #URL de la app foodtruck
    path('menu/', include('foodtruck.urls')),
    #URL de la app Usuarios
    path('', include('Usuarios.urls')),
    #URL de la app Ventas
    path('', include('Ventas.urls')),
    #URL de la app Inventario
    path('', include('Inventario.urls')),
    
    path('api-auth/', include('rest_framework.urls')),
    
    path('accounts/', include('django.contrib.auth.urls')),
]
