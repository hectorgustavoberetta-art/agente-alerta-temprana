import streamlit as st
from pathlib import Path

from agente.analizador import analizar_alerta


# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------------

st.set_page_config(
    page_title="Sistema Agéntico de Alerta Temprana",
    page_icon="📡",
    layout="wide",
)


# ---------------------------------------------------------
# ESTILO VISUAL
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f6f8;
    }
    .block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e4e7eb;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    .info-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e4e7eb;
        margin-bottom: 16px;
    }

    .status-box {
        background: #f9f2f4;
        border-left: 5px solid #7A1730;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .result-section {
        background: white;
        padding: 22px 24px;
        border-radius: 12px;
        border: 1px solid #e4e7eb;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 18px;
    }

    .result-section h3 {
        color: #7A1730;
        margin-top: 0;
        margin-bottom: 14px;
        font-size: 22px;
    }

    .alert-card {
        background: #fff8f8;
        border-left: 5px solid #7A1730;
        padding: 16px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    .trend-card {
        background: #f7f8fa;
        border-left: 5px solid #6b7280;
        padding: 16px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    .limit-card {
        background: #fff9e8;
        border-left: 5px solid #d6a520;
        padding: 16px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    .result-meta {
        color: #6b7280;
        font-size: 13px;
        margin-bottom: 18px;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        padding-top: 30px;
        padding-bottom: 20px;
    }

    div.stButton > button[kind="primary"] {
    background-color: #7A1730;
    border-color: #7A1730;
    color: white;
    width: 100%;
    min-height: 52px;
    border-radius: 8px;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.2px;
    box-shadow: 0 3px 8px rgba(122, 23, 48, 0.18);
}

    div.stButton > button[kind="primary"]:hover {
        background-color: #651327;
        border-color: #651327;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# ENCABEZADO VISUAL
# ---------------------------------------------------------

st.image(
    "assets/banner_alerta_temprana.png",
    use_container_width=True,
)

# ---------------------------------------------------------
# PANEL LATERAL
# ---------------------------------------------------------

with st.sidebar:

    st.header("Configuración")

    st.caption(
        "Defina los parámetros que utilizará el agente para realizar el análisis."
    )

    areas = st.multiselect(
        "Áreas de interés",
        [
            "UAS / FPV / ISR",
            "UGV",
            "Drones logísticos / Sistemas autónomos",
            "Guerra de información / Desinformación",
            "Tecnologías emergentes",
        ],
        default=["UAS / FPV / ISR"],
    )

    dias = st.selectbox(
        "Período de análisis",
        [1, 3, 7, 14, 30],
        index=2,
        format_func=lambda x: f"Últimos {x} días",
    )

    relevancia = st.selectbox(
        "Relevancia mínima",
        ["Alta", "Media", "Baja"],
        index=1,
    )

    max_resultados = st.slider(
        "Cantidad máxima de fuentes",
        min_value=5,
        max_value=20,
        value=10,
        step=1,
    )

    st.divider()

    st.subheader("Supervisión")

    st.caption(
        "El informe requiere revisión humana antes de su utilización o distribución."
    )


# ---------------------------------------------------------
# CONSULTA AUTOMÁTICA
# ---------------------------------------------------------

consultas_por_area = {
    "UAS / FPV / ISR":
        '"FPV drone" OR UAV OR "unmanned aerial system"',

    "UGV":
        '"unmanned ground vehicle" OR UGV',

    "Drones logísticos / Sistemas autónomos":
        '"military logistics drone" OR "autonomous logistics systems"',

    "Guerra de información / Desinformación":
        '"military disinformation" OR "information warfare"',

    "Tecnologías emergentes":
        '"military autonomous systems" OR "emerging military technology"',
}


def construir_consulta(areas_seleccionadas):

    consultas = []

    for area in areas_seleccionadas:
        if area in consultas_por_area:
            consultas.append(f"({consultas_por_area[area]})")

    return " OR ".join(consultas)


# ---------------------------------------------------------
# ESTADO INICIAL
# ---------------------------------------------------------

if "resultado" not in st.session_state:
    st.session_state.resultado = None


# ---------------------------------------------------------
# PANEL PRINCIPAL
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Áreas seleccionadas",
        len(areas),
    )

with col2:
    st.metric(
        "Período",
        f"{dias} días",
    )

with col3:

    texto_relevancia = {
        "Alta": "Nivel alto",
        "Media": "Nivel medio",
        "Baja": "Nivel bajo",
    }.get(relevancia, str(relevancia))

    st.metric(
        "Relevancia mínima",
        texto_relevancia,
    )


st.markdown("### Ejecutar análisis")

st.markdown(
    """
    <div class="status-box">
    El agente buscará información pública reciente, filtrará los resultados,
    clasificará los hechos y generará un informe estructurado de alerta temprana.
    </div>
    """,
    unsafe_allow_html=True,
)


ejecutar = st.button(
    "Ejecutar análisis",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# EJECUCIÓN DEL AGENTE
# ---------------------------------------------------------

if ejecutar:

    if not areas:

        st.warning(
            "Seleccione al menos un área de interés."
        )

    else:

        consulta = construir_consulta(areas)

        try:

            with st.spinner(
                "Buscando fuentes y realizando análisis..."
            ):

                resultado = analizar_alerta(
                    consulta=consulta,
                    areas=areas,
                    dias=dias,
                    relevancia_minima=relevancia,
                    max_resultados=max_resultados,
                )

                st.session_state.resultado = resultado

            st.success(
                "Análisis completado correctamente."
            )

        except Exception as error:

            st.error(
                f"No se pudo completar el análisis: {error}"
            )


# ---------------------------------------------------------
# RESULTADOS
# ---------------------------------------------------------

resultado = st.session_state.resultado

if resultado:

    st.divider()

    st.markdown("## Resultados del análisis")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Fuentes",
            resultado["fuentes_recuperadas"],
        )

    with m2:
        st.metric(
            "Tokens entrada",
            resultado["tokens_entrada"],
        )

    with m3:
        st.metric(
            "Tokens salida",
            resultado["tokens_salida"],
        )

    with m4:
        st.metric(
            "Tokens totales",
            resultado["tokens_totales"],
        )

    st.caption(
        f'Modelo: {resultado["modelo"]} · '
        f'Fecha: {resultado["fecha_ejecucion"]}'
    )

    st.markdown("---")

    informe = resultado["informe"]

    secciones = {
        "Resumen ejecutivo": "",
        "Alertas prioritarias": "",
        "Informe estructurado": "",
        "Tendencias": "",
        "Limitaciones": "",
    }

    seccion_actual = None

    for linea in informe.splitlines():

        linea_limpia = linea.strip()

        if linea_limpia.startswith("## ") or linea_limpia.startswith("### "):

            titulo = linea_limpia.lstrip("#").strip()

            if titulo in secciones:
                seccion_actual = titulo
                continue

        if seccion_actual:
            secciones[seccion_actual] += linea + "\n"

    # -----------------------------------------------------
    # RESUMEN EJECUTIVO
    # -----------------------------------------------------

    if secciones["Resumen ejecutivo"].strip():

        st.markdown("### Resumen ejecutivo")

        with st.container(border=True):
            st.markdown(
                secciones["Resumen ejecutivo"].strip()
            )

    # -----------------------------------------------------
    # PESTAÑAS DE RESULTADOS
    # -----------------------------------------------------
    
    tab_alertas, tab_informe, tab_tendencias, tab_fuentes = st.tabs(
        [
            "🚨 Alertas prioritarias",
            "📋 Informe estructurado",
            "📈 Tendencias",
            "🔗 Fuentes",
        ]
    )
    
    # -----------------------------------------------------
    # ALERTAS PRIORITARIAS
    # -----------------------------------------------------
    
    with tab_alertas:
    
        if secciones["Alertas prioritarias"].strip():
    
            st.markdown("### Alertas prioritarias")
    
            with st.container(border=True):
                st.markdown(
                    secciones["Alertas prioritarias"].strip()
                )
    
        else:
            st.info("No se identificaron alertas prioritarias para esta corrida.")
    
    # -----------------------------------------------------
    # INFORME ESTRUCTURADO
    # -----------------------------------------------------
    
    with tab_informe:
    
        if secciones["Informe estructurado"].strip():
    
            st.markdown("### Informe estructurado")
    
            contenido_tabla = secciones["Informe estructurado"].strip()
    
            lineas_tabla = [
                linea.strip()
                for linea in contenido_tabla.splitlines()
                if linea.strip().startswith("|")
            ]
    
            if len(lineas_tabla) >= 3:
    
                encabezados = [
                    celda.strip()
                    for celda in lineas_tabla[0].strip("|").split("|")
                ]
    
                filas = lineas_tabla[2:]
    
                for numero, fila in enumerate(filas, start=1):
    
                    celdas = [
                        celda.strip()
                        for celda in fila.strip("|").split("|")
                    ]
    
                    if len(celdas) != len(encabezados):
                        continue
    
                    datos = dict(zip(encabezados, celdas))
    
                    area = datos.get("Área", "Sin área")
                    hecho = datos.get("Hecho", "Hecho sin descripción")
                    relevancia_hecho = datos.get(
                        "Relevancia",
                        "Sin clasificar",
                    )
    
                    normalizar_relevancia = {
                        "alta": "Alta",
                        "alto": "Alta",
                        "media": "Media",
                        "medio": "Media",
                        "medios": "Media",
                        "baja": "Baja",
                        "bajo": "Baja",
                    }
    
                    relevancia_hecho = normalizar_relevancia.get(
                        relevancia_hecho.strip().lower(),
                        relevancia_hecho,
                    )
    
                    icono_relevancia = {
                        "Alta": "🔴",
                        "Media": "🟠",
                        "Baja": "🟢",
                    }.get(relevancia_hecho, "⚪")
    
                    titulo_hecho = hecho
    
                    if len(titulo_hecho) > 115:
                        titulo_hecho = titulo_hecho[:112] + "..."
    
                    with st.expander(
                        f"{icono_relevancia} {numero}. {area} · "
                        f"{relevancia_hecho} · {titulo_hecho}"
                    ):
    
                        c1, c2, c3, c4 = st.columns(4)
    
                        with c1:
                            st.caption("PAÍS / ACTOR")
                            st.markdown(
                                datos.get(
                                    "País/Actor",
                                    "No informado",
                                )
                            )
    
                        with c2:
                            st.caption("FECHA")
                            st.markdown(
                                datos.get(
                                    "Fecha",
                                    "No informada",
                                )
                            )
    
                        with c3:
                            st.caption("RELEVANCIA")
                            st.markdown(
                                f"**{icono_relevancia} {relevancia_hecho}**"
                            )
    
                        with c4:
                            st.caption("FUENTE")
                            st.markdown(
                                datos.get(
                                    "Fuente",
                                    "No informada",
                                )
                            )
    
                        st.divider()
    
                        st.markdown("**Hecho**")
                        st.markdown(hecho)
    
                        st.markdown("**Estado de la información**")
                        st.markdown(
                            datos.get(
                                "Estado",
                                "No informado",
                            )
                        )
    
                        st.markdown("**Tendencia**")
                        st.markdown(
                            datos.get(
                                "Tendencia",
                                "No informada",
                            )
                        )
    
                        st.markdown("**Implicancia**")
                        st.markdown(
                            datos.get(
                                "Implicancia",
                                "No informada",
                            )
                        )
    
                        st.markdown("**Seguimiento recomendado**")
                        st.markdown(
                            datos.get(
                                "Seguimiento",
                                "No informado",
                            )
                        )
    
            else:
                st.markdown(contenido_tabla)
    
        else:
            st.info("No hay informe estructurado disponible.")
    
    # -----------------------------------------------------
    # TENDENCIAS
    # -----------------------------------------------------
    
    with tab_tendencias:
    
        if secciones["Tendencias"].strip():
    
            st.markdown("### Tendencias")
    
            with st.container(border=True):
                st.markdown(
                    secciones["Tendencias"].strip()
                )
    
        if secciones["Limitaciones"].strip():
    
            st.markdown("### Limitaciones del análisis")
    
            st.warning(
                secciones["Limitaciones"].strip()
            )
    
    # -----------------------------------------------------
    # FUENTES
    # -----------------------------------------------------
    
    with tab_fuentes:
    
        st.markdown("### Fuentes utilizadas")
    
        fuentes = resultado.get("fuentes", [])
    
        if fuentes:
    
            for numero, fuente in enumerate(fuentes, start=1):
    
                with st.container(border=True):
    
                    titulo_fuente = fuente.get(
                        "titulo",
                        "Fuente sin título",
                    )
    
                    nombre_fuente = fuente.get(
                        "fuente",
                        "Fuente no informada",
                    )
    
                    fecha_fuente = fuente.get(
                        "fecha",
                        "Fecha no informada",
                    )
    
                    url_fuente = fuente.get(
                        "url",
                        "",
                    )
    
                    st.markdown(
                        f"**{numero}. {titulo_fuente}**"
                    )
    
                    st.caption(
                        f"{nombre_fuente} · {fecha_fuente}"
                    )
    
                    if url_fuente:
                        st.markdown(
                            f"[Abrir fuente original]({url_fuente})"
                        )
    
        else:
            st.info("No hay fuentes disponibles para mostrar.")
            
        # -----------------------------------------------------
    # DESCARGA
    # -----------------------------------------------------

    st.markdown("---")

    nombre_archivo = Path(
        resultado["archivo_corrida"]
    ).name

    contenido_descarga = Path(
        resultado["archivo_corrida"]
    ).read_text(
        encoding="utf-8"
    )

    st.download_button(
        label="Descargar informe",
        data=contenido_descarga,
        file_name=nombre_archivo,
        mime="text/markdown",
        use_container_width=True,
    )


# ---------------------------------------------------------
# PIE
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Sistema Agéntico de Alerta Temprana ·
        MBA UCEMA · Programación de y con Agentes de IA · 2026
        <br>
        Producto de apoyo al análisis sujeto a supervisión humana.
    </div>
    """,
    unsafe_allow_html=True,
)