import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime


GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


def buscar_noticias_rss(consulta, dias=7, max_resultados=20):
    """
    Busca noticias recientes mediante Google News RSS.

    Parámetros:
        consulta: texto de búsqueda.
        dias: cantidad de días hacia atrás.
        max_resultados: cantidad máxima de noticias.

    Devuelve:
        lista de diccionarios con las noticias encontradas.
    """

    consulta_completa = f"{consulta} when:{dias}d"

    parametros = {
        "q": consulta_completa,
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
    }

    url = GOOGLE_NEWS_RSS + "?" + urllib.parse.urlencode(parametros)

    solicitud = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Agente-Alerta-Temprana-UCEMA/1.0"
        },
    )

    try:
        with urllib.request.urlopen(solicitud, timeout=30) as respuesta:
            contenido = respuesta.read()

    except Exception as error:
        raise RuntimeError(
            f"No se pudo consultar la fuente RSS: {error}"
        ) from error

    try:
        raiz = ET.fromstring(contenido)

    except ET.ParseError as error:
        raise RuntimeError(
            f"No se pudo interpretar la respuesta RSS: {error}"
        ) from error

    resultados = []

    for item in raiz.findall(".//item"):
        titulo = item.findtext("title", default="").strip()
        enlace = item.findtext("link", default="").strip()
        fecha_original = item.findtext("pubDate", default="").strip()

        fuente_elemento = item.find("source")

        if fuente_elemento is not None:
            fuente = (fuente_elemento.text or "").strip()
        else:
            fuente = ""

        fecha = fecha_original

        if fecha_original:
            try:
                fecha_dt = parsedate_to_datetime(fecha_original)
                fecha = fecha_dt.isoformat()
            except Exception:
                pass

        resultados.append(
            {
                "titulo": titulo,
                "url": enlace,
                "fuente": fuente,
                "fecha": fecha,
            }
        )

        if len(resultados) >= max_resultados:
            break

    return resultados


if __name__ == "__main__":
    consulta_prueba = '"FPV drone" OR "unmanned ground vehicle"'

    articulos = buscar_noticias_rss(
        consulta=consulta_prueba,
        dias=7,
        max_resultados=10,
    )

    print(f"\nResultados encontrados: {len(articulos)}\n")

    for numero, articulo in enumerate(articulos, start=1):
        print(f"{numero}. {articulo['titulo']}")
        print(f"   Fuente: {articulo['fuente']}")
        print(f"   Fecha: {articulo['fecha']}")
        print(f"   URL: {articulo['url']}")
        print()