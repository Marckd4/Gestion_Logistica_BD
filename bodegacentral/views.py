from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from bodegacentral.forms import CentralForm
from .models import Central # IMPORTAR EL MODEL 

def index(request):
    centrales = Central.objects.all()
   
    return render(request, 'central.html', context={'centrales':centrales})

# area formulario 

def formulario(request):
    if request.method == 'POST':
        form = CentralForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bodegacentral')
    else:
        form = CentralForm()
            
    
    return render( request, 'central_form.html',{'form': form})