from datetime import datetime
from pathlib import Path

from utils import descargar, geojson_a_tabla, guardar

URL_TRAFICO = "https://geoportal.valencia.es/server/rest/services/OPENDATA/Trafico/MapServer/192/query?where=1=1&outFields=*&f=geojson"


def trafico(raiz: Path, ahora: datetime) -> None:
    # Solo atributos (tramo y estado). La geometría de los tramos no cambia: se guarda aparte una vez.
    contenido = descargar(URL_TRAFICO)
    tabla = geojson_a_tabla(contenido, con_coordenadas=False)
    if tabla.empty:
        raise ValueError("Tráfico ha devuelto 0 tramos")
    tabla.insert(0, "captura", ahora.isoformat())
    guardar(tabla, raiz, "trafico", ahora)
    geometria = raiz / "trafico" / "tramos_geometria.geojson"
    if not geometria.exists():
        geometria.write_bytes(contenido)
