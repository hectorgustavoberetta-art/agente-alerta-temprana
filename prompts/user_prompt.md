# User Prompt — Sistema Agéntico de Alerta Temprana

## Solicitud de análisis

Generá un informe de alerta temprana y situación operacional utilizando únicamente información obtenida mediante las herramientas habilitadas y los parámetros indicados a continuación.

## Parámetros de la ejecución

**Período de análisis:**  
{{periodo}}

**Áreas de interés:**  
{{areas}}

**Nivel mínimo de relevancia:**  
{{relevancia_minima}}

**Fuentes o información adicional proporcionada por el usuario:**  
{{fuentes_adicionales}}

## Instrucciones

1. Analizá únicamente información comprendida dentro del período solicitado, salvo antecedentes indispensables para explicar un hecho actual.
2. Priorizá información directamente relacionada con las áreas seleccionadas.
3. Identificá claramente la fuente utilizada para cada hecho.
4. No inventes información para completar campos faltantes.
5. Cuando un dato no pueda verificarse, indicá su condición de incertidumbre.
6. Diferenciá los hechos observados de las inferencias realizadas.
7. Clasificá la relevancia de cada hecho como Alta, Media o Baja.
8. Excluí de la salida final los hechos que estén por debajo del nivel mínimo de relevancia solicitado.
9. Identificá tendencias solamente cuando exista evidencia suficiente para sostenerlas.
10. Toda implicancia o recomendación de seguimiento debe estar vinculada con la evidencia analizada.

## Formato esperado

Entregá la respuesta en las siguientes secciones:

### Resumen ejecutivo

Síntesis de los acontecimientos más relevantes del período.

### Alertas prioritarias

Principales hechos que requieren atención o seguimiento.

### Informe estructurado

| Área | Hecho | País/Actor | Fecha | Fuente | Relevancia | Estado | Tendencia | Implicancia | Seguimiento |
|---|---|---|---|---|---|---|---|---|---|

### Tendencias

Principales patrones o evoluciones identificados.

### Limitaciones

Indicá información faltante, fuentes contradictorias, incertidumbres o cualquier otra limitación que afecte el análisis.

## Condición de cierre

El resultado es un producto de apoyo al análisis y requiere revisión humana antes de su utilización o distribución.