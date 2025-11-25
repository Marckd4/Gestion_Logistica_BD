

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
        data["total_cajas"] = data["cajas_bsf"] + data["cajas_central"]
        resumen.append(data)

    return render(request, "resumen_unificado.html", {"resumen": resumen})



# resumen exportar excel 
def exportar_resumen_excel(request):
    import openpyxl
    from openpyxl.styles import Font
    from django.http import HttpResponse
    from collections import defaultdict
    from bodegabsf.models import Bsf
    from bodegacentral.models import Central

    # ==== Construcción del resumen (igual que en la vista HTML) ====
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

    # Convertir resumen
    resumen = []
    for data in resumen_dict.values():
        data["total_cajas"] = data["cajas_bsf"] + data["cajas_central"]
        resumen.append(data)

    # ==== Crear Excel ====
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resumen Inventario"

    columnas = [
        "Cod DUN",
        "Cod EAN",
        "Cod Sistema",
        "Descripción",
        "Cajas Bsf",
        "Cajas Central",
        "Stock Bsf",
        "Stock Central",
        "Total Cajas Lingues + Bsf",
    ]

    # Encabezados
    for col_num, columna in enumerate(columnas, 1):
        celda = ws.cell(row=1, column=col_num, value=columna)
        celda.font = Font(bold=True)

    # Filas
    for row_num, item in enumerate(resumen, 2):
        ws.cell(row=row_num, column=1, value=item["cod_dun"])
        ws.cell(row=row_num, column=2, value=item["cod_ean"])
        ws.cell(row=row_num, column=3, value=item["cod_sistema"])
        ws.cell(row=row_num, column=4, value=item["descripcion"])
        ws.cell(row=row_num, column=5, value=item["cajas_bsf"])
        ws.cell(row=row_num, column=6, value=item["cajas_central"])
        ws.cell(row=row_num, column=7, value=item["stock_bsf"])
        ws.cell(row=row_num, column=8, value=item["stock_central"])
        ws.cell(row=row_num, column=9, value=item["total_cajas"])

    # Respuesta
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="resumen_unificado.xlsx"'

    wb.save(response)
    return response
