from django.shortcuts import render, HttpResponse, redirect

#--------------------------
# inicializacion
prioridad_amarillo = 0 
prioridad_verde = 0
prioridad_rojo = 0

destino_amarillo = 0 
destino_verde = 0 
destino_rojo = 0
#--------------------------
# Create your views here.
def home(request):
    return render(request, 'homepage/index.html')

def PrioridadPaquete(request):
   
    return render(request, 'homepage/PrioridadPaquete.html')

def DestinoPaquete(request):
     if request.method == 'POST':

        # ---------------------------
        # Declarar valores globales en este modulo
        global prioridad_amarillo 
        global prioridad_verde 
        global prioridad_rojo
        # ---------------------------
        prioridad_amarillo = request.POST.get('select1')
        prioridad_verde = request.POST.get('select2')
        prioridad_rojo = request.POST.get('select3')

        return render(request, 'homepage/ColorDestino.html')
    
     else:
        # renderizar la plantilla del formulario
        return render(request, 'homepage/ColorDestino.html')

def IniciarProceso(request):
    if request.method == 'POST':
        global destino_amarillo
        global destino_verde
        global destino_rojo

        destino_amarillo = request.POST.get('select1')
        destino_verde = request.POST.get('select2')
        destino_rojo = request.POST.get('select3')
 
        return render(request, 'homepage/Start.html')
    else:
        # renderizar la plantilla del formulario
        return render(request, 'homepage/Start.html')

