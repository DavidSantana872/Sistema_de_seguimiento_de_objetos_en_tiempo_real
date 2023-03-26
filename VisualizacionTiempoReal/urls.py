from django.urls import path
from . import views

urlpatterns = [
    path('', views.Visualizacion, name='VisualizacionTiempoReal'),
    # otras urls y vistas de la app2
]
