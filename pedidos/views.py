from django.http import HttpResponse
from django.shortcuts import render

def notadeventas(request):
    return HttpResponse("Ingreso de Mercaderia")