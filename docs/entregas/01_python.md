## Propuesta 3 · Asistente de movilidad cotidiana en Valencia

### 1. Título y descripción
Una aplicación para ayudar a residentes y turistas en Valencia a organizar sus desplazamientos y actividades según la meteorología y la información de movilidad disponible.
El usuario introduce lugares y horarios y consulta información relevante para decidir si mantener su planificación, revisar un horario o considerar otra opción de desplazamiento.

### 2. Problema y usuario
Residentes y turistas necesitan anticipar cómo la lluvia, el viento y la disponibilidad del transporte pueden afectar a sus desplazamientos y actividades.
Actualmente deben consultar distintas aplicaciones y páginas para conocer la previsión meteorológica, encontrar bicicletas disponibles y comprobar el tráfico. Después deben relacionar esa información con su planificación.
El producto busca reducir la incertidumbre, el tiempo dedicado a organizar los desplazamientos y los contratiempos evitables.

### 3. Uso y valor
**Ejemplo de una persona residente:** introduce los trayectos casa–trabajo–gimnasio y sus horarios. Consulta las condiciones meteorológicas previstas y las estaciones de Valenbisi próximas, con bicicletas y anclajes disponibles. Si se espera lluvia durante uno de los desplazamientos, puede valorar revisar su horario o planificación y además cambiar de medio de transporte.
**Ejemplo de una persona turista:** organiza una visita a la playa. Consulta la previsión de viento y lluvia para esa ubicación y horario, junto con las opciones de movilidad disponibles. Esta información le permite valorar cambiar la hora de la visita o elegir otra actividad.
El valor consiste en reunir información dispersa y relacionarla con los lugares, horarios y necesidades del usuario. Las recomendaciones no garantizarán la seguridad y tendrán en cuenta los avisos oficiales disponibles.

### 4. Datos y fuentes candidatas

| Fuente | Información necesaria | Estado del acceso |
|---|---|---|
| [AEMET OpenData](https://www.aemet.es/es/datos_abiertos/AEMET_OpenData) | Predicciones meteorológicas y avisos oficiales. | Servicio identificado; pendiente de validar los productos concretos y sus requisitos de acceso. |
| [Open-Meteo](https://open-meteo.com/en/docs) | Previsión por coordenadas: precipitación, viento y temperatura. | Alternativa candidata; se comprobó una consulta de datos históricos, pero falta validar las consultas previstas para el producto. |
| [Valenbisi — Datos abiertos del Ayuntamiento](https://opendata.vlci.valencia.es/dataset/valenbisi-disponibilitat-valenbisi-dsiponibilidad) | Ubicación de estaciones, bicicletas disponibles, anclajes libres y fecha de actualización. | Acceso JSON comprobado el 5 de noviembre de 2026. El portal declara actualización cada 10 minutos. |
| [Estado del tráfico de Valencia](https://opendata.vlci.valencia.es/dataset/estat-transit-temps-real-estado-trafico-tiempo-real) | Estado de circulación por tramos: fluido, denso, congestionado o cortado. | Fuente y recursos identificados; pendiente de probar su integración. El portal declara actualización cada 3 minutos. |

**Condiciones de uso y privacidad**
- Open-Meteo ofrece acceso gratuito para uso no comercial, sujeto a límites y condiciones.
- Se comprobarán las condiciones específicas de los productos seleccionados de AEMET.
- No se ha confirmado un histórico público de disponibilidad de Valenbisi; una función predictiva podría requerir recopilar observaciones.

### 5. Primera versión o MVP
El alcance definitivo se concretará después del feedback del profesor (y equipo) y de comprobar la viabilidad de las fuentes. Se consideran tres versiones alternativas o evolutivas:

| Versión | Funciones principales |
|---|---|
| **MVP 1 · Planificar un trayecto** | Introducir origen, destino y horario; consultar meteorología y estaciones cercanas con disponibilidad actual. |
| **MVP 2 · Anticipar disponibilidad** | Añadir una estimación de bicicletas y anclajes para la hora prevista del desplazamiento, condicionada a disponer de histórico suficiente. |
| **MVP 3 · Organizar el día** | Introducir varios lugares y horarios, visualizar los trayectos del día e identificar cuáles conviene revisar ante cambios meteorológicos. |

La preferencia inicial del equipo se centra en los MVP 1 y 3. La función predictiva propia se definirá durante la validación de los datos y del alcance académico.

**Fuera del alcance inicial:** integración con calendarios, reservas, cálculo de rutas optimizadas, predicción de accidentes e integración con metro u otros transportes cuyos datos no se hayan confirmado.

#### Bocetos de las tres versiones
<img width="1536" height="1024" alt="Movilidad cotidiana_ tres prototipos en Valencia" src="https://github.com/user-attachments/assets/f2e1ffd1-0a91-49a9-96cd-3c33eb33f203" />

*Prototipos conceptuales con datos ficticios. Ilustran posibles versiones del producto; no representan funciones ya implementadas ni un alcance definitivo.*

### 6. Viabilidad y dudas
La principal dificultad será integrar fuentes con diferentes frecuencias de actualización y convertir sus datos en información útil para el usuario.

Antes de confirmar el alcance, comprobaremos:
- Acceso, continuidad, cobertura y condiciones de reutilización de las fuentes.
- Calidad de los datos y detección de información desactualizada.
- Correspondencia entre ubicaciones, horarios y previsiones meteorológicas.
- Utilidad de las funciones para residentes y turistas.
- Disponibilidad de histórico si se incorpora una función predictiva.
- Funcionamiento del producto cuando una fuente no esté disponible.

El proyecto comenzará con un ámbito limitado a Valencia y un conjunto reducido de funciones, ampliable según los resultados y el feedback recibido.
