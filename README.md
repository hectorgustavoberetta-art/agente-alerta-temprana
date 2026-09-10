# Sistema Agéntico de Alerta Temprana y Situación Operacional

Trabajo Final — Programación de y con Agentes de IA  
MBA UCEMA · 2026 2T

## Descripción

Este proyecto implementa un sistema agéntico para recopilar, filtrar, clasificar y sintetizar información pública reciente relacionada con tecnologías y acontecimientos de interés para la situación operacional.

El sistema no funciona como un chatbot de propósito general. Ejecuta un proceso definido mediante un contrato escrito, utiliza una herramienta real para recuperar información, analiza los resultados mediante un modelo de IA, produce una salida estructurada y conserva evidencia de sus ejecuciones.

## Objetivo

El sistema busca detectar hechos relevantes y tendencias relacionados con:

- UAS, UAV, drones FPV e ISR;
- UGV y sistemas terrestres no tripulados;
- drones logísticos y sistemas autónomos;
- guerra de información y desinformación;
- tecnologías militares emergentes relacionadas con estos ámbitos.

El resultado es un informe de apoyo al análisis que requiere supervisión humana antes de su utilización o distribución.

## Arquitectura

El flujo principal es:

Usuario  
↓  
Interfaz Streamlit  
↓  
Selección de parámetros  
↓  
Búsqueda de información pública mediante RSS  
↓  
Filtrado y preparación de fuentes  
↓  
Análisis mediante OpenAI API  
↓  
Informe estructurado  
↓  
Registro de la corrida  
↓  
Revisión humana

## Herramientas utilizadas

### Google News RSS

Se utiliza como herramienta real para recuperar noticias públicas recientes.

Para cada resultado se obtienen:

- título;
- fuente;
- fecha;
- URL.

La versión actual trabaja principalmente con títulos y metadatos. No recupera automáticamente el texto completo de los artículos.

### OpenAI API

La API procesa las fuentes recuperadas y genera el informe de acuerdo con el contrato definido en:

- `prompts/system_prompt.md`
- `prompts/user_prompt.md`

El modelo predeterminado es:

`gpt-5.6-luna`

La selección de este modelo se encuentra justificada en `analisis_economico.md` y documentada en `DECISIONES.md`.

### Streamlit

`app.py` proporciona la interfaz visual del sistema.

Permite seleccionar:

- áreas de interés;
- período de análisis;
- nivel mínimo de relevancia;
- cantidad máxima de fuentes.

## Salida del sistema

Cada informe contiene:

1. Resumen ejecutivo.
2. Alertas prioritarias.
3. Informe estructurado.
4. Tendencias.
5. Limitaciones.

El informe estructurado utiliza los siguientes campos:

| Área | Hecho | País/Actor | Fecha | Fuente | Relevancia | Estado | Tendencia | Implicancia | Seguimiento |
|---|---|---|---|---|---|---|---|---|---|

## Supervisión humana

El sistema trabaja con autonomía limitada.

Puede buscar, ordenar, clasificar y realizar análisis iniciales, pero no adopta decisiones operacionales.

Las alertas relevantes, las fuentes, las inferencias, las tendencias y las recomendaciones deben ser revisadas por una persona antes de utilizar o distribuir el informe.

La política completa se encuentra en:

`gobierno_riesgos.md`

## Estructura del repositorio

```text
agente-alerta-temprana/
│
├── README.md
├── app.py
├── requirements.txt
├── DECISIONES.md
├── analisis_economico.md
├── gobierno_riesgos.md
│
├── agente/
│   ├── __init__.py
│   └── analizador.py
│
├── herramientas/
│   ├── __init__.py
│   ├── busqueda_rss.py
│   └── busqueda_gdelt.py
│
├── prompts/
│   ├── system_prompt.md
│   └── user_prompt.md
│
└── corridas/
    ├── README.md
    ├── corrida_01.md
    ├── corrida_02.md
    ├── corrida_03.md
    ├── corrida_04.md
    └── corrida_05.md
