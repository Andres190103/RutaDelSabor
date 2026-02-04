from django.urls import path
from .views import *

urlpatterns = [
    path('Usuarios/', home, name='home'),
]