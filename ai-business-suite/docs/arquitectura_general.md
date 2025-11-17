# 📄 Arquitectura General - AI Business Suite

Este documento describe la arquitectura de alto nivel del proyecto AI Business Suite, mostrando cómo interactúan sus componentes principales.

## Diagrama de Flujo Lógico

El sistema se puede dividir en cuatro capas principales:
1.  **Capa de Datos (Data Layer):** Donde residen los datos crudos y se originan los modelos.
2.  **Capa de Machine Learning (ML Layer):** Donde se entrenan los modelos y se guardan los artefactos.
3.  **Capa de Servicio (Service Layer):** La API de backend que expone los modelos como endpoints.
4.  **Capa de Presentación (Presentation Layer):** La interfaz de usuario web con la que interactúa el usuario final.

A continuación, un diagrama textual que ilustra el flujo:

```
+---------------------+      +------------------------+      +---------------------+      +-----------------------+
|    📂 DATA LAYER    |      |    🧠 ML TRAINING      |      |   🌐 SERVICE LAYER  |      |   🖥️ PRESENTATION   |
|---------------------|      |------------------------|      |---------------------|      |-----------------------|
|                     |      |                        |      |                     |      |                       |
| data/               |      | scripts/               |      | backend/            |      | frontend/             |
|  ├─ raw/            |  ──> |  ├─ train_forecast.py  |  ──> |  ├─ models_ml/     |  ──> |  ├─ src/pages/       |
|  │  ├─ sales.csv    |      |  ├─ train_risk.py      |      |  │  ├─ model.pkl   |      |  │  ├─ Forecast.tsx |
|  │  ├─ risk.csv     |      |  ├─ train_nlp.py       |      |  │  └─ vector.pkl  |      |  │  ├─ Risk.tsx     |
|  │  └─ tickets.csv  |      |                        |      |  ├─ routers/        |      |  │  └─ Tickets.tsx  |
|                     |      +------------------------+      |  │  ├─ forecast.py  |      |  ├─ lib/api.ts       |
|                     |                 |                    |  │  ├─ risk.py      |      |                       |
|                     |                 ▼                    |  │  └─ nlp.py      |      |         │             |
|                     |      +------------------------+      |  ├─ main.py (API)  |      |         │             |
|                     |      |   📦 ML ARTIFACTS      |      |                     |      |         ▼             |
|                     |      |------------------------|      |                     |      |  [ Usuario Final ]    |
|                     |      | backend/models_ml/     |      |                     |      |                       |
|                     |      |  ├─ forecast/model.pkl |      +---------------------+      +-----------------------+
|                     |      |  ├─ risk/model.pkl     |                 ▲
|                     |      |  └─ nlp/model.pkl      |                 │
|                     |      +------------------------+                 │
|                     |                                                 │
+---------------------+                                                 │
                                                                        │
                               +----------------------------------------+
                               |        ⚙️ AUTOMATION (e.g., n8n)       |
                               |----------------------------------------|
                               | scripts/                               |
                               |  └─ example_workflow.json             |
                               |     (Calls API endpoints)              |
                               +----------------------------------------+

```

## Flujo de Trabajo

1.  **Entrenamiento de Modelos:**
    *   Los datos de ejemplo se encuentran en `data/raw/*.csv`.
    *   Los scripts en `backend/app/models_ml/{modulo}/train_*.py` leen estos datos.
    *   Cada script procesa los datos, entrena un modelo de scikit-learn y guarda el artefacto (`.pkl`) en su respectivo directorio dentro de `backend/app/models_ml/`.

2.  **Exposición vía API:**
    *   La aplicación `FastAPI` en `backend/app/main.py` se inicia.
    *   En el arranque, los módulos de servicio (`services/*_service.py`) cargan los modelos `.pkl` en memoria.
    *   Los `routers` (`routers/*.py`) definen los endpoints (`/api/forecast/predict`, `/api/risk/score`, etc.).
    *   Cuando un router recibe una petición, la pasa al servicio correspondiente, que utiliza el modelo cargado para generar una predicción.
    *   La respuesta se devuelve en formato JSON.

3.  **Interacción con el Frontend:**
    *   La aplicación `React` (iniciada con `npm run dev` en `frontend/`) se ejecuta en el navegador del usuario.
    *   Cuando el usuario interactúa (por ejemplo, rellenando un formulario y haciendo clic en "Calcular"), una función en `frontend/src/lib/api.ts` realiza una llamada `fetch` al endpoint correspondiente de la API FastAPI.
    *   La respuesta de la API se procesa y se utiliza para actualizar el estado de la aplicación React, mostrando los resultados en la interfaz de usuario (por ejemplo, un gráfico o una tarjeta de resultados).

4.  **Automatización:**
    *   Sistemas externos como `n8n`, `Zapier` o `cron jobs` pueden interactuar directamente con la API de FastAPI.
    *   El `scripts/example_n8n_workflow.json` muestra un ejemplo de cómo un flujo de trabajo puede llamar a un endpoint (`/api/forecast/top-items`) para obtener datos y tomar decisiones (por ejemplo, enviar un correo electrónico).

## Stack Tecnológico

*   **Backend:** Python 3.11+, FastAPI, Pydantic, scikit-learn, Pandas.
*   **Frontend:** React, TypeScript, Vite, TailwindCSS, Recharts.
*   **Base de Datos:** No se utiliza una base de datos persistente para los datos de negocio. SQLite podría usarse para configuraciones o logs, pero está fuera del alcance inicial.
*   **Contenerización:** Docker y Docker Compose para empaquetar y orquestar los servicios.
