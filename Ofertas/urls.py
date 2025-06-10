from django.urls import path
from . import views

from Ofertas.views import inicioVista, listadoOfertasVista, reporteOfertasVista

# app_name = 'Ofertas'

urlpatterns = [
    # path('perfil/<int:pk>', PerfilOpenVista, name='perfil'),    
    path('', inicioVista, name='inicio'),
    path('listado_ofertas', listadoOfertasVista, name='listado-ofertas'),
    path('reporte_ofertas/', reporteOfertasVista, name='reporte-ofertas'),
    
]

