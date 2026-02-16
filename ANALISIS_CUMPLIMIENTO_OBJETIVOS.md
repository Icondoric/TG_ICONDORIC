# Analisis de Cumplimiento de Objetivos - TG_ICONDORIC

**Fecha de analisis:** 13 de febrero de 2026
**Proyecto:** Sistema de Evaluacion de Perfiles Profesionales con NLP y ML
**Institucion:** Escuela Militar de Ingenieria (EMI)

---

## 1. OBJETIVO GENERAL

> *"Desarrollar un sistema de evaluacion de perfiles profesionales, aplicando procesamiento de lenguaje natural y machine learning, para centralizar la informacion de estudiantes y titulados con el proposito de apoyar la toma de decisiones en la identificacion de correspondencia entre aptitudes y demandas, a fin de generar recomendaciones laborales y de pasantia en empresas e instituciones que tengan convenio con la Escuela Militar de Ingenieria."*

### Veredicto: CUMPLIDO PARCIALMENTE (85%)

| Componente del Objetivo | Estado | Evidencia |
|--------------------------|--------|-----------|
| Sistema de evaluacion de perfiles profesionales | CUMPLIDO | Modulo completo de evaluacion en `backend/app/ml/` y `frontend/src/features/evaluation/` |
| Procesamiento de lenguaje natural | CUMPLIDO | `backend/app/core/nlp.py` (spaCy) + `backend/app/core/llm_extractor.py` (Gemini) |
| Machine learning | CUMPLIDO | Ridge Regression en `backend/app/ml/models/ridge_model.py`, R2=0.7996 |
| Centralizar informacion de estudiantes y titulados | CUMPLIDO | Tabla `perfiles_profesionales` en Supabase, gestion completa de perfiles |
| Identificacion de correspondencia entre aptitudes y demandas | CUMPLIDO | Feature engineering con 18 dimensiones, scoring por dimension |
| Recomendaciones laborales y de pasantia | CUMPLIDO | `frontend/src/features/recommendations/`, endpoint `/api/recommendations` |
| Empresas e instituciones con convenio con la EMI | PARCIAL | 5 perfiles institucionales (AGETIC, Banco FIE, INTI, Empacar, MOPSV) pero **no existe un modulo de gestion de convenios como tal** |

### Brechas del Objetivo General

1. **No existe un modulo dedicado a la gestion de convenios/acuerdos** con la EMI. Los "convenios" estan implicitamente representados como perfiles institucionales y ofertas laborales, pero no hay:
   - Registro formal de convenios (fecha inicio, fecha fin, estado del convenio)
   - Documentacion de convenios asociada
   - Personas de contacto por convenio
   - Historial de relacion institucional

2. **La diferenciacion entre estudiantes y titulados** existe en roles (`estudiante`, `graduado`) pero el sistema no personaliza significativamente la experiencia segun el tipo de usuario mas alla de cambiar la palabra "pasantia" por "empleo" en la interfaz.

---

## 2. OBJETIVO ESPECIFICO 1

> *"Recopilar informacion de convenios gestionados a traves de la Escuela Militar de Ingenieria, para determinar los requerimientos funcionales y tecnicos del sistema de evaluacion de perfiles profesionales."*

### Veredicto: CUMPLIDO PARCIALMENTE (60%)

### Lo que SI se cumple:

- **5 perfiles institucionales** configurados con requerimientos detallados en `backend/app/data/profiles/`:
  - `profile_agetic.json` - AGETIC (Gobierno/Tecnologia)
  - `profile_banco_fie.json` - Banco FIE (Servicios Financieros)
  - `profile_drogueria_inti.json` - Drogueria INTI (Farmaceutico)
  - `profile_empacar.json` - Empacar S.A. (Industria/Manufactura)
  - `profile_mopsv.json` - Min. Obras Publicas (Gobierno)
- Cada perfil contiene: pesos de evaluacion, habilidades requeridas/preferidas, nivel de educacion, idiomas, umbrales de clasificacion
- Documentacion de sprints (`Documentacion_Sprints_1_3.docx`, `Documentacion_Sprints_4_6.docx`)

### Lo que NO se cumple:

| Elemento Faltante | Descripcion | Impacto |
|--------------------|-------------|---------|
| **Modulo de gestion de convenios** | No existe CRUD para convenios formales entre la EMI y las empresas/instituciones | ALTO - El objetivo habla explicitamente de "convenios gestionados" |
| **Datos reales de convenios** | Los perfiles institucionales son configuraciones tecnicas, no representan convenios formales con fechas, estados, responsables | ALTO |
| **Documento formal de requerimientos** | No existe un documento SRS (Software Requirements Specification) independiente | MEDIO - Los requerimientos estan dispersos en la documentacion de sprints |
| **Trazabilidad requisitos-implementacion** | No hay matriz de trazabilidad que vincule cada requisito con su implementacion | MEDIO |
| **Validacion de requerimientos con stakeholders** | No hay evidencia documentada de validacion de requerimientos con las instituciones convenidas | MEDIO |

