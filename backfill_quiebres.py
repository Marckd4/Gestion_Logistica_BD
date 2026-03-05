#!/usr/bin/env python
"""
Script para regenerar quiebres de stock faltantes en notas ya despachadas.
Usa la nueva lógica de stock virtual acumulado.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'productly.settings')
django.setup()

from pedidos.models import NotaVenta, QuiebresStock, DetalleNota
from pedidos.views import _construir_plan_picking
from django.db import transaction

def regenerar_quiebres_nota(nota_id):
    """Regenera quiebres para una nota específica"""
    try:
        nota = NotaVenta.objects.get(id=nota_id)
    except NotaVenta.DoesNotExist:
        print(f"❌ Nota {nota_id} no existe")
        return False
    
    if nota.estado != 'despachada':
        print(f"⚠️  Nota {nota_id} no está despachada. Estado: {nota.estado}")
        return False
    
    # Obtener quiebres actuales
    quiebres_actuales = QuiebresStock.objects.filter(nota=nota).values_list('detalle_id', flat=True)
    detalles = nota.detalles.all()
    detalles_sin_quiebre = detalles.exclude(id__in=quiebres_actuales)
    
    if not detalles_sin_quiebre.exists():
        print(f"✅ Nota {nota_id}: Todos los detalles con quiebre ya están registrados")
        return True
    
    print(f"\n📝 Procesando nota {nota_id}...")
    print(f"   Detalles totales: {detalles.count()}")
    print(f"   Quiebres existentes: {quiebres_actuales.count()}")
    print(f"   Detalles sin quiebre: {detalles_sin_quiebre.count()}")
    
    # Recalcular plan con nueva lógica
    plan, _ = _construir_plan_picking(nota, bloquear=False)
    
    quiebres_creados = 0
    with transaction.atomic():
        for detalle_plan in plan:
            detalle = detalle_plan['detalle']
            faltante = detalle_plan['faltante']
            
            # Verificar si ya existe quiebre para este detalle
            quiebre_existe = QuiebresStock.objects.filter(
                nota=nota,
                detalle=detalle
            ).exists()
            
            if quiebre_existe:
                continue
            
            # Si hay faltante y no existe registro, crearlo
            if faltante > 0:
                cantidad_requerida = detalle_plan['cantidad_requerida']
                cantidad_entregada = cantidad_requerida - faltante
                
                quiebre = QuiebresStock.objects.create(
                    nota=nota,
                    detalle=detalle,
                    codigo=detalle.codigo or '',
                    descripcion=detalle.descripcion,
                    cantidad_solicitada=cantidad_requerida,
                    cantidad_entregada=cantidad_entregada,
                    cantidad_faltante=faltante
                )
                quiebres_creados += 1
                print(f"   ✓ Creado quiebre: {detalle.codigo} ({faltante} cajas faltantes)")
    
    if quiebres_creados > 0:
        print(f"   ✅ {quiebres_creados} quiebre(s) registrado(s)")
    
    return True


def backfill_all():
    """Regenera quiebres para TODAS las notas despachadas"""
    notas_despachadas = NotaVenta.objects.filter(estado='despachada').order_by('id')
    
    print("=" * 60)
    print("🔧 BACKFILL DE QUIEBRES DE STOCK")
    print("=" * 60)
    print(f"Total de notas despachadas: {notas_despachadas.count()}\n")
    
    total_creados = 0
    exitosas = 0
    
    for nota in notas_despachadas:
        if regenerar_quiebres_nota(nota.id):
            exitosas += 1
            quiebres = QuiebresStock.objects.filter(nota=nota).count()
            detalles = nota.detalles.count()
            if quiebres > 0:
                total_creados += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN:")
    print(f"   Notas procesadas: {exitosas}/{notas_despachadas.count()}")
    print(f"   Notas con quiebres detectados: {total_creados}")
    print("=" * 60)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Procesar nota específica
        nota_id = int(sys.argv[1])
        regenerar_quiebres_nota(nota_id)
    else:
        # Procesar todas
        backfill_all()
