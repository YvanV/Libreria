import logging
from django.shortcuts import render

from Ofertas.models import Oferta
from .forms import BuscaOfertaForm

# Create your views here.

sesionInfoInicial = {"busqueda": {}}

def inicioVista(request):
    return render(request, 'Ofertas/inicio.html')

def listadoOfertasVista(request):
    listaOfertas = []
    for oferta in Oferta.objects.all():
        elemento = {
            "titulo": oferta.titulo,
            "autor": oferta.autor,
            "precio": oferta.precio_en_texto,
            "ingreso": oferta.fecha_ingreso,
            "salida": oferta.fecha_salida,
            "estado": oferta.estado
            }
        listaOfertas.append(elemento)
    contexto = {
        "lista_ofertas": listaOfertas
        }

    return render(request, "Ofertas/listado_ofertas.html", contexto)

def reporteOfertasVista(request):

    logger = logging.getLogger(__name__)
    sesionInfo = request.session["sesion_info"] if "sesion_info" in request.session else sesionInfoInicial
    logger.error("reporteOfertasVista: inicio")

    form = BuscaOfertaForm(request.GET)
    tituloBuscado = request.GET.get('titulo', None)
    autorBuscado = request.GET.get('autor', None)
    estadoBuscado = request.GET.get('estado', None)
    qsOfertas = Oferta.objects.all()
    if tituloBuscado is not None and tituloBuscado != "":
        qsOfertas = qsOfertas.filter(titulo__icontains=tituloBuscado) 
    if autorBuscado is not None and autorBuscado != "":
        qsOfertas = qsOfertas.filter(autor__icontains=autorBuscado) 
    if estadoBuscado is not None and estadoBuscado != "":
        qsOfertas = qsOfertas.filter(estado=estadoBuscado) 
    qsOfertas = qsOfertas.order_by("-fecha_ingreso")

    listaOfertas = qsOfertas

    request.session["sesion_info"] = sesionInfo
    
    contexto = {
        "sesion_info": sesionInfo,
        "form": form,
        "lista_ofertas": listaOfertas}
    return render(request, 'Ofertas/reporte_ofertas.html', contexto)    

