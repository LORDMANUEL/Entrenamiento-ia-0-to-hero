# 📖 Manual de Instalación - AI Business Suite

Esta guía detalla los pasos necesarios para instalar, configurar y ejecutar el proyecto AI Business Suite en un entorno de desarrollo local.

## ✅ Prerrequisitos

Asegúrese de tener instalado el siguiente software:

*   **Python:** Versión 3.11 o superior.
*   **Node.js:** Versión 18.x o superior.
*   **npm:** Generalmente se instala con Node.js.
*   **Docker & Docker Compose:** (Opcional) Para una ejecución contenerizada.

---

## 🚀 Instalación y Ejecución

Siga estos pasos para poner en marcha la aplicación.

### 1. Clonar el Repositorio

Primero, clone el repositorio a su máquina local:

```bash
git clone <URL_DEL_REPOSITORIO>
cd ai-business-suite
```

### 2. Configuración del Backend (API FastAPI)

Siga estos pasos desde la raíz del proyecto (`ai-business-suite/`).

**a. Crear y Activar Entorno Virtual:**

```bash
# Navegar al directorio del backend
cd backend

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
# venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

**b. Instalar Dependencias:**

Con el entorno virtual activado, instale las librerías de Python necesarias.

```bash
pip install -r requirements.txt
```

**c. Entrenar los Modelos de Machine Learning (Paso Manual Obligatorio):**

Antes de poder usar la API, debe ejecutar los scripts de entrenamiento para generar los archivos `.pkl` de los modelos. **Este es un paso que se hace una sola vez.**

```bash
# Desde la carpeta 'backend/', y con el entorno virtual activado:
python -m models_ml.forecast.train_forecast
python -m models_ml.risk_scoring.train_risk
python -m models_ml.nlp_tickets.train_nlp
```

**d. Lanzar el Servidor FastAPI:**

Una vez instaladas las dependencias y entrenados los modelos, inicie el servidor de la API.

```bash
# Asegúrese de estar en el directorio 'backend/'
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor del backend ahora estará corriendo en `http://localhost:8000`. Puede acceder a la documentación interactiva de la API en `http://localhost:8000/docs`.

### 3. Configuración del Frontend (Dashboard React)

Abra una **nueva terminal** y siga estos pasos desde la raíz del proyecto (`ai-business-suite/`).

**a. Instalar Dependencias de Node.js:**

```bash
# Navegar al directorio del frontend
cd frontend

# Instalar los paquetes necesarios
npm install
```

**b. Lanzar el Servidor de Desarrollo:**

```bash
# Desde el directorio 'frontend/'
npm run dev
```

El servidor de desarrollo de Vite se iniciará y la aplicación web estará disponible en `http://localhost:5173`.

### 4. (Opcional) Ejecución con Docker Compose

Si prefiere una configuración más sencilla y aislada, puede usar Docker Compose para levantar tanto el backend como el frontend.

**a. Construir y Ejecutar los Contenedores:**

Desde la raíz del proyecto (`ai-business-suite/`), ejecute el siguiente comando:

```bash
docker-compose up --build
```

Esto se encargará de:
*   Construir la imagen de Docker para el backend.
*   Instalar las dependencias y ejecutar los scripts de entrenamiento dentro del contenedor.
*   Iniciar el servidor de FastAPI.
*   (Si se añade un servicio de frontend) Construir y servir la aplicación de React.

**b. Puertos Expuestos:**
*   **Backend API:** `http://localhost:8000`
*   **Frontend App:** `http://localhost:5173` (según se configure en `docker-compose.yml`)

---

¡Listo! Con estos pasos, el entorno de desarrollo de AI Business Suite estará completamente funcional.
