from django.urls import path
from Ventas.views import *
from . import views

urlpatterns = [
    path('orden/create/', CreateViewOrden.as_view(), name='orden_create'),
    
    path('orden/estado/<int:pk>/', UpdateViewOrden.as_view(), name='orden_update'),

    path('orden/list/', listOrdenes.as_view(), name='orden_list'),

    path('orden/delete/<int:pk>/', DeleteViewOrden.as_view(), name='orden_delete'),

    path('orden/exportar/', exportar_csv, name='exportar_ventas'),
]