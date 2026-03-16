from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
#Importaciones de lo VioewSets de las Apps
from foodtruck.api import *
from Usuarios.api import *
from Ventas.api import *
from Inventario.api import *

#Creacion de un enrutador global
router = DefaultRouter()

#Rutas de la app foodtruck
router.register(r'categorias', CategoriaViewSet, basename= 'api-categorias')
router.register(r'productos', ProductoViewSet, basename='api-productos')
router.register(r'recetas', RecetaViewSet, basename='api-recetas')
router.register(r'configuracion', ConfiguracionNegocioViewSet, basename = 'api-configuracion')
#Rutas de la app Usuarios
router.register(r'users', UserViewSet, basename = 'api-users')
router.register(r'roles', RolesViewSet, basename = 'api-roles')
router.register(r'perfiles', PerfilUsuarioViewSet, basename = 'api-perfiles')
#Rutas de la app Ventas
router.register(r'detalle-orden', DetalleOrdenViewSet, basename = 'api-detalle-orden')
router.register(r'ordenes', OrdenViewSet, basename = 'api-ordenes')
#Rutas de la app Inventario
router.register(r'proveedores', ProveedorViewSet, basename = 'api-proveedores')
router.register(r'ingredietnes', IngredienteViewSet, basename = 'api-ingredientes')
router.register(r'compras', CompraInsumoViewSet, basename = 'api-compras')
router.register(r'cierres', CierreDiaViewSet, basename = 'api-cierres')

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='start_page'),

    path('admin/', admin.site.urls),
    #URL de la app foodtruck
    path('', include('foodtruck.urls')),
    #URL de la app Usuarios
    path('', include('Usuarios.urls')),
    #URL de la app Ventas
    path('', include('Ventas.urls')),
    #URL de la app Inventario
    path('', include('Inventario.urls')),
    
    path('accounts/', include('django.contrib.auth.urls')),

    path('api/login/', LoginPersonalizado.as_view(), name='api-login'),

    path('api/', include(router.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
