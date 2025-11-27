from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm # formato de extarer fprmulario

def usuario(request):
    return render (request, 'data_usuario.html',{
        'form':UserCreationForm
    })
    
def home(request):
    return render(request, 'home.html')