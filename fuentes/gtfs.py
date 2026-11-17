import hashlib
import io
import os
import zipfile
from datetime import datetime
from pathlib import Path

from logs import log
from utils import descargar, ultimo_gtfs

GTFS = {
    "emt": (
        "https://opendata.vlci.valencia.es/dataset/ab058cf8-ad3e-4d9c-ac89-0c6367ecf351/resource/"
        "c81b69e6-c082-44dc-acc6-66fc417b4e66/download/google_transit.zip",
        None,
    ),
    "renfe": (
        "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip",
        None,
    ),
    "metrovalencia": (
        "https://nap.transportes.gob.es/api/Fichero/download/1168",
        "NAP_API_KEY",
    ),
}


def gtfs(raiz: Path, ahora: datetime) -> None:
    """Guarda los horarios de cada operador solo cuando cambian (se comparan por huella SHA-256)."""
    for operador, (url, variable_clave) in GTFS.items():
        cabeceras = {}
        if variable_clave:
            clave = os.environ.get(variable_clave)
            if not clave:
                log.info("gtfs %s: omitido (falta %s)", operador, variable_clave)
                continue
            cabeceras = {"ApiKey": clave}
        try:
            contenido = descargar(url, cabeceras, timeout=180)
            zipfile.ZipFile(io.BytesIO(contenido)).testzip()
        except Exception as error:  # noqa: BLE001 - se registra y se sigue con el resto
            log.warning("gtfs %s: error %s", operador, error)
            continue
        huella = hashlib.sha256(contenido).hexdigest()
        anterior = ultimo_gtfs(raiz, operador)
        if anterior and hashlib.sha256(anterior.read_bytes()).hexdigest() == huella:
            log.info("gtfs %s: sin cambios", operador)
            continue
        destino = raiz / "gtfs" / operador / f"{ahora:%Y-%m-%d}.zip"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(contenido)
        log.info("gtfs %s: nueva versión -> %s", operador, destino)
