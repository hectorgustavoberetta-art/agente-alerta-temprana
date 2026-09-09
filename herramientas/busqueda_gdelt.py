import json
import urllib.parse
import urllib.request


GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def buscar_noticias(consulta, dias=7, max_resultados=20):
    """
    Busca artículos recientes en GDELT.

    Parámetros:
        consulta: texto de búsqueda.
        dias: cantidad de días hacia atrás.
        max_resultados: cantidad máxima de artículos.

    Devuelve:
        lista de diccionarios con artículos encontrados.
    """

    parametros = {
        "query": consulta,
        "mode": "artlist",
        "format": "json",
        "timespan": f"{dias}d",
        "maxrecords": max_resultados,
        "sort": "datedesc",
    }

    url = GDELT_URL + "?" + urllib.parse.urlencode(parametros)

    solicitud = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Agente-Alerta-Temprana-UCEMA/1.0"
        },
    )

    try:
        with urllib.request.urlopen(solicitud, timeout=30) as respuesta:
            datos = json.loads(respuesta.read().decode("utf-8"))

    except Exception as error:
        raise RuntimeError(
            f"No se pudo consultar GDELT: {error}"
        ) from error

    resultados = []

    for articulo in datos.get("articles", []):
        resultados.append(
            {
                "titulo": articulo.get("title", ""),
                "url": articulo.get("url", ""),
                "fuente": articulo.get("domain", ""),
                "fecha": articulo.get("seendate", ""),
                "idioma": articulo.get("language", ""),
                "pais_fuente": articulo.get("sourcecountry", ""),
            }
        )

    return resultados


if __name__ == "__main__":
    consulta_prueba = '"FPV drone" OR "unmanned ground vehicle"'

    articulos = buscar_noticias(
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