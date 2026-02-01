# Propuesta de Reestructuración del Sistema de Recomendaciones

## 1. Resumen Ejecutivo

Este documento propone una reestructuración del sistema de recomendación laboral para la Unidad de Vinculación de la EMI. El objetivo es optimizar el flujo de trabajo para que los usuarios (estudiantes y titulados) puedan **subir su CV una sola vez**, tener sus competencias extraídas y guardadas de forma persistente, y recibir recomendaciones personalizadas de pasantías o empleos según su perfil.

### Alcance del Sistema (Explícito)

> **IMPORTANTE:** El sistema se limita a la **generación de recomendaciones de correspondencia** entre perfiles de candidatos y ofertas institucionales.
>
> **NO gestiona:**
> - Postulaciones formales
> - Procesos de selección
> - Entrevistas
> - Contratación final
>
> Estos procesos dependen exclusivamente de las empresas/instituciones y de los procedimientos establecidos por la **Unidad de Vinculación de la EMI**.

---

## 2. Análisis del Estado Actual

### 2.1 Lo que Ya Existe

| Componente | Estado | Observaciones |
|------------|--------|---------------|
| Autenticación (JWT) | ✅ Implementado | Login/Register funcional |
| 3 Roles (estudiante, titulado, admin) | ✅ Definidos | En tabla `usuarios` |
| Extracción CV con Gemini | ✅ Funcional | Endpoint `/api/upload-cv` |
| Feature Engineering (5 scorers) | ✅ Implementado | Hard/Soft skills, Edu, Exp, Lang |
| Modelo ML (Ridge Regression) | ✅ Entrenado | `ridge_v1.joblib` |
| Perfiles Institucionales | ✅ CRUD Admin | En Supabase |
| Historial de Evaluaciones | ✅ Parcial | Solo guarda evaluaciones, no perfil |

### 2.2 Problema Identificado

**Flujo Actual:**
```
Usuario sube CV → Gemini extrae → Se evalúa → Se descarta la extracción
↓
(Próxima vez) Usuario sube CV de nuevo → Gemini extrae de nuevo → ...
```

**Problema:** Las competencias extraídas NO se guardan de forma persistente en el perfil del usuario. Cada evaluación requiere re-subir el CV y re-procesar con Gemini.

---

## 3. Propuesta de Arquitectura Mejorada

### 3.1 Nuevo Flujo de Usuario

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FLUJO PROPUESTO                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────┐    ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │ Usuario  │───>│ Sube CV     │───>│ Gemini       │───>│ Guardar      │  │
│   │ Registra │    │ (PDF)       │    │ Extrae       │    │ Competencias │  │
│   └──────────┘    └─────────────┘    └──────────────┘    │ en Perfil    │  │
│                                                          └──────┬───────┘  │
│                                                                 │          │
│                                                                 ▼          │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                    PERFIL PROFESIONAL PERSISTENTE                    │ │
│   │  ┌─────────────┬─────────────┬──────────────┬───────────────────┐   │ │
│   │  │ Hard Skills │ Soft Skills │ Educación    │ Experiencia       │   │ │
│   │  │ Python      │ Liderazgo   │ Licenciatura │ 2 años desarrollo │   │ │
│   │  │ React       │ Trabajo eq. │ EMI          │                   │   │ │
│   │  └─────────────┴─────────────┴──────────────┴───────────────────┘   │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
│                                       │                                    │
│                                       ▼                                    │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                    SISTEMA DE RECOMENDACIÓN                          │ │
│   │                                                                       │ │
│   │  Perfil Usuario + Ofertas Activas → ML → Ranking de Recomendaciones  │ │
│   │                                                                       │ │
│   │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │ │
│   │  │ 1. AGETIC      │  │ 2. Banco FIE   │  │ 3. MOPSV       │         │ │
│   │  │ Match: 85%     │  │ Match: 72%     │  │ Match: 68%     │         │ │
│   │  │ APTO           │  │ APTO           │  │ CONSIDERADO    │         │ │
│   │  └────────────────┘  └────────────────┘  └────────────────┘         │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Diferenciación por Rol

