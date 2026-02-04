from django.urls import path
from .views import *

urlpatterns = [
    path('create/', ProductoCreateView.as_view(), name='producto_create'),
    path('', MenuListView.as_view(), name='menu_list'),
    path('update/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
]