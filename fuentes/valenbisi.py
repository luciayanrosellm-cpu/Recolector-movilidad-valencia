from datetime import datetime
from pathlib import Path

from utils import descargar, geojson_a_tabla, guardar

URL_VALENBISI = "https://geoportal.valencia.es/server/rest/services/OPENDATA/Trafico/MapServer/228/query?where=1=1&outFields=*&f=geojson"


def valenbisi(raiz: Path, ahora: datetime) -> None:
    tabla = geojson_a_tabla(descargar(URL_VALENBISI), con_coordenadas=True)
    if tabla.empty:
        raise ValueError("Valenbisi ha devuelto 0 estaciones")
    tabla.insert(0, "captura", ahora.isoformat())
    guardar(tabla, raiz, "valenbisi", ahora)
