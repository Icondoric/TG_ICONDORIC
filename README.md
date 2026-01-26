# Plataforma de Intermediación Laboral con NLP

Sistema web de recomendación de candidatos que conecta estudiantes con ofertas laborales mediante análisis inteligente de CVs.

## Estructura del Proyecto

- `backend/`: API FastAPI con lógica de NLP (spaCy).
- `frontend/`: Aplicación Vue.js 3 + Vite + TailwindCSS.

## Requisitos Previos

- Python 3.9+
- Node.js 16+
- PostgreSQL (Supabase) - *Para Fase 2*

## Configuración e Instalación

### 1. Backend

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
4. Descarga el modelo de spaCy (español):
   ```bash
   python -m spacy download es_core_news_md
   ```
5. Inicia el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
   El backend estará corriendo en `http://localhost:8000`. Documentation API: `http://localhost:8000/docs`.

### 2. Frontend

1. Navega a la carpeta frontend:
   ```bash
   cd frontend
   ```
2. Instala las dependencias (si no se instalaron automáticamente):
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```
   El frontend estará disponible en `http://localhost:5173`.

## Uso (Fase 1)

1. Abre el frontend.
2. Selecciona un archivo PDF con un CV (preferiblemente con texto seleccionable).
3. El sistema procesará el archivo y mostrará:
   - Datos de contacto extraídos.
   - Competencias detectadas (Python, SQL, etc.).
4. Puedes editar los datos manualmente y guardar el perfil (simulado en log de consola por ahora).

## Metodología de Extracción de Competencias

Para garantizar la validez y estandarización en la detección de habilidades, este sistema utiliza una ontología basada en la clasificación **ESCO (European Skills, Competences, Qualifications and Occupations)**. 
- **Fuente de Datos**:
    1. **ESCO (v1.2)**: Subconjunto oficial de competencias y ocupaciones europeas (`skills_es.csv`, `occupations_es.csv`).
    2. **StackShare Tools**: Dataset comunitario (`tools.csv`) para cobertura de tecnologías modernas, obtenido de [captn3m0/stackshare-dataset](https://github.com/captn3m0/stackshare-dataset).
- **Técnica de Coincidencia**: Se emplea un enfoque híbrido que combina:
    1. **Coincidencia Exacta**: Para detección rápida y precisa de términos técnicos estándar.
    2. **Fuzzy Matching (Lógica Difusa)**: Para identificar variaciones léxicas o errores tipográficos leves, mejorando la robustez del sistema frente a entradas no estructuradas.

## Notas Técnicas

- La extracción de texto usa `pdfplumber`. Si el PDF es una imagen escaneada, no funcionará sin OCR (fuera del alcance actual).
- Las competencias se gestionan en un archivo JSON externo, permitiendo fácil actualización y ampliación del diccionario de habilidades sin modificar el código fuente.
