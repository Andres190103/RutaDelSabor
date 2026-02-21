from django.urls import path
from Inventario.views import *

urlpatterns = [
    path('ingrediente/create/', CreateViewIngrediente.as_view(), name='ingrediente_create'),
    path('ingrediente/list/', IngredienteListView.as_view(), name='ingrediente_list'),
    path('ingrediente/update/<int:pk>/', IngredienteUpdateView.as_view(), name='ingrediente_update'),
    path('ingrediente/delete/<int:pk>/', IngredienteDeleteView.as_view(), name='ingrediente_delete'),
    path('compra/create/', CompraInsumoCreateView.as_view(), name='compra_create'),

    path('cierre/create/', CierreDiaCreateView.as_view(), name='cierre_create'),
    path('cierre/list/', CierreDiaListView.as_view(), name='cierre_list'),
]