---

## 3. OBJETIVO ESPECIFICO 2

> *"Disenar la arquitectura que permita la gestion de informacion de perfiles, considerando un modulo de procesamiento de lenguaje natural para la extraccion y estructuracion de informacion relevante contenida en los curriculums de titulados y estudiantes de la Escuela Militar de Ingenieria."*

### Veredicto: CUMPLIDO (90%)

### Lo que SI se cumple:

| Componente | Ubicacion | Descripcion |
|------------|-----------|-------------|
| Arquitectura de perfiles | `backend/app/api/routes/profile.py` | CRUD completo: crear, leer, actualizar, eliminar perfiles |
| Modulo NLP - spaCy | `backend/app/core/nlp.py` | NER, segmentacion de CV, extraccion de emails/telefonos/carreras |
| Modulo NLP - Gemini LLM | `backend/app/core/llm_extractor.py` | Extraccion estructurada: habilidades, educacion, experiencia, idiomas |
| Procesamiento de PDF | Dependencia `pdfplumber` | Conversion de PDF a texto para procesamiento NLP |
| Extraccion de habilidades duras | `backend/app/scoring/feature_engineering/hard_skills_scorer.py` | TF-IDF + Jaccard para matching de habilidades tecnicas |
| Extraccion de habilidades blandas | `backend/app/scoring/feature_engineering/soft_skills_scorer.py` | Matching categorico de habilidades interpersonales |
| Extraccion de educacion | `backend/app/scoring/feature_engineering/education_scorer.py` | Jerarquia: Doctorado > Maestria > Licenciatura > Tecnico > Bachillerato |
| Extraccion de experiencia | `backend/app/scoring/feature_engineering/experience_scorer.py` | Calculo de anos con modelo logaritmico |
| Extraccion de idiomas | `backend/app/scoring/feature_engineering/languages_scorer.py` | Niveles CEFR: Nativo > C2 > C1 > B2 > B1 > A2 > A1 |
| Arquitectura frontend | `frontend/src/features/profile/` | Subida de CV, visualizacion de perfil, edicion manual |
| Documentacion de arquitectura | `FASE_1-7_IMPLEMENTACION.md` | 7 documentos detallando cada fase de implementacion |
| Diagrama de arquitectura | `diagrama_ml.drawio` | Diagrama del sistema ML en formato Draw.io |

### Lo que NO se cumple:

| Elemento Faltante | Descripcion | Impacto |
|--------------------|-------------|---------|
| **Diagrama de arquitectura general del sistema** | Solo existe `diagrama_ml.drawio` para ML; falta diagrama de arquitectura completa (frontend, backend, BD, servicios externos) | MEDIO |
| **Documento de Diseno de Arquitectura (SAD)** | No existe un documento formal de arquitectura del software (vistas logica, fisica, de procesos, de desarrollo) | MEDIO - Los documentos FASE_* cubren parcialmente esto |
| **Diagrama de despliegue** | No hay documentacion de como se despliega el sistema en produccion | BAJO |

---

## 4. OBJETIVO ESPECIFICO 3

> *"Integrar un modelo de machine learning que permita evaluar los perfiles profesionales con los perfiles laborales de referencia, determinando el nivel de correspondencia entre ambos."*

### Veredicto: CUMPLIDO (95%)

### Lo que SI se cumple:

| Componente | Ubicacion | Detalle |
|------------|-----------|---------|
| Modelo ML | `backend/app/ml/models/ridge_model.py` | Ridge Regression (L2), alpha=0.01 |
| Entrenamiento | `backend/app/ml/models/model_trainer.py` | Train/test split, cross-validation, grid search |
| Modelo entrenado | `backend/app/ml/trained_models/ridge_v1.joblib` | Modelo serializado listo para produccion |
| Feature Engineering | `backend/app/scoring/feature_engineering/` | 18 dimensiones (5 scores + 5 pesos + 5 interacciones + 3 contexto) |
| Prediccion | `backend/app/ml/models/predictor.py` | MatchPredictor con explicabilidad |
| Nivel de correspondencia | Clasificacion 3 niveles | APTO (>=70%), CONSIDERADO (50-70%), NO_APTO (<50%) |
| Metricas del modelo | `evaluation_report.md` | R2=0.7996, RMSE=0.0918, MAE=0.0736, Accuracy=77.1% |
| Visualizaciones | `evaluation_results/graficas/` | 8 graficos: importancia de features, confusion matrix, residuos, etc. |
| Integracion API | `backend/app/api/routes/ml_predictions.py` | Endpoints: evaluate-cv, get-recommendations, model-info |
| Integracion Frontend | `frontend/src/features/evaluation/` | Vista completa con graficos de score, resultados detallados, historial |
| Dataset sintetico | `synthetic_dataset.csv` | 5,000 ejemplos, 18 features, generado con 15 reglas expertas |

