# Gobierno, riesgos y supervisión humana

## Objetivo

Este documento describe los sistemas con los que interactúa el agente, los permisos utilizados, los principales riesgos operativos y de información, las medidas de control y el nivel de supervisión humana requerido.

## Sistemas utilizados

### 1. Google News RSS

El agente consulta información pública mediante Google News RSS.

Permisos utilizados:

- acceso de lectura a información pública;
- no requiere autenticación;
- no modifica contenidos;
- no realiza operaciones de escritura sobre sistemas externos.

Información recuperada:

- título;
- medio o fuente;
- fecha;
- enlace de la publicación.

En la versión actual no se descarga ni analiza automáticamente el contenido completo de los artículos.

### 2. OpenAI API

El sistema utiliza la API de OpenAI para clasificar, filtrar, sintetizar y analizar las fuentes recuperadas.

La API recibe:

- los prompts del sistema;
- los parámetros definidos por el usuario;
- títulos de las noticias;
- fuente;
- fecha;
- URL;
- instrucciones para generar el informe.

El sistema no necesita enviar información clasificada, datos personales ni documentación interna para cumplir su función actual.

La clave de API se administra mediante la variable de entorno `OPENAI_API_KEY`.

La clave no se encuentra escrita dentro del código ni almacenada en el repositorio público.

### 3. Sistema de archivos

El agente genera archivos de evidencia en la carpeta `corridas/`.

Cada corrida registra, según la versión correspondiente:

- fecha de ejecución;
- modelo utilizado;
- consulta;
- áreas de interés;
- período;
- relevancia;
- fuentes recuperadas;
- consumo de tokens;
- salida producida por el agente.

Estos archivos permiten auditar y reconstruir las ejecuciones.

### 4. Streamlit

Streamlit actúa como interfaz entre el usuario y el agente.

Permite seleccionar parámetros y ejecutar el análisis sin necesidad de utilizar directamente la terminal.

La interfaz no modifica fuentes externas ni toma decisiones operacionales.

## Nivel de autonomía

El sistema opera con autonomía limitada.

### L0 — Ejecución automática

El agente puede consultar las fuentes habilitadas y procesar los resultados sin intervención humana durante cada paso técnico.

### L1 — Clasificación automática

Puede ordenar y clasificar los hechos por área, relevancia y estado de la información.

### L2 — Análisis asistido

Puede proponer tendencias, implicancias y necesidades de seguimiento.

Estas conclusiones son orientativas y deben diferenciarse de los hechos directamente respaldados por las fuentes.

### L3 — Revisión humana obligatoria

Un responsable humano debe revisar:

- alertas de alta relevancia;
- fuentes utilizadas;
- hechos incluidos;
- inferencias;
- tendencias;
- recomendaciones de seguimiento;
- limitaciones declaradas por el sistema.

### L4 — Decisión humana

La utilización, aprobación y distribución del informe corresponde exclusivamente a una persona.

El agente no tiene autoridad para adoptar decisiones operacionales ni para emitir un informe definitivo sin revisión humana.

## Principales riesgos

### Información insuficiente

La herramienta RSS proporciona principalmente títulos, fuentes, fechas y enlaces.

Esto puede ser insuficiente para verificar detalles técnicos, contexto completo o afirmaciones contenidas en una publicación.

Control:

El agente debe indicar expresamente esta limitación y evitar presentar como confirmado aquello que no puede sostener con la información disponible.

### Resultados irrelevantes

La búsqueda puede recuperar información comercial, recreativa, histórica o poco relacionada con el área seleccionada.

Control:

El modelo realiza una etapa de filtrado antes de generar el informe y puede excluir los resultados que no alcancen el nivel mínimo de relevancia.

### Fuente única o falta de corroboración

Un hecho puede aparecer respaldado solamente por una publicación.

Control:

El informe debe identificar la fuente utilizada y señalar cuando no existe corroboración independiente.

### Desinformación, propaganda o contenido sesgado

Una fuente pública puede contener errores, propaganda, desinformación o información interesada.

Control:

El agente no considera la aparición de una noticia como prueba automática de veracidad.

Los hechos sensibles deben ser revisados por una persona y, cuando corresponda, contrastados con fuentes adicionales.

### Inferencias del modelo

El modelo puede realizar interpretaciones que excedan la evidencia disponible.

Control:

El contrato obliga a diferenciar hechos de inferencias, indicar incertidumbre y evitar presentar hipótesis como hechos confirmados.

### Fallas de red o de una fuente

Una fuente externa puede no responder o limitar temporalmente las consultas.

Durante el desarrollo se comprobó este riesgo con la API pública de GDELT, que respondió con un error HTTP 429 por exceso de solicitudes.

Control:

Se abandonó esa herramienta como fuente principal y se adoptó RSS como mecanismo de recuperación más simple y estable.

Si la fuente RSS no responde o no devuelve información, el sistema debe detener la ejecución e informar el error en lugar de fabricar resultados.

### Fallas de la API del modelo

La API puede fallar por problemas de conexión, autenticación, límites de uso o indisponibilidad temporal.

Control:

La ejecución debe finalizar con un mensaje de error.

El sistema no debe generar un informe ficticio como reemplazo de una respuesta fallida.

### Exposición de credenciales

Existe riesgo si una clave de API se incluye accidentalmente dentro del código o del repositorio.

Control:

La clave se almacena como secreto o variable de entorno y nunca debe incorporarse directamente al código fuente.

## Qué ocurre ante una falla

El principio general es falla segura.

Si el sistema no puede recuperar fuentes o no puede obtener una respuesta válida del modelo:

1. se interrumpe la ejecución;
2. se informa el error al usuario;
3. no se genera información inventada;
4. el usuario debe decidir si vuelve a ejecutar el proceso.

## Trazabilidad

Las corridas conservadas permiten revisar:

- qué consulta se realizó;
- qué fuentes fueron recuperadas;
- qué modelo se utilizó;
- cuánto consumió la ejecución;
- qué respuesta produjo.

Esta trazabilidad permite comparar iteraciones y evaluar posteriormente errores o cambios de comportamiento.

## Revisión y aprobación humana

El sistema produce un documento de apoyo al análisis.

Antes de utilizar o distribuir el resultado, el responsable humano debe verificar especialmente:

- alertas de relevancia alta;
- coherencia entre hechos y fuentes;
- inferencias operacionales;
- contradicciones;
- ausencia de fuentes relevantes;
- limitaciones declaradas.

La responsabilidad final sobre la aprobación, firma, utilización o distribución del informe corresponde al analista o responsable humano designado.

El agente no firma, aprueba ni adopta decisiones en nombre del usuario.

## Principio de control

El sistema automatiza la búsqueda, organización, clasificación y análisis inicial de información pública.

La responsabilidad sobre la interpretación final y el uso del producto permanece siempre en una persona.