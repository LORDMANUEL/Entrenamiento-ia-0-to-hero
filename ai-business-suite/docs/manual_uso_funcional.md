# 🎯 Manual de Uso Funcional - AI Business Suite

Este manual describe cómo utilizar las herramientas de inteligencia artificial disponibles en el dashboard de AI Business Suite. La guía está diseñada para usuarios de negocio, analistas y gerentes.

---

## 🚀 Acceso a la Plataforma

Para comenzar, abra su navegador web y vaya a la dirección donde se está ejecutando la aplicación (por ejemplo, `http://localhost:5173`).

Verá un panel de control con una barra de navegación a la izquierda. Cada elemento del menú corresponde a una herramienta de IA específica.

---

### 📈 Herramienta 1: Forecast de Demanda

**Objetivo:** Predecir la cantidad de ventas de un repuesto para el próximo mes en un almacén específico.

**¿Cuándo usarla?** Utilice esta herramienta para optimizar el inventario, planificar compras y evitar quiebres de stock.

**Pasos para usar:**

1.  **Navegación:** Haga clic en **"Forecast Demanda"** en el menú lateral.
2.  **Rellenar Parámetros:**
    *   **Item Code:** Ingrese el código del producto que desea analizar (ej: `ITM001`).
    *   **Almacén:** Especifique el código del almacén (ej: `WHS01`).
3.  **Ingresar Histórico de Ventas:**
    *   La plataforma muestra una tabla pre-rellenada para los últimos 12 meses.
    *   Rellene la columna **"Cantidad"** con las ventas reales de cada mes. Es importante proporcionar al menos 3-6 meses de datos reales para obtener una predicción fiable. Los meses sin ventas pueden dejarse en `0`.
4.  **Calcular Forecast:**
    *   Haga clic en el botón **"Calcular Forecast"**.
5.  **Interpretar Resultados:**
    *   A la derecha, aparecerá la sección de resultados:
        *   **Demanda estimada próximo mes:** El número de unidades que el modelo predice que se venderán.
        *   **Nivel de Demanda:** Un indicador visual (Bajo, Medio, Alto) para una rápida interpretación.
        *   **Gráfico de Evolución:** Una línea de tiempo que muestra las ventas históricas y el punto de la predicción, permitiéndole ver la tendencia visualmente.

---

### 💳 Herramienta 2: Scoring de Riesgo de Morosidad

**Objetivo:** Evaluar la probabilidad de que un cliente se atrase en el pago de una nueva operación comercial.

**¿Cuándo usarla?** Antes de aprobar una venta a crédito, extender un plazo de pago o realizar una operación de alto valor. Ayuda a tomar decisiones financieras más seguras.

**Pasos para usar:**

1.  **Navegación:** Haga clic en **"Riesgo de Morosidad"** en el menú.
2.  **Rellenar Datos de la Operación:**
    *   **Segmento:** Elija el tipo de cliente (Retail, Empresa, Gobierno).
    *   **Ciudad:** Ingrese la ciudad del cliente.
    *   **Monto:** El valor total de la operación.
    *   **Plazo (días):** Los días de crédito que se otorgan.
    *   **Veces en Mora:** Cuántas veces el cliente se ha atrasado en pagos anteriores.
    *   **Días Promedio en Mora:** El promedio de días que el cliente se ha retrasado en sus pagos.
3.  **Calcular Riesgo:**
    *   Haga clic en el botón **"Calcular Riesgo"**.
4.  **Interpretar Resultados:**
    *   La tarjeta de resultados mostrará:
        *   **Nivel de Riesgo:** Una clasificación clara (BAJO, MEDIO, ALTO) con un código de colores (verde, amarillo, rojo).
        *   **Probabilidad de Atraso:** El porcentaje específico de riesgo (de 0% a 100%). Un gráfico de "velocímetro" le dará una idea visual inmediata.
        *   **Explicación del Modelo:** Una breve descripción en texto que justifica el porqué de la clasificación, basada en los datos que ingresó.

---

### 🧾 Herramienta 3: Tickets IA

**Objetivo:** Clasificar automáticamente un ticket de soporte o una orden de trabajo y recibir sugerencias de soluciones basadas en casos históricos similares.

**¿Cuándo usarla?** Ideal para equipos de soporte, talleres o servicio al cliente para agilizar la asignación de tareas y la resolución de problemas.

**Pasos para usar:**

1.  **Navegación:** Haga clic en **"Tickets IA"** en el menú.
2.  **Describir el Problema:**
    *   En el área de texto de la izquierda, escriba una descripción detallada del problema o solicitud del cliente. Sea lo más específico posible.
3.  **Obtener Análisis:**
    *   **Para categorizar:** Haga clic en **"Clasificar Ticket"**.
        *   El sistema analizará el texto y en la tarjeta de la derecha le mostrará la **"Categoría Predicha"** (ej: MECANICO, ELECTRICO) y la **"Confianza"** del modelo en esa predicción.
    *   **Para encontrar soluciones:** Haga clic en **"Sugerir Solución"**.
        *   Además de clasificar el ticket, el sistema buscará en la base de datos de tickets históricos y mostrará una lista de **"Soluciones Sugeridas"**.
        *   Cada sugerencia incluye un resumen de la solución aplicada en el pasado, el ID del ticket original y el nivel de similitud con el problema que describió.
