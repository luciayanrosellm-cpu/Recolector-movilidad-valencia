# Recolector de datos de movilidad de Valencia

Guarda cada 10 minutos una "foto" de las fuentes abiertas de movilidad de Valencia para construir el histórico que necesita el proyecto (las fuentes en tiempo real no guardan su pasado).

## Qué se recoge

| Carpeta en `data/raw/` | Qué contiene | Frecuencia | Fuente y licencia |
|---|---|---|---|
| `valenbisi/` | Bicis y anclajes libres por estación, con coordenadas | Cada ejecución | Ajuntament de València · CC BY 4.0 |
| `trafico/` | Estado de cada tramo (0 fluido, 1 denso, 2 congestionado, 3 cortado…) | Cada ejecución | Ajuntament de València · CC BY 4.0 |
| `meteo_actual/` | Temperatura, lluvia, viento y rachas en Valencia | Cada ejecución | Open-Meteo |
| `meteo_prevision/` | Previsión horaria de las próximas 48 h | Una vez por hora | Open-Meteo |
| `renfe_avisos/` | Avisos de Cercanías que afectan a la zona de Valencia | Cada ejecución | Renfe (GTFS-Realtime) |
| `renfe_retrasos/` | Retraso y cancelación de cada tren de Cercanías Valencia | Cada ejecución | Renfe (GTFS-Realtime) |
| `gtfs/emt/`, `gtfs/renfe/`, `gtfs/metrovalencia/` | Horarios oficiales completos (zip GTFS) | Solo cuando cambian | EMT (CC BY 4.0), Renfe, FGV vía NAP |

Cada ejecución crea archivos nuevos (`AAAA/MM/DD/HHMM.csv.gz`) y no reescribe los anteriores. La columna `captura` indica el momento de la foto, en hora de Madrid.

**Metro y autobús EMT:** no publican tiempo real como datos abiertos, así que de ellos se guardan los horarios. No se usan APIs no oficiales de sus apps.

**Pendiente de confirmar:** las condiciones de reutilización de Renfe, Open-Meteo y el NAP, y la dirección de retrasos de Renfe (`trip_updates.pb`). Documentadlo en la actividad 1.

## Ponerlo en marcha con GitHub Actions (sin tener el ordenador encendido)

1. Crea un repositorio **aparte** para el recolector, por ejemplo `recolector-movilidad-valencia`, y sube el contenido de esta carpeta (incluida la carpeta oculta `.github`).
   - Recomendación: hazlo **público**. Los datos son abiertos y no hay secretos en el código, y en repositorios públicos GitHub Actions es gratis sin límite. En uno privado, ejecutar cada 10 minutos supera los minutos gratuitos al mes.
   - El repositorio del proyecto sigue siendo privado y enlaza a este desde `data/README.md`.
2. En el repositorio, ve a **Settings > Actions > General > Workflow permissions** y marca **Read and write permissions**. Así el robot puede guardar los datos.
3. Ve a la pestaña **Actions**, elige "Recoger datos de movilidad" y pulsa **Run workflow** para probarlo. Si sale en verde, aparecerá la carpeta `data/raw` con los primeros archivos.
4. A partir de ahí se ejecuta solo cada 10 minutos. GitHub a veces lo retrasa unos minutos: no pasa nada, cada archivo lleva su hora real.
5. Opcional, para el horario de Metrovalencia: regístrate gratis en nap.transportes.gob.es, copia tu clave y guárdala en **Settings > Secrets and variables > Actions > New repository secret** con el nombre `NAP_API_KEY`. Nunca la escribas en el código.

Revisad una vez por semana la pestaña Actions: si una fuente cambia de formato o de dirección, la ejecución lo indica en el registro y el resto de fuentes siguen guardándose.

## Ejecutarlo en tu ordenador

```bash
pip install -r requirements.txt
python recolector.py                          # todas las fuentes
python recolector.py --fuentes valenbisi meteo  # solo algunas
```

## Leer los datos acumulados

```python
import glob
import pandas as pd

archivos = sorted(glob.glob("data/raw/valenbisi/**/*.csv.gz", recursive=True))
valenbisi = pd.concat(map(pd.read_csv, archivos), ignore_index=True)
```

## Atribución

Datos de Valenbisi y del estado del tráfico: Ajuntament de València, portal de datos abiertos (opendata.vlci.valencia.es), licencia CC BY 4.0. Horarios de EMT València: Ajuntament de València, CC BY 4.0. Tiempo: Open-Meteo.com. Cercanías: Renfe. Metrovalencia: FGV a través del Punto de Acceso Nacional de Transporte Multimodal.
