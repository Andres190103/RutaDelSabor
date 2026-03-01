from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


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


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
