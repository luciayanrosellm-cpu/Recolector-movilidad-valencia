import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

from logs import log

CABECERAS = {"User-Agent": "recolector-movilidad-valencia (proyecto academico)"}


def geojson_a_tabla(contenido: bytes, con_coordenadas: bool) -> pd.DataFrame:
    filas = []
    for entidad in json.loads(contenido).get("features", []):
        fila = dict(entidad.get("properties") or {})
        geometria = entidad.get("geometry") or {}
        if con_coordenadas and geometria.get("type") == "Point":
            fila["lon"], fila["lat"] = geometria["coordinates"][:2]
        filas.append(fila)
    return pd.DataFrame(filas)


def descargar(url: str, cabeceras: dict | None = None, timeout: int = 60) -> bytes:
    respuesta = requests.get(
        url, headers={**CABECERAS, **(cabeceras or {})}, timeout=timeout
    )
    respuesta.raise_for_status()
    return respuesta.content


def guardar(tabla: pd.DataFrame, raiz: Path, fuente: str, ahora: datetime) -> Path:
    destino = raiz / fuente / ahora.strftime("%Y/%m/%d") / f"{ahora:%H%M}.csv.gz"
    destino.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(destino, index=False, compression="gzip")
    log.info("%s: %d filas -> %s", fuente, len(tabla), destino)
    return destino


def ultimo_gtfs(raiz: Path, operador: str) -> Path | None:
    archivos = sorted((raiz / "gtfs" / operador).glob("*.zip"))
    return archivos[-1] if archivos else None
