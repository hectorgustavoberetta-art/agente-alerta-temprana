# DECISIONES — Sistema Agéntico de Alerta Temprana

Este documento registra las principales decisiones, pruebas, errores y modificaciones realizadas durante la construcción del sistema.

## Iteración 1 — Definición del sistema

Se definió como caso real un Sistema Agéntico de Alerta Temprana y Situación Operacional.

El objetivo es recopilar, analizar, clasificar y sintetizar información pública reciente sobre UAS, FPV, ISR, UGV, drones logísticos, guerra de información, desinformación y tecnologías emergentes relacionadas.

Se decidió que el sistema no debe limitarse a responder preguntas como un chatbot. Debe utilizar herramientas reales para obtener información, procesarla mediante un agente y producir un informe estructurado sujeto a supervisión humana.

También se definieron los niveles de supervisión L0–L4 y se estableció que la aprobación y utilización final del informe corresponde a una persona.

## Iteración 2 — Primera herramienta: GDELT

La primera alternativa seleccionada para obtener información pública reciente fue la API de GDELT.

Se desarrolló la herramienta:

`herramientas/busqueda_gdelt.py`

Durante las pruebas reales, la consulta alcanzó correctamente el servicio externo, pero GDELT respondió reiteradamente:

`HTTP Error 429: Too Many Requests`

Se repitió la prueba y se obtuvo el mismo resultado.

### Decisión

No se eliminó la herramienta ni se ocultó la falla. Se decidió conservarla como evidencia de la primera iteración y buscar una alternativa que permitiera continuar el desarrollo con mayor disponibilidad.

## Iteración 3 — Búsqueda mediante RSS

Se desarrolló una segunda herramienta:

`herramientas/busqueda_rss.py`

La herramienta consulta noticias mediante RSS y recupera información estructurada de cada resultado:

- título;
- fuente;
- fecha;
- URL.

La primera prueba real recuperó 10 resultados recientes relacionados con la consulta de prueba sobre FPV drones y vehículos terrestres no tripulados.

La prueba también permitió detectar un nuevo problema: no todos los resultados recuperados eran relevantes para el objetivo del sistema. Aparecieron noticias militares pertinentes junto con resultados comerciales o de entretenimiento relacionados con la misma terminología.

### Decisión

La búsqueda RSS se adopta como fuente funcional inicial.

La siguiente iteración deberá incorporar al agente para que analice los resultados recuperados, descarte información irrelevante, clasifique los hechos y genere el informe estructurado.

## Estado actual

El sistema dispone de:

- contrato inicial mediante `system_prompt.md` y `user_prompt.md`;
- definición de supervisión humana L0–L4;
- una primera herramienta GDELT conservada como iteración fallida;
- una herramienta RSS probada con información real;
- una fuente real de datos sobre la cual construir el análisis agéntico.

El siguiente objetivo es conectar la herramienta RSS con el modelo para transformar los resultados de búsqueda en un producto de alerta temprana estructurado.