### Lo que NO se cumple:

| Elemento Faltante | Descripcion | Impacto |
|--------------------|-------------|---------|
| **Validacion con datos reales** | El modelo fue entrenado exclusivamente con datos sinteticos (5,000 ejemplos generados); no se evidencia validacion con CVs reales de estudiantes/titulados de la EMI | ALTO - Afecta la confiabilidad del modelo en produccion |
| **Reentrenamiento automatico** | No hay pipeline para reentrenar el modelo con nuevos datos reales recopilados | BAJO |
| **Comparacion con otros modelos** | Solo se implemento Ridge Regression; no se documenta comparacion sistematica con otros algoritmos (Random Forest, SVM, Gradient Boosting, etc.) para justificar la eleccion | MEDIO |

---

## 5. OBJETIVO ESPECIFICO 4 (CRITICO)

> *"Realizar la validacion integral del sistema mediante pruebas unitarias, de integracion, funcionales, de rendimiento y de usabilidad, verificando el correcto desempeno de los modulos de procesamiento de lenguaje natural y machine learning."*

### Veredicto: NO CUMPLIDO (25%)

Este es el objetivo con **mayor brecha de cumplimiento** en todo el proyecto.

### Estado Actual de Pruebas:

#### 5.1 Pruebas Unitarias - PARCIALMENTE CUMPLIDO (40%)

**Backend (7 archivos de prueba encontrados):**

| Archivo | Ubicacion | Que prueba |
|---------|-----------|------------|
| `test_pos_filtering.py` | `backend/tests/` | Filtrado POS en NLP |
| `test_user_repro.py` | `backend/tests/` | Caso de reproduccion de usuario |
| `test_nlp_improvement.py` | `backend/tests/` | Extraccion de telefonos, segmentacion CV, carreras |
| `test_feature_engineering.py` | `backend/tests/` | 5 scorers + pipeline de features |
| `test_fase4_model.py` | `backend/tests/` | Carga de modelo, prediccion, importancia de features |
| `test_fase6.py` | `backend/` | Integracion basica de modulos |
| `verify_*.py` (3 archivos) | `backend/` | Verificacion de bcrypt, Gemini, ML status |

**Problemas criticos:**
- Las pruebas son **scripts manuales** ejecutados con `python test_file.py`, no usan framework pytest
- No hay `conftest.py`, `pytest.ini`, ni fixtures compartidas
- No hay reporte de cobertura de codigo
- **CERO pruebas unitarias en el frontend** (0 archivos .test.js o .spec.js)
- No hay Vitest, Jest ni ningun framework de testing frontend configurado

#### 5.2 Pruebas de Integracion - NO CUMPLIDO (15%)

| Aspecto | Estado | Detalle |
|---------|--------|---------|
| Integracion Frontend-Backend | NO EXISTE | No hay pruebas que verifiquen la comunicacion API completa |
| Integracion NLP-ML | MINIMA | Solo `test_fase6.py` verifica imports y conexion basica |
| Integracion BD | MINIMA | Solo verifica conectividad con Supabase |
| Integracion Gemini API | NO EXISTE | `verify_gemini.py` es un script de verificacion, no una prueba de integracion |

#### 5.3 Pruebas Funcionales (E2E) - NO CUMPLIDO (0%)

| Aspecto | Estado |
|---------|--------|
| Framework E2E | NO CONFIGURADO - No existe Cypress, Playwright, ni Selenium |
| Flujos de usuario | NO PROBADOS automaticamente |
| Escenarios criticos | NO CUBIERTOS |
| Registro de usuario + login | SIN PRUEBA E2E |
| Subida de CV + procesamiento NLP | SIN PRUEBA E2E |
| Evaluacion de perfil + resultado ML | SIN PRUEBA E2E |
| Generacion de recomendaciones | SIN PRUEBA E2E |
| Gestion admin de perfiles institucionales | SIN PRUEBA E2E |

#### 5.4 Pruebas de Rendimiento - NO CUMPLIDO (0%)

| Aspecto | Estado |
|---------|--------|
| Herramienta de carga | NO CONFIGURADA - No existe Locust, k6, Artillery |
| Tiempo de respuesta API | NO MEDIDO |
| Concurrencia de usuarios | NO PROBADA |
| Rendimiento del modelo ML | NO BENCHMARKED (tiempo de inferencia) |
| Rendimiento del procesamiento NLP | NO BENCHMARKED |
| Carga de procesamiento de PDFs | NO PROBADA |
| Uso de memoria | NO MONITOREADO |

