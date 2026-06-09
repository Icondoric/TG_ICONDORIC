# Sistema de Evaluación de Perfiles Profesionales (TG ICONDORIC)

Sistema de Evaluación de Perfiles Profesionales Aplicando PLN y ML

## Características Principales

- **Extracción de Datos de CVs**: Utiliza Google Gemini API y `pdfplumber` para extraer de manera inteligente y estructurada información clave de CVs en formato PDF.
- **Evaluación de Candidatos**: Predicción de idoneidad utilizando un modelo **Ridge Regression** entrenado con datos sintéticos, clasificando a los candidatos como APTO, CONSIDERADO o NO APTO según los umbrales configurados por cada institución.
- **Sistema de Recomendaciones**: Motor de recomendación que encuentra las instituciones que mejor se adaptan al perfil del candidato.
- **Panel Administrativo**: Gestión de perfiles institucionales, permitiendo configurar de manera dinámica los pesos de las dimensiones (hard skills, soft skills, educación, experiencia) y requisitos específicos.
- **Historial de Evaluaciones**: Seguimiento de las evaluaciones realizadas por los usuarios y reportes generados.

## Estructura del Proyecto

El proyecto está dividido en dos partes principales:

- `backend/`: API REST desarrollada con **FastAPI**. Contiene toda la lógica de integración con Supabase, procesamiento NLP (spaCy), llamadas a Gemini, y la integración de modelos de ML (`scikit-learn`).
- `frontend/`: Aplicación de cliente desarrollada con **Vue.js 3**, **Vite**, **Pinia** (manejo de estado) y **TailwindCSS**.

## Requisitos Previos

- Python 3.9+
- Node.js 16+
- Base de datos PostgreSQL en [Supabase](https://supabase.com/)
- API Key de [Google Gemini](https://ai.google.dev/)

## Configuración e Instalación

### 1. Configuración del Backend

1. Navega a la carpeta backend:
   ```bash
   cd backend
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate # Linux/Mac
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Descarga el modelo de procesamiento de lenguaje natural de spaCy (español):
   ```bash
   python -m spacy download es_core_news_sm
   ```
5. Configura las variables de entorno. Crea un archivo `.env` en la carpeta `backend` con las siguientes variables:
   ```env
   SUPABASE_URL=tu_supabase_url
   SUPABASE_KEY=tu_supabase_anon_key
   GEMINI_API_KEY=tu_gemini_api_key
   SECRET_KEY=clave_secreta_para_jwt
   ```
6. Inicia el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
   El backend estará corriendo en `http://localhost:8000`. La documentación de la API está en `http://localhost:8000/docs`.

### 2. Configuración del Frontend

1. Navega a la carpeta frontend:
   ```bash
   cd frontend
   ```
2. Instala las dependencias:
   ```bash
   npm install
   ```
3. Configura las variables de entorno. Crea un archivo `.env` en `frontend/`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
4. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```
   El frontend estará disponible en `http://localhost:5173`.

## Arquitectura y Flujo de Datos (ML)

El sistema procesa los CVs en el siguiente orden:

1. **Recepción y Procesamiento del PDF**: El usuario sube un PDF desde el frontend, el cual se parsea utilizando `pdfplumber`.
2. **Extracción LLM**: El contenido del CV se envía a **Gemini**, que estructura la información en formato JSON siguiendo un esquema Pydantic predefinido.
3. **Generación de Features (Ingeniería de Características)**: Se calculan puntuaciones (`scores`) parciales para:
   - Educación (basado en niveles ISCED).
   - Experiencia (meses y relevancia).
   - Habilidades Técnicas (Hard Skills) y Blandas (Soft Skills) comparadas contra el perfil de la institución.
   - Idiomas (niveles A1 a C2).
4. **Predicción con Modelo Ridge**: El vector de características se normaliza (`StandardScaler`) y evalúa en un modelo **Ridge Regression** pre-entrenado que genera un *Score Final*.
5. **Clasificación**: Según el *Score Final* y los umbrales de la institución, se clasifica al candidato y el frontend muestra los resultados de manera visual a través de barras de progreso, gráficos y tarjetas de recomendación.
