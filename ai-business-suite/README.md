# 🚀 AI Business Suite: Monorepo de IA Aplicada a Negocio

![Banner](https://i.imgur.com/your-banner-image.png) <!-- Reemplazar con un banner real si se desea -->

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.95+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18+-blueviolet.svg" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5+-informational.svg" alt="TypeScript">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
</p>

---

### 🌟 **Visión del Proyecto**

Nuestra visión es democratizar el acceso a la inteligencia artificial para empresas de cualquier tamaño, proporcionando herramientas modulares, prácticas y listas para producción que resuelvan problemas de negocio reales y generen un impacto medible.

### 🎯 **Misión**

Construir una suite de soluciones de IA robusta, escalable y fácil de implementar on-premise, enfocada en optimizar operaciones clave en áreas como **logística, finanzas y soporte al cliente**.

### ✨ **Objetivos Principales**

*   **Funcionalidad Completa:** Entregar un monorepo 100% funcional con código ejecutable.
*   **Modularidad:** Permitir que cada módulo de IA se utilice de forma independiente o conjunta.
*   **Facilidad de Uso:** Ofrecer una interfaz de usuario web intuitiva y una API bien documentada.
*   **Listo para Producción:** Proveer configuraciones y scripts para un despliegue on-premise sin fricciones.

---

## 🛠️ **Módulos de la Suite**

La suite se compone de cuatro módulos principales que trabajan en sinergia.

###  forecasting 🔮 **1. Forecast de Demanda de Repuestos**

*   **Área:** `Logística & Inventario`
*   **Tecnología:** `Regresión / Series de Tiempo`
*   **Descripción:** Este módulo utiliza el historial de ventas mensuales para predecir la demanda futura de cada repuesto en cada almacén. Analiza tendencias y estacionalidades para generar pronósticos precisos.
*   **Funcionamiento:**
    1.  El modelo (`RandomForestRegressor`) se entrena con datos históricos de ventas (`ventas_repuestos.csv`).
    2.  Se generan *features* clave como ventas de meses anteriores (lags) y variables de calendario (mes, año).
    3.  La API expone un endpoint `POST /api/forecast/predict` que recibe el historial reciente de un item.
    4.  El frontend permite al usuario introducir estos datos y visualiza la predicción en un gráfico, ayudando a los planificadores de inventario a tomar decisiones informadas.

---

### 💳 **2. Scoring de Riesgo de Morosidad**

*   **Área:** `Finanzas & Riesgo Crediticio`
*   **Tecnología:** `Clasificación Binaria`
*   **Descripción:** Evalúa el riesgo de que un cliente no cumpla con sus obligaciones de pago para una operación específica. El modelo asigna una probabilidad de atraso y clasifica al cliente en un nivel de riesgo.
*   **Funcionamiento:**
    1.  Se entrena un pipeline (`LogisticRegression` + preprocesadores) con un dataset de operaciones pasadas (`riesgo_clientes.csv`).
    2.  El pipeline transforma automáticamente variables categóricas (como ciudad) y escala las numéricas (como monto).
    3.  A través del endpoint `POST /api/risk/score`, se envían los datos de una nueva operación.
    4.  La interfaz web presenta el resultado de forma clara y visual: un **bucket de riesgo** (🟢 BAJO, 🟡 MEDIO, 🔴 ALTO), la probabilidad exacta y una explicación textual generada por el modelo.

---

### nlp **3. Clasificación y Asistencia de Tickets**

*   **Área:** `Soporte al Cliente & Operaciones`
*   **Tecnología:** `Procesamiento de Lenguaje Natural (NLP)`
*   **Descripción:** Este módulo automatiza la gestión de tickets de soporte o taller. Clasifica el problema en una categoría y sugiere soluciones basadas en casos históricos resueltos.
*   **Funcionamiento:**
    1.  Un modelo (`LinearSVC`) y un vectorizador de texto (`TfidfVectorizer`) se entrenan con un historial de tickets (`tickets.csv`).
    2.  El endpoint `POST /api/tickets/classify` recibe la descripción de un nuevo ticket y devuelve la categoría más probable (ej: "MECANICO", "ELECTRICO").
    3.  El endpoint `POST /api/tickets/suggest` va un paso más allá: busca en el historial los tickets más similares usando similitud de coseno y devuelve las soluciones que se aplicaron en esos casos.
    4.  El frontend agiliza drásticamente el trabajo del personal de soporte, que recibe la categoría y posibles soluciones al instante.

---

### 🌐 **4. Orquestación y Plataforma Unificada**

*   **Área:** `Plataforma & Integración`
*   **Tecnología:** `API Unificada, Frontend & Automatización`
*   **Descripción:** Este es el corazón que une todos los módulos. Consiste en la API de FastAPI, el panel web en React y los flujos de automatización.
*   **Funcionamiento:**
    *   **API Unificada:** `FastAPI` sirve como un único punto de entrada para todos los modelos de IA.
    *   **Panel Web:** Un dashboard moderno y limpio construido con `React` y `TailwindCSS` que permite a los usuarios interactuar con los modelos sin necesidad de conocimientos técnicos.
    *   **Flujos de Automatización:** Se proveen ejemplos (ver `scripts/`) para integrar la API con herramientas como `n8n` o `Zapier`, permitiendo crear flujos de trabajo automatizados (ej: "enviar una alerta si la demanda de un item supera un umbral").

---

## 🚀 **¡Empezar a Usar!**

Para explorar la suite, siga las instrucciones detalladas en nuestros manuales:

*   **Para instalar y ejecutar el proyecto:** `docs/manual_instalacion.md`
*   **Para usar cada herramienta:** `docs/manual_uso_funcional.md`
*   **Para entender la arquitectura:** `docs/arquitectura_general.md`

¡Esperamos que esta suite impulse la eficiencia y la toma de decisiones inteligentes en su organización!