#### 5.5 Pruebas de Usabilidad - NO CUMPLIDO (0%)

| Aspecto | Estado |
|---------|--------|
| Protocolo de pruebas de usabilidad | NO EXISTE |
| Pruebas con usuarios reales | NO DOCUMENTADAS |
| Metricas SUS (System Usability Scale) | NO RECOPILADAS |
| Encuestas de satisfaccion | NO IMPLEMENTADAS |
| Analisis heuristico | NO DOCUMENTADO |
| Pruebas de accesibilidad (WCAG) | NO REALIZADAS |

#### 5.6 Infraestructura de CI/CD - NO EXISTE (0%)

| Aspecto | Estado |
|---------|--------|
| GitHub Actions | NO CONFIGURADO |
| Pipeline automatizado | NO EXISTE |
| Ejecucion automatica de pruebas | NO IMPLEMENTADA |
| Reporte de cobertura | NO CONFIGURADO |

---

## 6. RESUMEN EJECUTIVO

### Tabla de Cumplimiento General

| Objetivo | Cumplimiento | Estado |
|----------|-------------|--------|
| **General**: Sistema de evaluacion con NLP y ML | 85% | PARCIAL |
| **OE1**: Recopilar informacion de convenios | 60% | PARCIAL |
| **OE2**: Disenar arquitectura con modulo NLP | 90% | CUMPLIDO |
| **OE3**: Integrar modelo ML | 95% | CUMPLIDO |
| **OE4**: Validacion integral con pruebas | 25% | **NO CUMPLIDO** |
| **PROMEDIO PONDERADO** | **71%** | **PARCIAL** |

### Hallazgos Criticos (Requieren Atencion Inmediata)

1. **CRITICO - Objetivo Especifico 4**: La validacion integral del sistema es el objetivo con mayor brecha. Se requieren como minimo:
   - Pruebas unitarias con pytest (backend) y Vitest (frontend)
   - Pruebas de integracion para flujos NLP -> ML -> API
   - Al menos un framework E2E (Cypress o Playwright)
   - Pruebas de rendimiento basicas con Locust o k6
   - Pruebas de usabilidad con al menos 5 usuarios reales

2. **ALTO - Gestion de Convenios**: No existe modulo de gestion de convenios. Se necesita al menos una entidad/tabla `convenios` con:
   - Institucion, fecha de inicio, fecha de fin, estado, tipo de convenio
   - Relacion con perfiles institucionales y ofertas

3. **ALTO - Validacion con Datos Reales del ML**: El modelo ML fue entrenado solo con datos sinteticos. Se debe:
   - Recopilar CVs reales (anonimizados) de estudiantes/titulados
   - Validar las predicciones del modelo con casos reales
   - Documentar la precision en escenarios reales

### Elementos Bien Logrados

- Arquitectura feature-based del frontend bien estructurada
- Pipeline NLP (spaCy + Gemini) robusto y funcional
- Modelo ML con metricas documentadas y explicabilidad
- API REST completa con 40+ endpoints
- Sistema de recomendaciones personalizado por rol
- Interfaz de administracion con gestion de perfiles institucionales y ofertas
- Documentacion tecnica de implementacion por fases (7 documentos)

---

## 7. PLAN DE ACCION SUGERIDO

### Prioridad 1 - Pruebas (Objetivo Especifico 4)

1. Configurar pytest con conftest.py y fixtures
2. Escribir pruebas unitarias para todos los scorers de feature engineering
3. Escribir pruebas unitarias para el pipeline NLP
4. Configurar Vitest para el frontend
5. Escribir pruebas de componentes Vue
6. Implementar pruebas E2E con Cypress/Playwright para flujos criticos
7. Implementar pruebas de rendimiento con Locust
8. Realizar pruebas de usabilidad con usuarios reales
9. Documentar todos los resultados de pruebas

### Prioridad 2 - Gestion de Convenios (Objetivo Especifico 1)

1. Crear tabla `convenios` en Supabase
2. Crear CRUD de convenios en backend
3. Crear interfaz de administracion de convenios en frontend
4. Vincular convenios con perfiles institucionales y ofertas

### Prioridad 3 - Validacion ML con Datos Reales (Objetivo Especifico 3)

1. Recopilar CVs reales anonimizados
2. Ejecutar predicciones y comparar con evaluacion manual
3. Documentar precision real del modelo
4. Ajustar modelo si es necesario

---

*Documento generado automaticamente como parte del analisis de cumplimiento del proyecto TG_ICONDORIC.*
