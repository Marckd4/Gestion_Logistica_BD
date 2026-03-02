from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.db.models.functions import Replace, Upper
from django.db.models import Value
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from decimal import Decimal, ROUND_HALF_UP
from decimal import InvalidOperation

from .forms import NotaVentaForm, DetalleNotaFormSet
from .models import NotaVenta, DetalleNota
from bodegabsf.models import Bsf
from bodegacentral.models import Central


@login_required
def inicio_pedidos(request):
    return redirect('crear_nota')


def _normalizar_rut(rut):
    if not rut:
        return ""
    return rut.replace(".", "").replace("-", "").strip().upper()


def _json_no_cache(payload):
    response = JsonResponse(payload)
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


@login_required
@require_GET
def buscar_cliente_por_rut(request):
    rut = request.GET.get("rut", "")
    nombre = request.GET.get("nombre", "").strip()
    rut_normalizado = _normalizar_rut(rut)

    if not rut_normalizado and not nombre:
        return _json_no_cache({"found": False})

    notas = NotaVenta.objects.all()

    if rut_normalizado:
        notas = notas.exclude(rut_cliente__isnull=True).exclude(rut_cliente="").annotate(
            rut_normalizado=Upper(
                Replace(
                    Replace("rut_cliente", Value("."), Value("")),
                    Value("-"),
                    Value(""),
                )
            )
        ).filter(rut_normalizado=rut_normalizado)

    if nombre:
        notas = notas.exclude(cliente__isnull=True).exclude(cliente="").filter(
            Q(cliente__iexact=nombre) | Q(cliente__icontains=nombre)
        )

    nota = notas.order_by("-fecha").first()

    if not nota:
        return _json_no_cache({"found": False})

    return _json_no_cache(
        {
            "found": True,
            "cliente": {
                "cliente": nota.cliente or "",
                "rut_cliente": nota.rut_cliente or "",
                "giro": nota.giro or "",
                "telefono": nota.telefono or "",
                "direccion": nota.direccion or "",
                "comuna": nota.comuna or "",
                "ciudad": nota.ciudad or "",
                "lugar_de_entrega": nota.lugar_de_entrega or "",
                "persona_responsable": nota.persona_responsable or "",
            },
        }
    )


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
            messages.success(request, "Nota creada correctamente.")
            return redirect('ingresar_producto', nota_id=nota.id)
    else:
        form = NotaVentaForm()

    return render(request, 'pedidos/crear_nota.html', {'form': form})


@login_required
def ingresar_producto(request, nota_id):
    nota = get_object_or_404(NotaVenta, id=nota_id)
    detalles = nota.detalles.all().order_by('id')
    return render(
        request,
        'pedidos/ingresar_producto.html',
        {
            'nota': nota,
            'detalles': detalles,
            'next_correlativo': detalles.count() + 1,
        }
    )


@login_required
@require_POST
def agregar_detalle_nota(request, nota_id):
    nota = get_object_or_404(NotaVenta, id=nota_id)

    codigo = request.POST.get('cod_sistema', '').strip()
    descripcion_form = request.POST.get('descripcion', '').strip()
    cantidad_raw = request.POST.get('cantidad', '').strip()
    valor_raw = request.POST.get('valor', '').strip()

    if not codigo:
        return _json_no_cache({'ok': False, 'message': 'Código de sistema requerido.'})

    try:
        cantidad = int(cantidad_raw)
        if cantidad <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return _json_no_cache({'ok': False, 'message': 'Cantidad inválida.'})

    try:
        valor = Decimal(valor_raw)
        if valor < 0:
            raise InvalidOperation
    except (TypeError, InvalidOperation, ValueError):
        return _json_no_cache({'ok': False, 'message': 'Valor inválido.'})

    producto_bsf = Bsf.objects.filter(cod_sistema__iexact=codigo).first()
    producto_central = Central.objects.filter(cod_sistema__iexact=codigo).first()
    producto = producto_bsf or producto_central

    descripcion = descripcion_form
    ean = ''
    dun = ''
    formato_venta = ''
    capacidad_x_caja = None

    if producto:
        descripcion = producto.descripcion or descripcion_form
        ean = producto.cod_ean or ''
        dun = producto.cod_dun or ''
        formato_venta = producto.unidad or ''
        capacidad_x_caja = producto.pack if producto.pack else None

    if not descripcion:
        return _json_no_cache({'ok': False, 'message': 'Descripción requerida.'})

    detalle = DetalleNota.objects.create(
        nota=nota,
        codigo=codigo,
        descripcion=descripcion,
        ean=ean,
        dun=dun,
        formato_venta=formato_venta,
        cantidad_solicitada=cantidad,
        capacidad_x_caja=capacidad_x_caja,
        precio_x_caja=valor,
        precio_unitario=valor,
    )

    return _json_no_cache(
        {
            'ok': True,
            'message': 'Producto guardado correctamente.',
            'detalle': {
                'codigo': detalle.codigo or '',
                'descripcion': detalle.descripcion or '',
                'cantidad': detalle.cantidad_solicitada,
                'valor': str(detalle.precio_unitario),
            },
        }
    )


