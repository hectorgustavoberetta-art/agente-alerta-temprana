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

    .main-header {
        background: #7A1730;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 24px;
        color: white;
    }

    .main-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }

    .main-header p {
        margin-top: 8px;
        margin-bottom: 0;
        font-size: 16px;
        opacity: 0.92;
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
# ENCABEZADO
# ---------------------------------------------------------

st.markdown(
    """
    <div class="main-header">
        <h1>Sistema Agéntico de Alerta Temprana</h1>
        <p>Análisis de información pública para apoyo a la situación operacional</p>
    </div>
    """,
    unsafe_allow_html=True,
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
    st.metric(
        "Relevancia mínima",
        str(relevancia),
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

    st.markdown(
        resultado["informe"]
    )


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