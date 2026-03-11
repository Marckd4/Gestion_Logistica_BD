import pandas as pd
from django.db.models import F

from bodegacentral.models import Central
from bodegabsf.models import Bsf


def rebaje_masivo_excel(archivo, bodega):

    df = pd.read_excel(archivo)

    # seleccionar modelo según bodega
    modelo = Central if bodega == "central" else Bsf

    for _, row in df.iterrows():

        cod_dun = str(row["cod_dun"])
        ubicacion = row["ubicacion"]
        cajas = int(row["cajas"])

        modelo.objects.filter(
            cod_dun=cod_dun,
            ubicacion=ubicacion
        ).update(
            cajas=F("cajas") - cajas
        )