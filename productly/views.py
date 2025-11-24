from django.shortcuts import render

def inicio (request):
    return render( render,'inicio.html')


# resumen data tablas 
from django.shortcuts import render
from bodegabsf.models import Bsf
from bodegacentral.models import Central
from collections import defaultdict

def inicio(request):
    return render(request, 'inicio.html')

def resumen_unificado(request):

    resumen_dict = defaultdict(lambda: {
        "cod_dun": "",
        "cod_ean": "",
        "cod_sistema": "",
        "descripcion": "",
        "cajas_bsf": 0,
        "cajas_central": 0,
        "stock_bsf": 0,
        "stock_central": 0,
    })

    # --- Datos BSF ---
    for b in Bsf.objects.all():
        d = resumen_dict[b.cod_dun]
        d["cod_dun"] = b.cod_dun
        d["cod_ean"] = b.cod_ean
        d["cod_sistema"] = b.cod_sistema
        d["descripcion"] = b.descripcion
        d["cajas_bsf"] += b.cajas or 0
        d["stock_bsf"] += b.stock_fisico or 0

    # --- Datos Central ---
    for c in Central.objects.all():
        d = resumen_dict[c.cod_dun]
        d["cod_dun"] = c.cod_dun
        d["cod_ean"] = c.cod_ean
        d["cod_sistema"] = c.cod_sistema
        d["descripcion"] = c.descripcion
        d["cajas_central"] += c.cajas or 0
        d["stock_central"] += c.stock_fisico or 0

    # Convertir a lista final con diferencias
    resumen = []
    for data in resumen_dict.values():
        data["diferencia_stock"] = data["stock_bsf"] - data["stock_central"]
        resumen.append(data)

    return render(request, "resumen_unificado.html", {"resumen": resumen})