| Aspecto | ESTUDIANTE | TITULADO | ADMINISTRADOR |
|---------|------------|----------|---------------|
| Subir CV | ✅ | ✅ | ❌ |
| Ver perfil propio | ✅ | ✅ | ❌ |
| Editar perfil manual | ✅ (limitado) | ✅ | ❌ |
| Ver recomendaciones | ✅ Pasantías | ✅ Empleos | ❌ |
| Historial evaluaciones | ✅ Propio | ✅ Propio | ✅ Todos |
| Gestionar ofertas | ❌ | ❌ | ✅ |
| Gestionar perfiles inst. | ❌ | ❌ | ✅ |
| Ver estadísticas | ❌ | ❌ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |

---

## 4. Cambios Propuestos en Base de Datos

### 4.1 Modificar Tabla `perfiles_profesionales`

**Actual:**
```sql
CREATE TABLE perfiles_profesionales (
    id UUID PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios(id),
    data JSONB DEFAULT '{}'::jsonb,  -- Casi vacío
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Propuesto:**
```sql
CREATE TABLE perfiles_profesionales (
    id UUID PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios(id) UNIQUE,

    -- Datos extraídos de Gemini (persistentes)
    gemini_extraction JSONB DEFAULT '{}'::jsonb,

    -- Campos normalizados para búsqueda
    hard_skills TEXT[] DEFAULT '{}',
    soft_skills TEXT[] DEFAULT '{}',
    education_level TEXT,  -- 'Tecnico', 'Licenciatura', 'Maestria', 'Doctorado'
    experience_years NUMERIC(4,2) DEFAULT 0,
    languages TEXT[] DEFAULT '{}',

    -- Metadatos del CV
    cv_filename TEXT,
    cv_uploaded_at TIMESTAMP,
    cv_file_url TEXT,  -- Opcional: almacenar PDF en storage

    -- Estado del perfil
    is_complete BOOLEAN DEFAULT FALSE,
    completeness_score NUMERIC(3,2) DEFAULT 0,  -- 0.00 - 1.00

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para búsqueda eficiente
CREATE INDEX idx_perfiles_hard_skills ON perfiles_profesionales USING GIN(hard_skills);
CREATE INDEX idx_perfiles_soft_skills ON perfiles_profesionales USING GIN(soft_skills);
CREATE INDEX idx_perfiles_education ON perfiles_profesionales(education_level);
CREATE INDEX idx_perfiles_experience ON perfiles_profesionales(experience_years);
```

### 4.2 Nueva Tabla `ofertas_laborales`

```sql
CREATE TABLE ofertas_laborales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Relación con perfil institucional
    institutional_profile_id UUID REFERENCES institutional_profiles(id),

    -- Información de la oferta
    titulo TEXT NOT NULL,
    descripcion TEXT,
    tipo TEXT NOT NULL,  -- 'pasantia' o 'empleo'
    modalidad TEXT,  -- 'presencial', 'remoto', 'hibrido'
    ubicacion TEXT,

    -- Requisitos específicos (pueden diferir del perfil institucional base)
    requisitos_especificos JSONB DEFAULT '{}'::jsonb,

    -- Estado y vigencia
    is_active BOOLEAN DEFAULT TRUE,
    fecha_inicio DATE,
    fecha_cierre DATE,
    cupos_disponibles INTEGER DEFAULT 1,

    -- Auditoría
    created_by UUID REFERENCES usuarios(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ofertas_tipo ON ofertas_laborales(tipo);
CREATE INDEX idx_ofertas_active ON ofertas_laborales(is_active);
CREATE INDEX idx_ofertas_fecha ON ofertas_laborales(fecha_cierre);
```

### 4.3 Tabla `recomendaciones` (Historial)

```sql
CREATE TABLE recomendaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    usuario_id UUID REFERENCES usuarios(id),
    oferta_id UUID REFERENCES ofertas_laborales(id),

    -- Resultado de la evaluación
    match_score NUMERIC(4,3),  -- 0.000 - 1.000
    clasificacion TEXT,  -- 'APTO', 'CONSIDERADO', 'NO_APTO'

    -- Detalle de scores
    scores_detalle JSONB,
    fortalezas TEXT[],
    debilidades TEXT[],

    -- Estado
    fue_vista BOOLEAN DEFAULT FALSE,
    vista_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_recomendaciones_usuario ON recomendaciones(usuario_id);
CREATE INDEX idx_recomendaciones_oferta ON recomendaciones(oferta_id);
CREATE INDEX idx_recomendaciones_score ON recomendaciones(match_score DESC);
```

---

## 5. Cambios Propuestos en Backend

### 5.1 Nuevos Endpoints

#### 5.1.1 Gestión de Perfil del Usuario

```
POST /api/profile/upload-cv
├── Auth: Requerido (estudiante, titulado)
├── Input: PDF file
├── Proceso:
│   ├── Extraer con Gemini
│   ├── Guardar en perfiles_profesionales
│   └── Calcular completeness_score
└── Output: Perfil actualizado

GET /api/profile/me
├── Auth: Requerido
└── Output: Perfil completo del usuario

PUT /api/profile/me
├── Auth: Requerido
├── Input: Campos a actualizar (edición manual)
└── Output: Perfil actualizado

GET /api/profile/completeness
├── Auth: Requerido
└── Output: Score de completitud + campos faltantes
```

#### 5.1.2 Recomendaciones Basadas en Perfil Guardado

```
GET /api/recommendations
├── Auth: Requerido
├── Query:
│   ├── tipo: 'pasantia' | 'empleo' | 'all'
│   ├── top_n: int (default 10)
│   └── sector: string (opcional)
├── Proceso:
│   ├── Cargar perfil del usuario (ya guardado)
│   ├── Cargar ofertas activas (filtradas por tipo según rol)
│   ├── Evaluar contra cada oferta
│   └── Ordenar por match_score
└── Output: Lista de recomendaciones

GET /api/recommendations/history
├── Auth: Requerido
└── Output: Historial de recomendaciones vistas

POST /api/recommendations/{id}/mark-viewed
├── Auth: Requerido
└── Output: Actualiza fue_vista = true
```

#### 5.1.3 Gestión de Ofertas (Admin)

```
GET /api/admin/ofertas
├── Auth: Admin
├── Query: tipo, is_active, sector, fecha_desde, fecha_hasta
└── Output: Lista de ofertas

POST /api/admin/ofertas
├── Auth: Admin
├── Input: OfertaCreate
└── Output: Oferta creada

PUT /api/admin/ofertas/{id}
├── Auth: Admin
└── Output: Oferta actualizada

DELETE /api/admin/ofertas/{id}
├── Auth: Admin
└── Output: Soft delete (is_active = false)

GET /api/admin/estadisticas/ofertas
├── Auth: Admin
└── Output: Estadísticas de ofertas y matches
```

#### 5.1.4 Dashboard Admin

```
GET /api/admin/dashboard
├── Auth: Admin
└── Output:
    ├── total_usuarios (por rol)
    ├── total_ofertas (por tipo y estado)
    ├── total_recomendaciones_generadas
    ├── promedio_match_scores
    └── distribución_por_sector

GET /api/admin/usuarios
├── Auth: Admin
├── Query: rol, has_profile, search
└── Output: Lista de usuarios con estado de perfil

GET /api/admin/usuarios/{id}/perfil
├── Auth: Admin
└── Output: Perfil completo de un usuario
```

### 5.2 Nuevos Servicios

```python
# services/profile_service.py
class ProfileService:
    def update_profile_from_cv(user_id: UUID, gemini_output: dict)
    def calculate_completeness(profile: dict) -> float
    def get_user_profile(user_id: UUID) -> dict
    def update_profile_manual(user_id: UUID, updates: dict)

# services/recommendation_service.py
class RecommendationService:
    def get_recommendations_for_user(user_id: UUID, tipo: str, top_n: int)
    def evaluate_against_oferta(profile: dict, oferta: dict) -> EvaluationResult
    def save_recommendation(user_id: UUID, oferta_id: UUID, result: dict)
    def get_recommendation_history(user_id: UUID)

# services/oferta_service.py
class OfertaService:
    def create_oferta(data: OfertaCreate, created_by: UUID)
    def update_oferta(oferta_id: UUID, data: OfertaUpdate)
    def get_active_ofertas(tipo: str, sector: str) -> List[Oferta]
    def deactivate_expired_ofertas()  # Cron job
```

---

## 6. Cambios Propuestos en Frontend

### 6.1 Nuevas Vistas

| Vista | Ruta | Rol | Descripción |
|-------|------|-----|-------------|
| **MiPerfilView** | `/mi-perfil` | Est/Tit | Ver y editar perfil propio |
| **SubirCVView** | `/subir-cv` | Est/Tit | Subir CV y ver extracción |
| **MisRecomendacionesView** | `/mis-recomendaciones` | Est/Tit | Ver recomendaciones personalizadas |
| **OfertasAdminView** | `/admin/ofertas` | Admin | CRUD de ofertas |
| **OfertaFormView** | `/admin/ofertas/new` | Admin | Crear/editar oferta |
| **UsuariosAdminView** | `/admin/usuarios` | Admin | Gestión de usuarios |
| **EstadisticasView** | `/admin/estadisticas` | Admin | Dashboard con métricas |

### 6.2 Flujo de Usuario (Estudiante/Titulado)

```
1. REGISTRO
   └─> Redirige a /subir-cv (perfil vacío)

2. SUBIR CV
   ├─> Upload PDF
   ├─> Mostrar progreso extracción Gemini
   ├─> Mostrar datos extraídos para revisión
   ├─> Usuario confirma/edita
   └─> Guardar en perfil

3. MI PERFIL
   ├─> Ver competencias guardadas
   ├─> Score de completitud (barra de progreso)
   ├─> Editar manualmente si es necesario
   └─> Re-subir CV si hay cambios

4. MIS RECOMENDACIONES
   ├─> Automáticamente filtrado por rol:
   │   ├─> Estudiante: Solo pasantías
   │   └─> Titulado: Solo empleos
   ├─> Lista ordenada por match score
   ├─> Cada recomendación muestra:
   │   ├─> Institución + Logo
   │   ├─> Título de la oferta
   │   ├─> Match score (badge: APTO/CONSIDERADO)
   │   ├─> Fortaleza principal
   │   └─> Debilidad principal
   └─> Click expande detalles
       ├─> Descripción completa
       ├─> Requisitos
       ├─> Modalidad/Ubicación
       └─> Nota: "Para postular, contacta a la Unidad de Vinculación"
```

### 6.3 Flujo de Administrador

```
1. DASHBOARD ADMIN
   ├─> Métricas generales
   │   ├─> Usuarios por rol (gráfico torta)
   │   ├─> Ofertas activas vs expiradas
   │   ├─> Promedio match scores
   │   └─> Top instituciones con más matches
   └─> Accesos rápidos

2. GESTIÓN DE OFERTAS
   ├─> Tabla de ofertas
   │   ├─> Filtros: tipo, estado, sector, fecha
   │   ├─> Búsqueda
   │   └─> Acciones: Ver, Editar, Desactivar
   └─> Crear nueva oferta
       ├─> Seleccionar perfil institucional base
       ├─> Definir título, descripción
       ├─> Tipo: pasantía/empleo
       ├─> Fechas de vigencia
       └─> Requisitos específicos (opcional)

3. GESTIÓN DE USUARIOS
   ├─> Lista de usuarios
   │   ├─> Filtros: rol, tiene perfil completo
   │   └─> Búsqueda
   └─> Ver perfil de usuario
       ├─> Datos del CV extraído
       ├─> Historial de recomendaciones
       └─> NO puede editar perfil del usuario

4. PERFILES INSTITUCIONALES (Ya existe)
   └─> CRUD de perfiles base
```

---

## 7. Componentes UI Nuevos

### 7.1 Componentes de Perfil

```
PerfilCompletenessBar.vue
├── Props: score (0-100), missingFields[]
├── Visual: Barra de progreso con porcentaje
└── Tooltip con campos faltantes

CompetenciasGrid.vue
├── Props: hardSkills[], softSkills[]
├── Visual: Grid de badges/chips
└── Colores por categoría

EducacionCard.vue
├── Props: education[]
└── Visual: Timeline vertical

ExperienciaCard.vue
├── Props: experience[]
└── Visual: Timeline con duración calculada
```

### 7.2 Componentes de Recomendaciones

```
RecomendacionCard.vue
├── Props: recomendacion
├── Visual: Card con score badge, institución, fortalezas
└── Expandible para más detalles

RecomendacionesLista.vue
├── Props: recomendaciones[]
├── Visual: Lista scrolleable de RecomendacionCard
└── Empty state si no hay recomendaciones

MatchScoreBadge.vue
├── Props: score, clasificacion
└── Visual: Badge colorizado (verde/amarillo/rojo)
```

### 7.3 Componentes Admin

```
OfertaForm.vue
├── Props: oferta (opcional para edición)
├── Campos: título, descripción, tipo, fechas, etc.
└── Selector de perfil institucional base

EstadisticasCards.vue
├── Props: stats
└── Visual: Grid de cards con números y gráficos

UsuariosTable.vue
├── Props: usuarios[], filters
├── Visual: Tabla con paginación
└── Columnas: email, rol, perfil completo, acciones
```

---

## 8. Lógica de Negocio Clave

### 8.1 Filtrado de Recomendaciones por Rol

```python
def get_ofertas_for_user(user: User) -> List[Oferta]:
    if user.rol == 'estudiante':
        return get_active_ofertas(tipo='pasantia')
    elif user.rol == 'titulado':
        return get_active_ofertas(tipo='empleo')
    else:
        return []  # Admin no recibe recomendaciones
```

### 8.2 Cálculo de Completitud del Perfil

```python
def calculate_completeness(profile: dict) -> float:
    weights = {
        'hard_skills': 0.25,      # 25%
        'soft_skills': 0.15,      # 15%
        'education': 0.20,        # 20%
        'experience': 0.25,       # 25%
        'languages': 0.10,        # 10%
        'personal_summary': 0.05  # 5%
    }

    score = 0.0
    if profile.hard_skills and len(profile.hard_skills) >= 3:
        score += weights['hard_skills']
    if profile.soft_skills and len(profile.soft_skills) >= 2:
        score += weights['soft_skills']
    if profile.education and len(profile.education) >= 1:
        score += weights['education']
    if profile.experience_years > 0:
        score += weights['experience']
    if profile.languages and len(profile.languages) >= 1:
        score += weights['languages']
    if profile.gemini_extraction.get('personal_info', {}).get('summary'):
        score += weights['personal_summary']

    return score
```

### 8.3 Re-evaluación Automática

```python
# Cuando se actualiza el perfil del usuario
async def on_profile_update(user_id: UUID):
    # Invalidar recomendaciones anteriores
    await invalidate_user_recommendations(user_id)

    # Opcional: Re-calcular en background
    # await recalculate_recommendations.delay(user_id)
```

---

## 9. Plan de Implementación

### Fase 1: Base de Datos y Modelos (Backend)
- [ ] Actualizar tabla `perfiles_profesionales`
- [ ] Crear tabla `ofertas_laborales`
- [ ] Crear tabla `recomendaciones`
- [ ] Crear schemas Pydantic para nuevas entidades
- [ ] Migrar datos existentes (si aplica)

### Fase 2: Servicios de Perfil (Backend)
- [ ] Implementar `ProfileService`
- [ ] Endpoint `POST /api/profile/upload-cv` (guarda en perfil)
- [ ] Endpoint `GET /api/profile/me`
- [ ] Endpoint `PUT /api/profile/me`
- [ ] Lógica de completeness

### Fase 3: Sistema de Ofertas (Backend)
- [ ] Implementar `OfertaService`
- [ ] CRUD endpoints `/api/admin/ofertas`
- [ ] Validaciones y reglas de negocio

### Fase 4: Recomendaciones Mejoradas (Backend)
- [ ] Implementar `RecommendationService`
- [ ] Endpoint `GET /api/recommendations` (basado en perfil guardado)
- [ ] Filtrado por tipo según rol
- [ ] Historial de recomendaciones

### Fase 5: Dashboard Admin (Backend + Frontend)
- [ ] Endpoints de estadísticas
- [ ] Vista `AdminDashboardView` mejorada
- [ ] Gráficos y métricas

### Fase 6: Vistas de Usuario (Frontend)
- [ ] Vista `MiPerfilView`
- [ ] Vista `SubirCVView` mejorada
- [ ] Vista `MisRecomendacionesView`
- [ ] Componentes de UI

### Fase 7: Gestión Admin (Frontend)
- [ ] Vista `OfertasAdminView`
- [ ] Vista `UsuariosAdminView`
- [ ] Vista `EstadisticasView`

### Fase 8: Testing e Integración
- [ ] Tests unitarios backend
- [ ] Tests de integración
- [ ] Tests E2E frontend
- [ ] Pruebas de carga

---

## 10. Consideraciones Adicionales

### 10.1 Seguridad
- Los usuarios solo pueden ver/editar su propio perfil
- Admin puede ver perfiles pero NO editarlos
- JWT con expiración y refresh tokens
- Rate limiting en endpoints de Gemini

### 10.2 Privacidad
- CVs no se almacenan permanentemente (solo datos extraídos)
- Opción para usuario de eliminar su perfil
- Logs de acceso para auditoría

### 10.3 Performance
- Cache de perfiles institucionales
- Índices en arrays de skills
- Paginación en todas las listas
- Background jobs para re-evaluaciones masivas

### 10.4 UX
- Feedback visual durante extracción de CV
- Mensajes claros sobre alcance del sistema
- Indicadores de progreso en perfil
- Notificaciones cuando hay nuevas recomendaciones

---

## 11. Diagrama de Arquitectura Final

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Vue.js)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   Auth Views    │  │  User Views     │  │  Admin Views    │             │
│  │ Login/Register  │  │ MiPerfil        │  │ Dashboard       │             │
│  └────────┬────────┘  │ SubirCV         │  │ Ofertas         │             │
│           │           │ Recomendaciones │  │ Usuarios        │             │
│           │           └────────┬────────┘  │ Estadísticas    │             │
│           │                    │           └────────┬────────┘             │
│           └────────────────────┼────────────────────┘                      │
│                                ▼                                            │
│                    ┌───────────────────────┐                               │
│                    │   Pinia Stores        │                               │
│                    │ auth.js │ ml.js       │                               │
│                    └───────────┬───────────┘                               │
│                                │                                            │
└────────────────────────────────┼────────────────────────────────────────────┘
                                 │ HTTP/REST
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             BACKEND (FastAPI)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           API Layer                                  │   │
│  │  /api/auth  │  /api/profile  │  /api/recommendations  │  /api/admin │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────┼───────────────────────────────────┐   │
│  │                          Services Layer                              │   │
│  │  AuthService │ ProfileService │ RecommendationService │ OfertaService│  │
│  └─────────────────────────────────┼───────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────┼───────────────────────────────────┐   │
│  │                           ML Layer                                   │   │
│  │  ┌───────────────┐  ┌────────────────┐  ┌───────────────────────┐   │   │
│  │  │ Gemini API    │  │ Feature Eng.   │  │ Ridge Regression      │   │   │
│  │  │ (Extracción)  │  │ (5 Scorers)    │  │ (Predicción)          │   │   │
│  │  └───────────────┘  └────────────────┘  └───────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SUPABASE (PostgreSQL)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐  ┌─────────────────────┐  ┌─────────────────────────┐    │
│  │   usuarios   │  │ perfiles_profesion. │  │ institutional_profiles  │    │
│  │   (auth)     │◄─┤ (CV extraído)       │  │ (perfiles empresa)      │    │
│  └──────────────┘  └─────────────────────┘  └─────────────────────────┘    │
│         │                    │                          │                   │
│         │                    ▼                          ▼                   │
│         │          ┌─────────────────────┐  ┌─────────────────────────┐    │
│         └─────────►│   recomendaciones   │◄─┤   ofertas_laborales     │    │
│                    │   (historial)       │  │   (pasantías/empleos)   │    │
│                    └─────────────────────┘  └─────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Conclusión

Esta reestructuración permitirá:

1. **Mejor experiencia de usuario**: Subir CV una sola vez y recibir recomendaciones continuas
2. **Diferenciación clara por rol**: Estudiantes ven pasantías, titulados ven empleos
3. **Gestión administrativa completa**: Control sobre ofertas, usuarios y estadísticas
4. **Alcance claro**: Solo recomendaciones, sin gestionar procesos de selección
5. **Escalabilidad**: Arquitectura preparada para crecer

El sistema seguirá respetando que **la gestión de postulaciones, selección y contratación** es responsabilidad exclusiva de las empresas y la Unidad de Vinculación de la EMI.

---

*Documento generado para el proyecto ATG - Sistema de Recomendación Laboral EMI*
