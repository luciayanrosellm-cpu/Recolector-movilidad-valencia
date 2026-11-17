import io
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd

from utils import descargar, guardar, ultimo_gtfs

URL_RENFE_AVISOS = "https://gtfsrt.renfe.com/alerts.pb"
URL_RENFE_RETRASOS = "https://gtfsrt.renfe.com/trip_updates.pb"

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

LAT_MIN, LAT_MAX, LON_MIN, LON_MAX = 38.80, 40.05, -1.35, 0.10


def _leer_txt(zip_gtfs: zipfile.ZipFile, nombre: str) -> pd.DataFrame:
    datos = zip_gtfs.read(nombre)
    for codificacion in ("utf-8-sig", "latin-1"):
        try:
            tabla = pd.read_csv(io.BytesIO(datos), dtype=str, encoding=codificacion)
            tabla.columns = tabla.columns.str.strip()
            return tabla.apply(lambda c: c.str.strip())
        except UnicodeDecodeError:
            continue
    raise ValueError(f"No se pudo leer {nombre}")


def _filtro_renfe_valencia(zip_bytes: bytes) -> tuple[set, set, dict]:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        paradas = _leer_txt(z, "stops.txt")
        paradas[["stop_lat", "stop_lon"]] = paradas[["stop_lat", "stop_lon"]].astype(
            float
        )
        en_zona = paradas[
            paradas.stop_lat.between(LAT_MIN, LAT_MAX)
            & paradas.stop_lon.between(LON_MIN, LON_MAX)
        ]
        horarios = _leer_txt(z, "stop_times.txt")[["trip_id", "stop_id"]]
        viajes_zona = set(
            horarios.loc[horarios.stop_id.isin(en_zona.stop_id), "trip_id"]
        )
        viajes = _leer_txt(z, "trips.txt")[["trip_id", "route_id"]]
        linea_de_viaje = dict(viajes.loc[viajes.trip_id.isin(viajes_zona)].values)
    return set(en_zona.stop_id), set(linea_de_viaje.values()), linea_de_viaje


def renfe(raiz: Path, ahora: datetime) -> None:
    from google.transit import gtfs_realtime_pb2  # pip install gtfs-realtime-bindings

    zip_local = ultimo_gtfs(raiz, "renfe")
    if zip_local:
        zip_bytes = zip_local.read_bytes()
    else:  # primera ejecución: se descarga el horario y se guarda para las siguientes
        zip_bytes = descargar(GTFS["renfe"][0], timeout=180)
        destino = raiz / "gtfs" / "renfe" / f"{ahora:%Y-%m-%d}.zip"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(zip_bytes)
    paradas, lineas, linea_de_viaje = _filtro_renfe_valencia(zip_bytes)

    def leer(url: str):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(descargar(url))
        return feed

    texto = lambda t: t.translation[0].text if t.translation else ""
    avisos = []
    for e in leer(URL_RENFE_AVISOS).entity:
        afectados = e.alert.informed_entity
        if any(
            a.route_id in lineas
            or a.stop_id in paradas
            or a.trip.trip_id in linea_de_viaje
            for a in afectados
        ):
            avisos.append(
                {
                    "captura": ahora.isoformat(),
                    "aviso_id": e.id,
                    "titulo": texto(e.alert.header_text),
                    "descripcion": texto(e.alert.description_text),
                    "causa": e.alert.cause,
                    "efecto": e.alert.effect,
                    "lineas": "|".join(
                        sorted({a.route_id for a in afectados if a.route_id})
                    ),
                    "paradas": "|".join(
                        sorted({a.stop_id for a in afectados if a.stop_id})
                    ),
                }
            )
    guardar(
        pd.DataFrame(
            avisos,
            columns=[
                "captura",
                "aviso_id",
                "titulo",
                "descripcion",
                "causa",
                "efecto",
                "lineas",
                "paradas",
            ],
        ),
        raiz,
        "renfe_avisos",
        ahora,
    )

    retrasos = []
    for e in leer(URL_RENFE_RETRASOS).entity:
        tu = e.trip_update
        if tu.trip.trip_id not in linea_de_viaje:
            continue
        siguiente = tu.stop_time_update[0] if len(tu.stop_time_update) else None
        retraso = (
            tu.delay
            or (siguiente and (siguiente.arrival.delay or siguiente.departure.delay))
            or 0
        )
        retrasos.append(
            {
                "captura": ahora.isoformat(),
                "trip_id": tu.trip.trip_id,
                "route_id": linea_de_viaje[tu.trip.trip_id],
                "retraso_s": int(retraso),
                "proxima_parada": siguiente.stop_id if siguiente else "",
                "cancelado": int(tu.trip.schedule_relationship == 3),
            }
        )
    guardar(
        pd.DataFrame(
            retrasos,
            columns=[
                "captura",
                "trip_id",
                "route_id",
                "retraso_s",
                "proxima_parada",
                "cancelado",
            ],
        ),
        raiz,
        "renfe_retrasos",
        ahora,
    )
