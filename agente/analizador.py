import json
import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI

from herramientas.busqueda_rss import buscar_noticias_rss


MODELO = "gpt-5.6-luna"

BASE_DIR = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT = BASE_DIR / "prompts" / "system_prompt.md"

USER_PROMPT = BASE_DIR / "prompts" / "user_prompt.md"

def cargar_system_prompt():
    return SYSTEM_PROMPT.read_text(encoding="utf-8")

def cargar_user_prompt():
    return USER_PROMPT.read_text(encoding="utf-8")

def preparar_fuentes(articulos):
    fuentes = []

    for numero, articulo in enumerate(articulos, start=1):
        fuentes.append(
            {
                "id": numero,
                "titulo": articulo.get("titulo", ""),
                "fuente": articulo.get("fuente", ""),
                "fecha": articulo.get("fecha", ""),
                "url": articulo.get("url", ""),
            }
        )

    return fuentes


def analizar_alerta(
    consulta,
    areas,
    dias=7,
    relevancia_minima="Media",
    max_resultados=10,
    modelo=MODELO,
):
    """
    Busca información real mediante RSS y solicita al modelo
    que filtre, clasifique y analice los resultados.
    """

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "No se encontró la variable de entorno OPENAI_API_KEY."
        )

    articulos = buscar_noticias_rss(
        consulta=consulta,
        dias=dias,
        max_resultados=max_resultados,
    )

    if not articulos:
        raise RuntimeError(
            "La búsqueda no devolvió noticias para analizar."
        )

    fuentes = preparar_fuentes(articulos)

    system_prompt = cargar_system_prompt()

    user_prompt = cargar_user_prompt()

    solicitud = (
        user_prompt
        .replace("{{periodo}}", f"Últimos {dias} días")
        .replace("{{areas}}", ", ".join(areas))
        .replace("{{relevancia_minima}}", relevancia_minima)
        .replace(
            "{{fuentes_adicionales}}",
            json.dumps(fuentes, ensure_ascii=False, indent=2),
        )
    )

    solicitud += """

## Instrucciones técnicas de ejecución

- Descartá resultados comerciales, recreativos o irrelevantes.
- Conservá la URL correspondiente a cada hecho utilizado.
- Utilizá exclusivamente las fuentes recuperadas en esta ejecución.
"""

    cliente = OpenAI()

    respuesta = cliente.responses.create(
    model=modelo,
        instructions=system_prompt,
        input=solicitud,
    )

    uso = respuesta.usage

    resultado = {
        "fecha_ejecucion": datetime.now().astimezone().isoformat(),
        "modelo": respuesta.model,
        "consulta": consulta,
        "areas": areas,
        "dias": dias,
        "relevancia_minima": relevancia_minima,
        "fuentes_recuperadas": len(fuentes),
        "fuentes": fuentes,
        "tokens_entrada": uso.input_tokens if uso else None,
        "tokens_salida": uso.output_tokens if uso else None,
        "tokens_totales": uso.total_tokens if uso else None,
        "informe": respuesta.output_text,
    }
    # Guardar automáticamente la corrida
    carpeta_corridas = BASE_DIR / "corridas"
    carpeta_corridas.mkdir(exist_ok=True)

    corridas_existentes = sorted(
        carpeta_corridas.glob("corrida_*.md")
    )

    numero_corrida = len(corridas_existentes) + 1
    archivo_corrida = carpeta_corridas / f"corrida_{numero_corrida:02d}.md"

    contenido_corrida = f"""# Corrida {numero_corrida:02d}

## Datos de ejecución

- Fecha: {resultado["fecha_ejecucion"]}
- Modelo: {resultado["modelo"]}
- Consulta: {resultado["consulta"]}
- Áreas: {", ".join(resultado["areas"])}
- Período: últimos {resultado["dias"]} días
- Relevancia mínima: {resultado["relevancia_minima"]}
- Fuentes recuperadas: {resultado["fuentes_recuperadas"]}
- Tokens de entrada: {resultado["tokens_entrada"]}
- Tokens de salida: {resultado["tokens_salida"]}
- Tokens totales: {resultado["tokens_totales"]}

## Fuentes utilizadas

```json
{json.dumps(resultado["fuentes"], ensure_ascii=False, indent=2)}
```

## Salida del agente

{resultado["informe"]}
"""

    archivo_corrida.write_text(
        contenido_corrida,
        encoding="utf-8",
    )

    resultado["archivo_corrida"] = str(archivo_corrida)

    return resultado


if __name__ == "__main__":
    resultado = analizar_alerta(
        consulta='"FPV drone" OR "unmanned ground vehicle"',
        areas=[
            "UAS / FPV / ISR",
            "UGV",
        ],
        dias=7,
        relevancia_minima="Media",
        max_resultados=10,
    )

    print("\n=== INFORME GENERADO ===\n")
    print(resultado["informe"])

    print("\n=== DATOS DE LA CORRIDA ===\n")
    print(f"Fecha: {resultado['fecha_ejecucion']}")
    print(f"Modelo: {resultado['modelo']}")
    print(f"Fuentes recuperadas: {resultado['fuentes_recuperadas']}")
    print(f"Tokens entrada: {resultado['tokens_entrada']}")
    print(f"Tokens salida: {resultado['tokens_salida']}")
    print(f"Tokens totales: {resultado['tokens_totales']}")