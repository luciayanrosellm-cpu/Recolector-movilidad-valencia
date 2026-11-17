import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from utils import descargar, guardar

URL_METEO = (
    "https://api.open-meteo.com/v1/forecast?latitude=39.4699&longitude=-0.3763&timezone=Europe%2FMadrid&forecast_days=2"
    "&current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m,wind_gusts_10m"
    "&hourly=temperature_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m,wind_gusts_10m"
)


def meteo(raiz: Path, ahora: datetime) -> None:
    datos = json.loads(descargar(URL_METEO))
    actual = pd.DataFrame([datos["current"]])
    actual.insert(0, "captura", ahora.isoformat())
    guardar(actual, raiz, "meteo_actual", ahora)
    # La previsión se guarda una vez por hora: permite medir después cómo de buena era.
    if ahora.minute < 10:
        prevision = pd.DataFrame(datos["hourly"])
        prevision.insert(0, "captura", ahora.isoformat())
        guardar(prevision, raiz, "meteo_prevision", ahora)
