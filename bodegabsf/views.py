
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from bodegabsf.forms import BsfForm
from .models import Bsf  # importar el modelo

def data(request):
    bsfs = Bsf.objects.all()
    return render(request, 'index.html', context={'bsfs': bsfs})

# area formulario 

def formulario(request):
    if request.method == 'POST':
        form = BsfForm(request.POST)
        if form.is_valid():
             form.save()
             return HttpResponseRedirect('/bodegabsf')
    else:
        form = BsfForm()
        
        
    return render( request, 'bsf_form.html',{'form': form})
