from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def home(request):
    return render(request, 'homepage/index.html')

def PrioridadPaquete(request):
   
    return render(request, 'homepage/PrioridadPaquete.html')

def DestinoPaquete(request):
     if request.method == 'POST':
        select1_value = request.POST.get('select1')
        select2_value = request.POST.get('select2')
        select3_value = request.POST.get('select3')
        return render(request, 'homepage/ColorDestino.html')
    

        # hacer algo con los valores de los selectores
     else:
        # renderizar la plantilla del formulario
        return render(request, 'homepage/ColorDestino.html')

def IniciarProceso(request):
    if request.method == 'POST':
        select4_value = request.POST.get('select1')
        select5_value = request.POST.get('select2')
        select6_value = request.POST.get('select3')
        return render(request, 'homepage/Start.html')
    

        # hacer algo con los valores de los selectores
    else:
        # renderizar la plantilla del formulario
        return render(request, 'homepage/Start.html')


