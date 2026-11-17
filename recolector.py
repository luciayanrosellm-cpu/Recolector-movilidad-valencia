"""
Recolector de datos de movilidad de Valencia.

Cada ejecución guarda una "foto" del momento de cada fuente en
data/raw/<fuente>/AAAA/MM/DD/HHMM.csv.gz (un archivo por ejecución, sin reescribir los anteriores).
Pensado para ejecutarse cada 10 minutos (por ejemplo con GitHub Actions) y acumular histórico.

Fuentes:
  valenbisi  Disponibilidad de Valenbisi (Ajuntament de València, CC BY 4.0). Se actualiza cada 10 min.
  trafico    Estado del tráfico por tramo (Ajuntament de València, CC BY 4.0). Se actualiza cada 3 min.
  meteo      Tiempo actual y previsión horaria en Valencia (Open-Meteo, sin clave).
  renfe      Avisos y retrasos en tiempo real de Cercanías, filtrados a la zona de Valencia (Renfe).
  gtfs       Horarios oficiales (EMT, Renfe y, con clave del NAP, Metrovalencia). Solo se guardan si cambian.

Metro y autobús EMT no publican tiempo real como datos abiertos: de ellos se guardan los horarios (GTFS).
No se usan APIs no oficiales de las apps.

Uso:
  python recolector.py                    # todas las fuentes
  python recolector.py --fuentes valenbisi meteo
Variables de entorno opcionales:
  NAP_API_KEY   clave gratuita del Punto de Acceso Nacional (nap.transportes.gob.es) para el GTFS de Metrovalencia
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fuentes.gtfs import gtfs
from fuentes.meteo import meteo
from fuentes.renfe import renfe
from fuentes.trafico import trafico
from fuentes.valenbisi import valenbisi
from logs import log

ZONA = ZoneInfo("Europe/Madrid")
CABECERAS = {"User-Agent": "recolector-movilidad-valencia (proyecto academico)"}


FUENTES = {
    "valenbisi": valenbisi,
    "trafico": trafico,
    "meteo": meteo,
    "gtfs": gtfs,
    "renfe": renfe,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guarda una foto de las fuentes de movilidad de Valencia"
    )
    parser.add_argument(
        "--salida", default="data/raw", help="Carpeta raíz de los datos"
    )
    parser.add_argument(
        "--fuentes", nargs="+", choices=list(FUENTES), default=list(FUENTES)
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    ahora = datetime.now(ZONA).replace(second=0, microsecond=0)
    raiz = Path(args.salida)
    fallos = []
    for (
        nombre
    ) in args.fuentes:  # gtfs va antes que renfe: renfe usa el último horario guardado
        try:
            FUENTES[nombre](raiz, ahora)
        except (
            Exception
        ) as error:  # noqa: BLE001 - un fallo en una fuente no detiene las demás
            log.error("%s: %s", nombre, error)
            fallos.append(nombre)
    if fallos:
        log.warning("Fuentes con error: %s", ", ".join(fallos))
    return 1 if len(fallos) == len(args.fuentes) else 0


if __name__ == "__main__":
    sys.exit(main())
