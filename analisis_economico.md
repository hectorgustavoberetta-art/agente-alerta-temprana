# Análisis económico

## Objetivo

El análisis económico busca estimar el costo de operación del Sistema Agéntico de Alerta Temprana y justificar la selección del modelo de menor costo que demostró calidad suficiente para la tarea.

## Modelos evaluados

Durante el desarrollo inicial se utilizó `gpt-5.6-sol`.

Posteriormente se realizó una prueba real con `gpt-5.6-luna` para determinar si un modelo de menor costo podía mantener la calidad necesaria.

Los precios de referencia utilizados son los publicados por OpenAI para procesamiento estándar:

| Modelo | Entrada por 1M tokens | Salida por 1M tokens |
|---|---:|---:|
| gpt-5.6-sol | USD 4,00 | USD 20,00 |
| gpt-5.6-luna | USD 0,20 | USD 1,20 |

## Medición real con Luna

La Corrida 05 registró:

- Tokens de entrada: 3.873
- Tokens de salida: 3.180
- Tokens totales: 7.053

### Costo de entrada

3.873 / 1.000.000 × USD 0,20 = USD 0,000775

### Costo de salida

3.180 / 1.000.000 × USD 1,20 = USD 0,003816

### Costo total de la ejecución

USD 0,000775 + USD 0,003816 = **USD 0,004591**

Por lo tanto, una ejecución representativa cuesta aproximadamente **USD 0,0046**.

## Proyección de uso

Para proyectar el costo operativo se adopta como supuesto una ejecución semanal del informe.

Este supuesto no corresponde a una medición del sistema sino a un escenario de utilización.

### Costo semanal estimado

1 ejecución × USD 0,004591 = **USD 0,004591 por semana**

### Costo anual estimado

52 ejecuciones × USD 0,004591 = **USD 0,2387 por año**

El costo anual estimado del modelo es, por lo tanto, aproximadamente **USD 0,24**, bajo el supuesto de una ejecución semanal con un volumen de tokens semejante al observado en la Corrida 05.

## Comparación económica con Sol

Si la misma cantidad de tokens de la Corrida 05 se procesara con `gpt-5.6-sol`:

Entrada:

3.873 / 1.000.000 × USD 4,00 = USD 0,015492

Salida:

3.180 / 1.000.000 × USD 20,00 = USD 0,063600

Costo total estimado con Sol:

**USD 0,079092 por ejecución**

Frente a aproximadamente USD 0,004591 con Luna, el uso de Luna representa una reducción aproximada del **94 %** para este patrón de tokens.

## Selección del modelo

La decisión no se tomó únicamente por precio.

La Corrida 05 permitió comprobar que `gpt-5.6-luna` mantuvo:

- el formato estructurado requerido;
- la identificación de alertas;
- el filtrado de información poco pertinente;
- la trazabilidad con las fuentes;
- la diferenciación entre hechos e inferencias;
- la explicitación de limitaciones;
- la necesidad de supervisión humana.

Por lo tanto, `gpt-5.6-luna` fue seleccionado como modelo predeterminado porque fue el modelo de menor costo probado que demostró calidad suficiente para esta tarea.

No se consideró necesario utilizar un modelo intermedio una vez comprobado que Luna cumplía satisfactoriamente el contrato del sistema.

## Alcance de la estimación

Los valores anteriores representan únicamente el costo estimado de tokens del modelo.

No incluyen eventuales costos futuros de infraestructura, alojamiento, servicios externos o herramientas pagas.

La fuente RSS utilizada actualmente es de acceso público y el sistema no incorpora en esta versión otros servicios pagos además de la API del modelo.