@login_required
@require_POST
def terminar_pedido(request, nota_id):
    nota = get_object_or_404(NotaVenta, id=nota_id)
    nota.estado = 'finalizada'
    nota.save(update_fields=['estado'])
    messages.success(request, f"Pedido de la Nota #{nota.id} finalizado correctamente.")
    return redirect('status_pedido')


@login_required
def status_pedido(request):
    notas = NotaVenta.objects.select_related('vendedor').order_by('-fecha')
    return render(request, 'pedidos/status_pedido.html', {'notas': notas})


@login_required
def editar_nota(request, nota_id):
    nota = get_object_or_404(NotaVenta, id=nota_id)

    if request.method == 'POST':
        form = NotaVentaForm(request.POST, instance=nota)
        formset = DetalleNotaFormSet(request.POST, instance=nota, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            nota_actualizada = form.save()
            detalles = formset.save(commit=False)

            for detalle_eliminado in formset.deleted_objects:
                detalle_eliminado.delete()

            for detalle in detalles:
                if detalle.precio_unitario and (not detalle.precio_x_caja or detalle.precio_x_caja != detalle.precio_unitario):
                    detalle.precio_x_caja = detalle.precio_unitario
                detalle.nota = nota_actualizada
                detalle.save()

            nota_actualizada.calcular_totales()
            messages.success(request, f"Nota #{nota_actualizada.id} actualizada correctamente.")
            return redirect('status_pedido')
    else:
        form = NotaVentaForm(instance=nota)
        formset = DetalleNotaFormSet(instance=nota, prefix='detalles')

    return render(
        request,
        'pedidos/editar_nota.html',
        {
            'nota': nota,
            'form': form,
            'formset': formset,
        }
    )


@login_required
def ver_nota_venta(request, nota_id):
    nota = get_object_or_404(
        NotaVenta.objects.select_related('vendedor').prefetch_related('detalles'),
        id=nota_id
    )

    detalles = nota.detalles.all().order_by('id')

    for detalle in detalles:
        total_linea = (Decimal(detalle.cantidad_solicitada) * detalle.precio_unitario).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        if detalle.importe_a_facturar != total_linea:
            detalle.importe_a_facturar = total_linea
            detalle.save(update_fields=['importe_a_facturar'])

    neto_calculado = sum(
        (Decimal(d.cantidad_solicitada) * d.precio_unitario for d in detalles),
        Decimal("0.00")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    iva_calculado = (neto_calculado * nota.IVA_PORCENTAJE).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    total_general = (neto_calculado + iva_calculado).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    if nota.neto != neto_calculado or nota.iva != iva_calculado or nota.total != total_general:
        nota.neto = neto_calculado
        nota.iva = iva_calculado
        nota.total = total_general
        nota.save(update_fields=['neto', 'iva', 'total'])

    return render(
        request,
        'pedidos/ver_nota_venta.html',
        {
            'nota': nota,
            'detalles': detalles,
            'total_general': total_general,
        }
    )


@login_required
@require_GET
def buscar_producto_por_codigo(request):
    codigo = request.GET.get("cod_sistema", "").strip()

    if not codigo:
        return _json_no_cache(
            {
                "found": False,
                "producto": {},
                "stocks": {
                    "bsf": 0,
                    "central": 0,
                    "total": 0,
                },
            }
        )

    bsf_base = Bsf.objects.exclude(cod_sistema__isnull=True).exclude(cod_sistema="")
    central_base = Central.objects.exclude(cod_sistema__isnull=True).exclude(cod_sistema="")

    bsf_exact = bsf_base.filter(cod_sistema__iexact=codigo)
    central_exact = central_base.filter(cod_sistema__iexact=codigo)

    bsf_qs = bsf_exact if bsf_exact.exists() else bsf_base.filter(cod_sistema__icontains=codigo)
    central_qs = central_exact if central_exact.exists() else central_base.filter(cod_sistema__icontains=codigo)

    stock_bsf = bsf_qs.aggregate(total=Coalesce(Sum("cajas"), 0))["total"] or 0
    stock_central = central_qs.aggregate(total=Coalesce(Sum("cajas"), 0))["total"] or 0
    stock_total = stock_bsf + stock_central

    producto = bsf_qs.first() or central_qs.first()

    if not producto:
        return _json_no_cache(
            {
                "found": False,
                "producto": {},
                "stocks": {
                    "bsf": 0,
                    "central": 0,
                    "total": 0,
                },
            }
        )

    return _json_no_cache(
        {
            "found": True,
            "producto": {
                "cod_sistema": producto.cod_sistema or "",
                "descripcion": producto.descripcion or "",
                "cod_ean": producto.cod_ean or "",
                "cod_dun": producto.cod_dun or "",
            },
            "stocks": {
                "bsf": stock_bsf,
                "central": stock_central,
                "total": stock_total,
            },
        }
    )
