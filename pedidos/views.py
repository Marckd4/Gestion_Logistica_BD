from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .forms import NotaVentaForm
from .models import NotaVenta, DetalleNota

from bodegabsf.models import Bsf
from bodegacentral.models import Central


# ==============================
# CREAR NOTA
# ==============================

@login_required
def crear_nota(request):
    if request.method == 'POST':
        form = NotaVentaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.vendedor = request.user
            nota.save()
            return redirect('agregar_producto', nota_id=nota.id)
    else:
        form = NotaVentaForm()

    return render(request, 'pedidos/crear_nota.html', {'form': form})


# ==============================
# AGREGAR PRODUCTOS
# ==============================

from django.shortcuts import render, redirect, get_object_or_404
from .models import NotaVenta, DetalleNota
from bodegabsf.models import Bsf
from bodegacentral.models import Central


def agregar_producto(request, nota_id):
    nota = get_object_or_404(NotaVenta, id=nota_id)

    # Si no tiene bodega asignada, debe seleccionarla primero
    if not nota.tipo_bodega:
        if request.method == "POST":
            bodega = request.POST.get("bodega")
            if bodega in ['bsf', 'central']:
                nota.tipo_bodega = bodega
                nota.save()
                return redirect("agregar_producto", nota_id=nota.id)
        
        return render(request, "pedidos/seleccionar_bodega.html", {"nota": nota})

    if nota.tipo_bodega == "bsf":
        productos = Bsf.objects.filter(cajas__gt=0)
    else:
        productos = Central.objects.filter(cajas__gt=0)

    if request.method == "POST":
        producto_id = request.POST.get("producto")
        cantidad = int(request.POST.get("cantidad"))
        precio_caja = float(request.POST.get("precio_caja"))

        if nota.tipo_bodega == "bsf":
            producto = get_object_or_404(Bsf, id=producto_id)
        else:
            producto = get_object_or_404(Central, id=producto_id)

        if producto.cajas >= cantidad:

            DetalleNota.objects.create(
                nota=nota,
                codigo=producto.cod_sistema,
                descripcion=producto.descripcion,
                ean=producto.cod_ean,
                dun=producto.cod_dun,
                formato_venta=producto.unidad,
                cantidad_solicitada=cantidad,
                capacidad_x_caja=producto.pack,
                precio_x_caja=precio_caja
            )

            producto.cajas -= cantidad
            producto.save()

            return redirect("agregar_producto", nota_id=nota.id)

    return render(request, "pedidos/agregar_producto.html", {
        "nota": nota,
        "productos": productos
    })


# ==============================
# LISTA DE NOTAS
# ==============================

@login_required
def lista_notas(request):
    notas = NotaVenta.objects.select_related(
        "vendedor"
    ).prefetch_related(
        "detalles"
    ).order_by("-fecha")

    return render(request, 'pedidos/lista_notas.html', {
        'notas': notas
    })


# ==============================
# DETALLE DE NOTA
# ==============================
@login_required
def detalle_nota(request, nota_id):
    nota = get_object_or_404(NotaVenta, id=nota_id)
    detalles = nota.detalles.all()

    neto, iva, total = nota.calcular_totales()

    return render(request, 'pedidos/detalle_nota.html', {
        'nota': nota,
        'detalles': detalles,
        'neto': neto,
        'iva': iva,
        'total': total
    })