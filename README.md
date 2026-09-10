# Sistema Agéntico de Alerta Temprana y Situación Operacional

Trabajo Final — Programación de y con Agentes de IA  
MBA UCEMA · 2026 2T

## Aplicación pública

El sistema se encuentra desplegado en Streamlit Community Cloud y puede ejecutarse directamente desde:

**[Abrir Sistema Agéntico de Alerta Temprana](https://agente-alerta-temprana.streamlit.app)**

La aplicación permite seleccionar las áreas de interés, el período de análisis, el nivel mínimo de relevancia y la cantidad máxima de fuentes. Cada ejecución recupera información pública reciente, realiza el análisis mediante el agente y presenta los resultados en una interfaz estructurada.

> El resultado constituye un producto de apoyo al análisis y requiere revisión humana antes de su utilización o distribución.

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
├── assets/
│   └── banner_alerta_temprana.png
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
    ├── corrida_05.md
    ├── corrida_06.md
    ├── corrida_07.md
    ├── corrida_08.md
    ├── corrida_09.md
    ├── corrida_10.md
    └── corrida_11.md
    
## Instalación y reproducción

El sistema puede reproducirse desde un entorno local o desde GitHub Codespaces.

### 1. Clonar el repositorio

```bash
git clone https://github.com/hectorgustavoberetta-art/agente-alerta-temprana.git
cd agente-alerta-temprana
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la API de OpenAI

El sistema requiere una variable de entorno denominada `OPENAI_API_KEY`.

La clave debe configurarse como secreto o variable de entorno y no debe incorporarse al código ni publicarse en el repositorio.

En Linux, macOS o GitHub Codespaces:

```bash
export OPENAI_API_KEY="TU_CLAVE_DE_OPENAI"
```

En GitHub Codespaces puede configurarse mediante Codespaces Secrets.

En Streamlit Community Cloud debe configurarse como secreto de la aplicación con el nombre `OPENAI_API_KEY`.

### 4. Ejecutar por terminal

```bash
python -m agente.analizador
```

La ejecución recupera información pública, realiza el análisis y guarda automáticamente la evidencia en la carpeta `corridas/`.

### 5. Ejecutar con Streamlit

```bash
streamlit run app.py
```

También puede utilizarse:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### 6. Evidencia y reproducibilidad

La carpeta `corridas/` conserva las ejecuciones realizadas durante el desarrollo y validación del sistema.

Cada corrida permite revisar, según la versión correspondiente:

- fecha de ejecución;
- parámetros utilizados;
- modelo empleado;
- fuentes recuperadas;
- consumo de tokens;
- resultado generado.

Las salidas se preservan como evidencia del proceso. Si una ejecución presenta una URL malformada o una salida defectuosa, no se modifica retroactivamente; se conserva como parte de la trazabilidad.

Para reconstruir el funcionamiento del proyecto, un tercero debe:

1. clonar el repositorio;
2. instalar `requirements.txt`;
3. configurar su propia `OPENAI_API_KEY`;
4. ejecutar `python -m agente.analizador` o `streamlit run app.py`;
5. comparar la nueva ejecución con las evidencias almacenadas en `corridas/`.

Los resultados pueden variar con el tiempo porque el sistema consulta información pública reciente y utiliza un modelo generativo. La arquitectura, los prompts, las herramientas y el procedimiento de ejecución permanecen documentados en el repositorio.