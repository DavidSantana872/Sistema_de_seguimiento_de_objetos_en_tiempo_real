from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('PrioridadPaquete/', views.PrioridadPaquete, name = 'PrioridadPaquete'),
    path('DestinoPaquete/', views.DestinoPaquete, name='DestinoPaquete'),
    path('IniciarProceso/', views.IniciarProceso, name='Start'),

]