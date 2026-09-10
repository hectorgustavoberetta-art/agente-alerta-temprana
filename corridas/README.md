# Corridas del sistema

Este directorio conserva las ejecuciones reales realizadas durante el desarrollo, calibración y validación final del Sistema Agéntico de Alerta Temprana.

Se mantuvieron las corridas tal como fueron generadas para asegurar trazabilidad, reproducibilidad y documentación del proceso de construcción del sistema.

## Clasificación de las corridas

### Corridas de desarrollo inicial

- `corrida_01.md`: primera ejecución real del sistema.
- `corrida_02.md`: segunda ejecución, con mejora en la preservación de fuentes.
- `corrida_03.md`: tercera ejecución sobre drones logísticos y sistemas autónomos.
- `corrida_04.md`: primera ejecución completa desde la interfaz Streamlit.

Estas corridas documentan la evolución inicial del sistema y se conservaron como evidencia del proceso.

### Comparación y selección de modelo

- `corrida_05.md`: ejecución utilizada para validar el desempeño de `gpt-5.6-luna` y compararlo con ejecuciones previas realizadas con `gpt-5.6-sol`.

A partir de esta prueba se seleccionó `gpt-5.6-luna` como modelo final por mantener una calidad suficiente para la tarea con un costo significativamente menor.

### Corridas finales de validación

- `corrida_06.md`
- `corrida_07.md`
- `corrida_08.md`
- `corrida_09.md`

Estas ejecuciones corresponden a la versión final del sistema, con:

- prompts integrados al flujo real de ejecución;
- herramienta RSS activa;
- modelo `gpt-5.6-luna`;
- registro de fuentes recuperadas;
- medición de tokens;
- salida estructurada;
- interfaz Streamlit;
- supervisión humana definida.

Las corridas finales se utilizaron también para verificar la correcta visualización de los resultados en la interfaz.

## Contenido registrado

Cada corrida conserva, según la versión correspondiente:

- fecha de ejecución;
- modelo utilizado;
- consulta realizada;
- áreas seleccionadas;
- período analizado;
- nivel mínimo de relevancia;
- cantidad de fuentes recuperadas;
- fuentes utilizadas;
- tokens de entrada;
- tokens de salida;
- tokens totales;
- salida generada por el agente.

## Nota sobre reproducibilidad

Las primeras corridas se preservaron sin modificarlas retroactivamente, incluso cuando posteriormente se mejoró el registro de fuentes y parámetros.

Esta decisión permite mostrar de manera transparente la evolución real del sistema.

Para reconstruir y evaluar la versión final se recomienda utilizar principalmente las corridas `06`, `07`, `08` y `09`, junto con los archivos:

- `prompts/system_prompt.md`
- `prompts/user_prompt.md`
- `agente/analizador.py`
- `herramientas/busqueda_rss.py`
- `app.py`