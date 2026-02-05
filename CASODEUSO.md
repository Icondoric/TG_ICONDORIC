# DIAGRAMA DE CASOS DE USO DE ALTO NIVEL

## Sistema de Intermediación Laboral con Recomendaciones basadas en Machine Learning

**Versión:** 1.0
**Fecha:** Febrero 2026
**Proyecto:** Plataforma de Intermediación Laboral Universitaria

---

## 1. DESCRIPCIÓN GENERAL DEL SISTEMA

El sistema es una **plataforma web de intermediación laboral** diseñada para conectar estudiantes y titulados universitarios con oportunidades laborales (pasantías y empleos) mediante un sistema inteligente de recomendaciones basado en Machine Learning.

### Objetivos del Sistema:
- Digitalizar perfiles profesionales de estudiantes y titulados mediante extracción automática de CVs
- Gestionar ofertas laborales de instituciones públicas y privadas
- Evaluar la correspondencia entre candidatos y ofertas usando algoritmos de ML
- Generar recomendaciones personalizadas basadas en el perfil del usuario
- Proporcionar herramientas de gestión y reportes para administradores

---

## 2. DIAGRAMA 1: ACTORES DEL SISTEMA

```mermaid
flowchart TB
    subgraph ACTORES["🎭 ACTORES DEL SISTEMA"]
        direction TB

        subgraph CANDIDATOS["👥 Usuarios Candidatos"]
            EST[("👨‍🎓 ESTUDIANTE<br/>Busca pasantías")]
            TIT[("👨‍💼 TITULADO<br/>Busca empleos")]
        end

        subgraph GESTORES["🔧 Gestores"]
            ADM[("👨‍💻 ADMINISTRADOR<br/>Control total")]
        end
    end

    EST --> |"Hereda de"| UC["Usuario Candidato"]
    TIT --> |"Hereda de"| UC

    style EST fill:#4CAF50,stroke:#2E7D32,color:#fff
    style TIT fill:#2196F3,stroke:#1565C0,color:#fff
    style ADM fill:#FF5722,stroke:#D84315,color:#fff
    style UC fill:#9E9E9E,stroke:#616161,color:#fff
```

### Descripción de Actores:

| Actor | Rol | Permisos | Restricciones |
|-------|-----|----------|---------------|
| **Estudiante** | Usuario activo universitario | Perfil, CV, Recomendaciones de **pasantías** | Sin acceso a empleos |
| **Titulado** | Egresado universitario | Perfil, CV, Recomendaciones de **empleos** | Sin acceso a pasantías |
| **Administrador** | Gestor del sistema | Acceso completo a todos los módulos | Ninguna |

---

## 3. DIAGRAMA 2: ARQUITECTURA MODULAR DEL SISTEMA

```mermaid
flowchart TB
    subgraph SISTEMA["🏢 SISTEMA DE INTERMEDIACIÓN LABORAL"]
        direction TB

        subgraph CAPA1["📱 Capa de Presentación"]
            M1["🔐 M1: AUTENTICACIÓN<br/>━━━━━━━━━━━━━━━<br/>• Registro<br/>• Login/Logout<br/>• JWT Tokens<br/>• Cambio Password"]
        end

        subgraph CAPA2["⚙️ Capa de Gestión"]
            M2["👥 M2: GESTIÓN USUARIOS<br/>━━━━━━━━━━━━━━━<br/>• CRUD Usuarios<br/>• Filtros/Búsqueda<br/>• Gestión Roles<br/>• Estado Activo"]

            M3["📄 M3: DIGITALIZACIÓN<br/>PERFILES<br/>━━━━━━━━━━━━━━━<br/>• Carga CV (PDF)<br/>• Extracción IA<br/>• Edición Manual<br/>• Completitud"]

            M4["💼 M4: GESTIÓN OFERTAS<br/>━━━━━━━━━━━━━━━<br/>• CRUD Ofertas<br/>• Tipos: Pasantía/Empleo<br/>• Estados/Vigencia<br/>• Estadísticas"]

            M5["🏛️ M5: PERFILES<br/>INSTITUCIONALES<br/>━━━━━━━━━━━━━━━<br/>• CRUD Perfiles<br/>• Pesos Evaluación<br/>• Umbrales<br/>• Requisitos"]
        end

        subgraph CAPA3["🤖 Capa de Inteligencia"]
            M6["🧠 M6: EVALUACIÓN ML<br/>━━━━━━━━━━━━━━━<br/>• Feature Engineering<br/>• Scoring Dimensiones<br/>• Ridge Regression<br/>• Clasificación"]

            M7["⭐ M7: RECOMENDACIONES<br/>━━━━━━━━━━━━━━━<br/>• Generación<br/>• Filtrado<br/>• Historial<br/>• Elegibilidad"]
        end

        subgraph CAPA4["📊 Capa de Análisis"]
            M8["📈 M8: INFORMES<br/>Y REPORTES<br/>━━━━━━━━━━━━━━━<br/>• Estadísticas<br/>• Métricas<br/>• Gráficos<br/>• Exportación"]
        end
    end

    M1 --> M2
    M1 --> M3
    M2 --> M4
    M2 --> M5
    M3 --> M6
    M4 --> M6
    M5 --> M6
    M6 --> M7
    M7 --> M8
    M4 --> M8
    M2 --> M8

    style M1 fill:#E91E63,stroke:#AD1457,color:#fff
    style M2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style M3 fill:#673AB7,stroke:#4527A0,color:#fff
    style M4 fill:#3F51B5,stroke:#283593,color:#fff
    style M5 fill:#2196F3,stroke:#1565C0,color:#fff
    style M6 fill:#00BCD4,stroke:#00838F,color:#fff
    style M7 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M8 fill:#FF9800,stroke:#EF6C00,color:#fff
```

---

## 4. DIAGRAMA 3: CASOS DE USO - VISTA GENERAL

```mermaid
flowchart LR
    subgraph ACTORES_IZQ[" "]
        EST(("👨‍🎓<br/>Estudiante"))
        TIT(("👨‍💼<br/>Titulado"))
    end

    subgraph SISTEMA["🏢 SISTEMA DE INTERMEDIACIÓN LABORAL"]
        subgraph AUTH["🔐 Autenticación"]
            UC1["Registrarse"]
            UC2["Iniciar Sesión"]
            UC3["Cambiar Contraseña"]
        end

        subgraph PERFIL["📄 Gestión Perfil"]
            UC4["Cargar CV"]
            UC5["Editar Perfil"]
            UC6["Ver Completitud"]
        end

        subgraph RECOM["⭐ Recomendaciones"]
            UC7["Obtener Recomendaciones"]
            UC8["Ver Historial"]
            UC9["Marcar como Vista"]
        end

        subgraph ADMIN_USERS["👥 Gestión Usuarios"]
            UC10["CRUD Usuarios"]
            UC11["Gestionar Roles"]
        end

        subgraph ADMIN_OFERTAS["💼 Gestión Ofertas"]
            UC12["CRUD Ofertas"]
            UC13["Activar/Desactivar"]
        end

        subgraph ADMIN_INST["🏛️ Perfiles Institucionales"]
            UC14["CRUD Perfiles"]
            UC15["Configurar Pesos"]
        end

        subgraph REPORTES["📈 Reportes"]
            UC16["Ver Dashboard"]
            UC17["Generar Informes"]
        end
    end

    subgraph ACTORES_DER[" "]
        ADM(("👨‍💻<br/>Admin"))
    end

    EST --> UC1 & UC2 & UC3
    EST --> UC4 & UC5 & UC6
    EST --> UC7 & UC8 & UC9

    TIT --> UC1 & UC2 & UC3
    TIT --> UC4 & UC5 & UC6
    TIT --> UC7 & UC8 & UC9

    ADM --> UC10 & UC11
    ADM --> UC12 & UC13
    ADM --> UC14 & UC15
    ADM --> UC16 & UC17

    style EST fill:#4CAF50,stroke:#2E7D32,color:#fff
    style TIT fill:#2196F3,stroke:#1565C0,color:#fff
    style ADM fill:#FF5722,stroke:#D84315,color:#fff
```

---

## 5. DIAGRAMA 4: CASOS DE USO - MÓDULO AUTENTICACIÓN (M1)

```mermaid
flowchart LR
    subgraph ACTORES[" "]
        EST(("👨‍🎓<br/>Estudiante"))
        TIT(("👨‍💼<br/>Titulado"))
        ADM(("👨‍💻<br/>Admin"))
    end

    subgraph M1["🔐 MÓDULO DE AUTENTICACIÓN (M1)"]
        UC1_1(["UC1.1<br/>Registrarse en el Sistema"])
        UC1_2(["UC1.2<br/>Iniciar Sesión"])
        UC1_3(["UC1.3<br/>Cerrar Sesión"])
        UC1_4(["UC1.4<br/>Cambiar Contraseña"])
        UC1_5(["UC1.5<br/>Recuperar Contraseña"])

        UC1_1 -.->|include| VAL["Validar Email Único"]
        UC1_1 -.->|include| HASH["Hash de Contraseña"]
        UC1_2 -.->|include| JWT["Generar Token JWT"]
        UC1_4 -.->|include| VER["Verificar Contraseña Actual"]
    end

    EST --> UC1_1 & UC1_2 & UC1_3 & UC1_4 & UC1_5
    TIT --> UC1_1 & UC1_2 & UC1_3 & UC1_4 & UC1_5
    ADM --> UC1_2 & UC1_3 & UC1_4

    style UC1_1 fill:#E8F5E9,stroke:#4CAF50
    style UC1_2 fill:#E8F5E9,stroke:#4CAF50
    style UC1_3 fill:#E8F5E9,stroke:#4CAF50
    style UC1_4 fill:#E8F5E9,stroke:#4CAF50
    style UC1_5 fill:#E8F5E9,stroke:#4CAF50
    style VAL fill:#FFF3E0,stroke:#FF9800
    style HASH fill:#FFF3E0,stroke:#FF9800
    style JWT fill:#FFF3E0,stroke:#FF9800
    style VER fill:#FFF3E0,stroke:#FF9800
```

### Detalle de Casos de Uso - Autenticación

| ID | Caso de Uso | Descripción | Precondición | Postcondición |
|----|-------------|-------------|--------------|---------------|
| UC1.1 | Registrarse | Crear cuenta con email, contraseña, rol | Sin cuenta previa | Cuenta creada + perfil vacío |
| UC1.2 | Iniciar Sesión | Acceder con credenciales | Cuenta activa | Token JWT generado |
| UC1.3 | Cerrar Sesión | Finalizar sesión | Sesión activa | Token invalidado |
| UC1.4 | Cambiar Contraseña | Modificar contraseña | Sesión activa | Contraseña actualizada |
| UC1.5 | Recuperar Contraseña | Restablecer acceso | Cuenta existente | Nueva contraseña |

---

## 6. DIAGRAMA 5: CASOS DE USO - DIGITALIZACIÓN DE PERFILES (M3)

```mermaid
flowchart LR
    subgraph ACTORES[" "]
        EST(("👨‍🎓<br/>Estudiante"))
        TIT(("👨‍💼<br/>Titulado"))
    end

    subgraph M3["📄 MÓDULO DIGITALIZACIÓN DE PERFILES (M3)"]
        UC3_1(["UC3.1<br/>Cargar CV en PDF"])
        UC3_2(["UC3.2<br/>Visualizar Perfil Extraído"])
        UC3_3(["UC3.3<br/>Editar Hard Skills"])
        UC3_4(["UC3.4<br/>Editar Soft Skills"])
        UC3_5(["UC3.5<br/>Editar Nivel Educativo"])
        UC3_6(["UC3.6<br/>Editar Experiencia"])
        UC3_7(["UC3.7<br/>Editar Idiomas"])
        UC3_8(["UC3.8<br/>Consultar Completitud"])

        UC3_1 -.->|include| GEMINI["🤖 Extracción con<br/>Gemini AI"]
        UC3_1 -.->|include| NORM["Normalizar Datos"]
        UC3_8 -.->|include| CALC["Calcular Score"]

        GEMINI -.->|extend| UC3_2
    end

    EST --> UC3_1 & UC3_2 & UC3_3 & UC3_4 & UC3_5 & UC3_6 & UC3_7 & UC3_8
    TIT --> UC3_1 & UC3_2 & UC3_3 & UC3_4 & UC3_5 & UC3_6 & UC3_7 & UC3_8

    style UC3_1 fill:#E3F2FD,stroke:#2196F3
    style UC3_2 fill:#E3F2FD,stroke:#2196F3
    style UC3_3 fill:#E3F2FD,stroke:#2196F3
    style UC3_4 fill:#E3F2FD,stroke:#2196F3
    style UC3_5 fill:#E3F2FD,stroke:#2196F3
    style UC3_6 fill:#E3F2FD,stroke:#2196F3
    style UC3_7 fill:#E3F2FD,stroke:#2196F3
    style UC3_8 fill:#E3F2FD,stroke:#2196F3
    style GEMINI fill:#FCE4EC,stroke:#E91E63
    style NORM fill:#FFF3E0,stroke:#FF9800
    style CALC fill:#FFF3E0,stroke:#FF9800
```

### Detalle de Casos de Uso - Digitalización

| ID | Caso de Uso | Descripción | Precondición | Postcondición |
|----|-------------|-------------|--------------|---------------|
| UC3.1 | Cargar CV | Subir PDF (máx 10MB) | Sesión activa | Datos extraídos con IA |
| UC3.2 | Visualizar Perfil | Ver datos extraídos | CV procesado | Perfil mostrado |
| UC3.3 | Editar Hard Skills | Modificar skills técnicas | Perfil existente | Skills actualizadas |
| UC3.4 | Editar Soft Skills | Modificar skills blandas | Perfil existente | Skills actualizadas |
| UC3.5 | Editar Educación | Modificar nivel educativo | Perfil existente | Educación actualizada |
| UC3.6 | Editar Experiencia | Modificar años experiencia | Perfil existente | Experiencia actualizada |
| UC3.7 | Editar Idiomas | Modificar idiomas/niveles | Perfil existente | Idiomas actualizados |
| UC3.8 | Consultar Completitud | Ver % de completitud | Perfil existente | Score mostrado |

---

## 7. DIAGRAMA 6: CASOS DE USO - ADMINISTRACIÓN

```mermaid
flowchart TB
    ADM(("👨‍💻<br/>Administrador"))

    subgraph M2["👥 GESTIÓN DE USUARIOS (M2)"]
        UC2_1(["UC2.1 Listar Usuarios"])
        UC2_2(["UC2.2 Buscar/Filtrar"])
        UC2_3(["UC2.3 Ver Detalle"])
        UC2_4(["UC2.4 Ver Perfil Usuario"])
        UC2_5(["UC2.5 Crear Usuario"])
        UC2_6(["UC2.6 Editar Usuario"])
        UC2_7(["UC2.7 Cambiar Rol"])
        UC2_8(["UC2.8 Desactivar"])
        UC2_9(["UC2.9 Eliminar"])
    end

    subgraph M4["💼 GESTIÓN DE OFERTAS (M4)"]
        UC4_1(["UC4.1 Listar Ofertas"])
        UC4_2(["UC4.2 Buscar/Filtrar"])
        UC4_3(["UC4.3 Ver Detalle"])
        UC4_4(["UC4.4 Crear Oferta"])
        UC4_5(["UC4.5 Editar Oferta"])
        UC4_6(["UC4.6 Activar"])
        UC4_7(["UC4.7 Desactivar"])
        UC4_8(["UC4.8 Eliminar"])
        UC4_9(["UC4.9 Ver Estadísticas"])
    end

    subgraph M5["🏛️ PERFILES INSTITUCIONALES (M5)"]
        UC5_1(["UC5.1 Listar Perfiles"])
        UC5_2(["UC5.2 Filtrar por Sector"])
        UC5_3(["UC5.3 Ver Detalle"])
        UC5_4(["UC5.4 Crear Perfil"])
        UC5_5(["UC5.5 Configurar Pesos"])
        UC5_6(["UC5.6 Configurar Umbrales"])
        UC5_7(["UC5.7 Definir Requisitos"])
        UC5_8(["UC5.8 Editar Perfil"])
        UC5_9(["UC5.9 Activar/Desactivar"])
        UC5_10(["UC5.10 Eliminar"])
    end

    ADM --> M2
    ADM --> M4
    ADM --> M5

    style UC2_1 fill:#F3E5F5,stroke:#9C27B0
    style UC2_5 fill:#F3E5F5,stroke:#9C27B0
    style UC2_9 fill:#FFEBEE,stroke:#F44336
    style UC4_4 fill:#E8EAF6,stroke:#3F51B5
    style UC4_7 fill:#FFEBEE,stroke:#F44336
    style UC5_4 fill:#E3F2FD,stroke:#2196F3
    style UC5_5 fill:#E0F7FA,stroke:#00BCD4
    style UC5_6 fill:#E0F7FA,stroke:#00BCD4
```

---

## 8. DIAGRAMA 7: CASOS DE USO - RECOMENDACIONES Y ML

```mermaid
flowchart TB
    subgraph ACTORES[" "]
        EST(("👨‍🎓<br/>Estudiante"))
        TIT(("👨‍💼<br/>Titulado"))
    end

    subgraph M7["⭐ MÓDULO DE RECOMENDACIONES (M7)"]
        UC7_1(["UC7.1<br/>Obtener Recomendaciones"])
        UC7_2(["UC7.2<br/>Filtrar Recomendaciones"])
        UC7_3(["UC7.3<br/>Ver Detalle Oferta"])
        UC7_4(["UC7.4<br/>Marcar como Vista"])
        UC7_5(["UC7.5<br/>Consultar Historial"])
        UC7_6(["UC7.6<br/>Ver Estadísticas Personales"])
        UC7_7(["UC7.7<br/>Verificar Elegibilidad"])
    end

    subgraph M6["🧠 MÓDULO ML (M6) - Interno"]
        direction TB
        FE["Feature Engineering<br/>━━━━━━━━━━━━━━━<br/>• Hard Skills (TF-IDF)<br/>• Soft Skills (Categorías)<br/>• Education (8 niveles)<br/>• Experience (Log)<br/>• Languages (CEFR)"]

        MODEL["Ridge Regression<br/>━━━━━━━━━━━━━━━<br/>• Input: 18 features<br/>• Output: score 0-1"]

        CLASS["Clasificación<br/>━━━━━━━━━━━━━━━<br/>• APTO ≥ 0.70<br/>• CONSIDERADO ≥ 0.50<br/>• NO_APTO < 0.50"]

        EXPL["Explicabilidad<br/>━━━━━━━━━━━━━━━<br/>• Fortalezas<br/>• Debilidades<br/>• Scores detallados"]

        FE --> MODEL --> CLASS --> EXPL
    end

    EST --> UC7_1 & UC7_2 & UC7_3 & UC7_4 & UC7_5 & UC7_6 & UC7_7
    TIT --> UC7_1 & UC7_2 & UC7_3 & UC7_4 & UC7_5 & UC7_6 & UC7_7

    UC7_1 -.->|usa| M6
    UC7_7 -.->|valida| ELIG["Perfil ≥ 70%"]

    style UC7_1 fill:#E8F5E9,stroke:#4CAF50
    style UC7_3 fill:#E8F5E9,stroke:#4CAF50
    style UC7_5 fill:#E8F5E9,stroke:#4CAF50
    style FE fill:#E0F7FA,stroke:#00BCD4
    style MODEL fill:#FCE4EC,stroke:#E91E63
    style CLASS fill:#FFF3E0,stroke:#FF9800
    style EXPL fill:#F3E5F5,stroke:#9C27B0
```

### Detalle de Casos de Uso - Recomendaciones

| ID | Caso de Uso | Descripción | Precondición | Postcondición |
|----|-------------|-------------|--------------|---------------|
| UC7.1 | Obtener Recomendaciones | Recibir ofertas ordenadas por match | Perfil ≥ 70% | Lista de recomendaciones |
| UC7.2 | Filtrar | Aplicar filtros (sector, clasificación) | Recomendaciones existentes | Resultados filtrados |
| UC7.3 | Ver Detalle | Ver oferta con scores detallados | Recomendación existente | Detalle con fortalezas/debilidades |
| UC7.4 | Marcar Vista | Actualizar estado de recomendación | Recomendación existente | fue_vista = true |
| UC7.5 | Historial | Ver todas las recomendaciones recibidas | Usuario autenticado | Historial paginado |
| UC7.6 | Estadísticas | Ver métricas personales | Usuario autenticado | Stats mostradas |
| UC7.7 | Verificar Elegibilidad | Validar requisitos para recibir recomendaciones | Usuario autenticado | Estado de elegibilidad |

---

## 9. DIAGRAMA 8: CASOS DE USO - REPORTES (M8)

```mermaid
flowchart LR
    ADM(("👨‍💻<br/>Administrador"))

    subgraph M8["📈 MÓDULO DE INFORMES Y REPORTES (M8)"]
        UC8_1(["UC8.1<br/>Ver Dashboard General"])
        UC8_2(["UC8.2<br/>Estadísticas Usuarios"])
        UC8_3(["UC8.3<br/>Distribución por Roles"])
        UC8_4(["UC8.4<br/>Métricas de Ofertas"])
        UC8_5(["UC8.5<br/>Análisis Recomendaciones"])
        UC8_6(["UC8.6<br/>Gráficos de Crecimiento"])
        UC8_7(["UC8.7<br/>Reportes por Período"])
        UC8_8(["UC8.8<br/>Exportar Datos"])

        UC8_1 -.->|include| KPIS["KPIs del Sistema"]
        UC8_3 -.->|include| PIE["Gráfico Circular"]
        UC8_6 -.->|include| LINE["Gráfico de Líneas"]
    end

    ADM --> UC8_1 & UC8_2 & UC8_3 & UC8_4 & UC8_5 & UC8_6 & UC8_7 & UC8_8

    style UC8_1 fill:#FFF3E0,stroke:#FF9800
    style UC8_2 fill:#FFF3E0,stroke:#FF9800
    style UC8_3 fill:#FFF3E0,stroke:#FF9800
    style UC8_4 fill:#FFF3E0,stroke:#FF9800
    style UC8_5 fill:#FFF3E0,stroke:#FF9800
    style UC8_6 fill:#FFF3E0,stroke:#FF9800
    style UC8_7 fill:#FFF3E0,stroke:#FF9800
    style UC8_8 fill:#FFF3E0,stroke:#FF9800
```

---

## 10. DIAGRAMA 9: FLUJO PRINCIPAL DEL SISTEMA

```mermaid
flowchart TB
    subgraph FLUJO["🔄 FLUJO PRINCIPAL DEL CANDIDATO"]
        START((Inicio))

        REG["1️⃣ REGISTRO<br/>━━━━━━━━━━━━━━━<br/>• Email, contraseña<br/>• Selección de rol<br/>• Creación perfil vacío"]

        CV["2️⃣ CARGA DE CV<br/>━━━━━━━━━━━━━━━<br/>• Subir PDF (máx 10MB)<br/>• Extracción con Gemini AI<br/>• Normalización de datos"]

        EDIT["3️⃣ COMPLETAR PERFIL<br/>━━━━━━━━━━━━━━━<br/>• Revisar datos extraídos<br/>• Editar/corregir info<br/>• Objetivo: ≥ 70%"]

        CHECK{{"4️⃣ VERIFICAR<br/>ELEGIBILIDAD<br/>¿Perfil ≥ 70%?"}}

        NO_ELIG["❌ NO ELEGIBLE<br/>━━━━━━━━━━━━━━━<br/>• Mostrar campos faltantes<br/>• Recomendaciones mejora"]

        ML["5️⃣ GENERACIÓN ML<br/>━━━━━━━━━━━━━━━<br/>• Feature Engineering (18 features)<br/>• Ridge Regression<br/>• Clasificación APTO/CONSIDERADO/NO_APTO<br/>• Identificar fortalezas/debilidades"]

        RECOM["6️⃣ RECOMENDACIONES<br/>━━━━━━━━━━━━━━━<br/>• Lista ordenada por match_score<br/>• Filtros por sector<br/>• Detalle con scores<br/>• Historial disponible"]

        END((Fin))

        START --> REG --> CV --> EDIT --> CHECK
        CHECK -->|No| NO_ELIG --> EDIT
        CHECK -->|Sí| ML --> RECOM --> END
    end

    style START fill:#4CAF50,stroke:#2E7D32,color:#fff
    style END fill:#F44336,stroke:#C62828,color:#fff
    style REG fill:#E3F2FD,stroke:#2196F3
    style CV fill:#FCE4EC,stroke:#E91E63
    style EDIT fill:#E8F5E9,stroke:#4CAF50
    style CHECK fill:#FFF3E0,stroke:#FF9800
    style NO_ELIG fill:#FFEBEE,stroke:#F44336
    style ML fill:#E0F7FA,stroke:#00BCD4
    style RECOM fill:#F3E5F5,stroke:#9C27B0
```

---

## 11. MATRIZ DE ACCESO ACTOR - MÓDULO

```mermaid
flowchart TB
    subgraph MATRIZ["📊 MATRIZ DE ACCESO"]
        direction TB

        subgraph HEADER[""]
            H1["MÓDULO"]
            H2["Estudiante"]
            H3["Titulado"]
            H4["Admin"]
        end

        subgraph R1["M1: Autenticación"]
            M1_E["✅"]
            M1_T["✅"]
            M1_A["✅"]
        end

        subgraph R2["M2: Gestión Usuarios"]
            M2_E["❌"]
            M2_T["❌"]
            M2_A["✅"]
        end

        subgraph R3["M3: Digitalización Perfiles"]
            M3_E["✅"]
            M3_T["✅"]
            M3_A["✅"]
        end

        subgraph R4["M4: Gestión Ofertas"]
            M4_E["❌"]
            M4_T["❌"]
            M4_A["✅"]
        end

        subgraph R5["M5: Perfiles Institucionales"]
            M5_E["❌"]
            M5_T["❌"]
            M5_A["✅"]
        end

        subgraph R6["M6: Evaluación ML"]
            M6_E["🔄 Auto"]
            M6_T["🔄 Auto"]
            M6_A["🔄 Auto"]
        end

        subgraph R7["M7: Recomendaciones"]
            M7_E["✅ Pasantías"]
            M7_T["✅ Empleos"]
            M7_A["✅ Todo"]
        end

        subgraph R8["M8: Reportes"]
            M8_E["❌"]
            M8_T["❌"]
            M8_A["✅"]
        end
    end

    style M1_E fill:#E8F5E9,stroke:#4CAF50
    style M1_T fill:#E8F5E9,stroke:#4CAF50
    style M1_A fill:#E8F5E9,stroke:#4CAF50
    style M2_E fill:#FFEBEE,stroke:#F44336
    style M2_T fill:#FFEBEE,stroke:#F44336
    style M2_A fill:#E8F5E9,stroke:#4CAF50
    style M7_E fill:#E3F2FD,stroke:#2196F3
    style M7_T fill:#E3F2FD,stroke:#2196F3
```

### Leyenda:
| Símbolo | Significado |
|---------|-------------|
| ✅ | Acceso completo |
| ❌ | Sin acceso |
| 🔄 Auto | Módulo automático/interno |
| ✅ Pasantías | Solo recomendaciones de pasantías |
| ✅ Empleos | Solo recomendaciones de empleos |

---

## 12. MODELO ENTIDAD-RELACIÓN

```mermaid
erDiagram
    USUARIOS ||--|| PERFILES_PROFESIONALES : "tiene"
    USUARIOS ||--o{ RECOMENDACIONES : "recibe"
    OFERTAS_LABORALES ||--o{ RECOMENDACIONES : "genera"
    INSTITUTIONAL_PROFILES ||--o{ OFERTAS_LABORALES : "configura"
    USUARIOS ||--o{ OFERTAS_LABORALES : "crea"

    USUARIOS {
        uuid id PK
        string email UK
        string password_hash
        string rol "estudiante|titulado|admin"
        string nombre_completo
        timestamp created_at
    }

    PERFILES_PROFESIONALES {
        uuid id PK
        uuid usuario_id FK
        jsonb gemini_extraction
        array hard_skills
        array soft_skills
        string education_level
        numeric experience_years
        array languages
        string cv_filename
        boolean is_complete
        numeric completeness_score
        timestamp updated_at
    }

    OFERTAS_LABORALES {
        uuid id PK
        uuid institutional_profile_id FK
        uuid created_by FK
        string titulo
        text descripcion
        string tipo "pasantia|empleo"
        string modalidad
        string ubicacion
        jsonb requisitos_especificos
        boolean is_active
        date fecha_inicio
        date fecha_cierre
        integer cupos_disponibles
    }

    RECOMENDACIONES {
        uuid id PK
        uuid usuario_id FK
        uuid oferta_id FK
        numeric match_score "0-1"
        string clasificacion "APTO|CONSIDERADO|NO_APTO"
        jsonb scores_detalle
        array fortalezas
        array debilidades
        boolean fue_vista
        timestamp created_at
    }

    INSTITUTIONAL_PROFILES {
        uuid id PK
        string institution_name UK
        string sector
        text description
        jsonb weights "sum=1.0"
        jsonb requirements
        jsonb thresholds
        boolean is_active
        uuid created_by FK
    }
```

---

## 13. COMPONENTES DEL MÓDULO ML

```mermaid
flowchart TB
    subgraph ML["🧠 MÓDULO DE EVALUACIÓN ML (M6)"]
        direction TB

        subgraph INPUT["📥 ENTRADA"]
            CV_DATA["Datos del CV<br/>━━━━━━━━━━━━━━━<br/>• hard_skills[]<br/>• soft_skills[]<br/>• education_level<br/>• experience_years<br/>• languages[]"]

            REQ_DATA["Requisitos Oferta<br/>━━━━━━━━━━━━━━━<br/>• required_skills[]<br/>• preferred_skills[]<br/>• min_experience<br/>• required_education<br/>• required_languages[]"]
        end

        subgraph FE["⚙️ FEATURE ENGINEERING"]
            HS["Hard Skills Scorer<br/>━━━━━━━━━━━━━━━<br/>TF-IDF + Jaccard<br/>Match exacto: 50%<br/>Similitud: 25%<br/>Preferidos: 15%<br/>Amplitud: 10%"]

            SS["Soft Skills Scorer<br/>━━━━━━━━━━━━━━━<br/>Categorías semánticas:<br/>• Interpersonal<br/>• Cognitivo<br/>• Organizacional<br/>• Personal"]

            ED["Education Scorer<br/>━━━━━━━━━━━━━━━<br/>8 niveles bolivianos:<br/>Técnico → Doctorado<br/>Score: 0.25 - 1.00"]

            EX["Experience Scorer<br/>━━━━━━━━━━━━━━━<br/>Función logarítmica<br/>Rendimientos<br/>decrecientes"]

            LA["Languages Scorer<br/>━━━━━━━━━━━━━━━<br/>Escala CEFR:<br/>A1-C2 + Nativo<br/>Score: 0.30 - 1.00"]
        end

        subgraph EXTRACT["📊 EXTRACTOR"]
            FV["Feature Vector<br/>━━━━━━━━━━━━━━━<br/>18 features normalizados"]
        end

        subgraph MODEL["🤖 MODELO"]
            RIDGE["Ridge Regression<br/>━━━━━━━━━━━━━━━<br/>ridge_v1.joblib<br/>Input: 18 features<br/>Output: score 0-1"]
        end

        subgraph OUTPUT["📤 SALIDA"]
            RESULT["Resultado<br/>━━━━━━━━━━━━━━━<br/>• match_score<br/>• clasificación<br/>• scores_detalle<br/>• fortalezas[]<br/>• debilidades[]"]
        end

        CV_DATA --> HS & SS & ED & EX & LA
        REQ_DATA --> HS & SS & ED & EX & LA
        HS & SS & ED & EX & LA --> FV
        FV --> RIDGE
        RIDGE --> RESULT
    end

    style HS fill:#E3F2FD,stroke:#2196F3
    style SS fill:#E8F5E9,stroke:#4CAF50
    style ED fill:#FFF3E0,stroke:#FF9800
    style EX fill:#FCE4EC,stroke:#E91E63
    style LA fill:#F3E5F5,stroke:#9C27B0
    style RIDGE fill:#E0F7FA,stroke:#00BCD4
    style RESULT fill:#FFECB3,stroke:#FFC107
```

---

## 14. PERFILES INSTITUCIONALES CONFIGURADOS

```mermaid
pie showData
    title Distribución de Pesos - AGETIC
    "Hard Skills" : 40
    "Soft Skills" : 20
    "Experiencia" : 20
    "Educación" : 15
    "Idiomas" : 5
```

| Institución | Sector | Hard Skills | Soft Skills | Experiencia | Educación | Idiomas |
|-------------|--------|:-----------:|:-----------:|:-----------:|:---------:|:-------:|
| **AGETIC** | Gobierno - Tecnología | 40% | 20% | 20% | 15% | 5% |
| **Banco FIE** | Finanzas | 30% | 25% | 20% | 15% | 10% |
| **Droguería INTI** | Farmacéutico | 25% | 30% | 20% | 15% | 10% |
| **Empacar S.A.** | Manufactura | 35% | 20% | 30% | 10% | 5% |
| **MOPSV** | Gobierno | 30% | 20% | 25% | 15% | 10% |

---

## 15. ESCALAS DE EVALUACIÓN

### 15.1 Niveles Educativos (Sistema Boliviano)

```mermaid
flowchart LR
    subgraph EDUCACION["🎓 ESCALA EDUCATIVA"]
        TM["Técnico Medio<br/>0.25"] --> TS["Técnico Superior<br/>0.45"]
        TS --> LIC["Licenciatura<br/>0.75"]
        LIC --> DIP["Diplomado<br/>0.80"]
        DIP --> ESP["Especialidad<br/>0.85"]
        ESP --> MAE["Maestría<br/>0.92"]
        MAE --> DOC["Doctorado<br/>1.00"]
    end

    style TM fill:#FFEBEE,stroke:#F44336
    style TS fill:#FFF3E0,stroke:#FF9800
    style LIC fill:#E8F5E9,stroke:#4CAF50
    style DIP fill:#E3F2FD,stroke:#2196F3
    style ESP fill:#E8EAF6,stroke:#3F51B5
    style MAE fill:#EDE7F6,stroke:#673AB7
    style DOC fill:#FCE4EC,stroke:#E91E63
```

### 15.2 Niveles de Idiomas (CEFR)

```mermaid
flowchart LR
    subgraph IDIOMAS["🌐 ESCALA CEFR"]
        A1["A1<br/>0.35"] --> A2["A2<br/>0.45"]
        A2 --> B1["B1<br/>0.60"]
        B1 --> B2["B2<br/>0.75"]
        B2 --> C1["C1<br/>0.90"]
        C1 --> C2["C2<br/>0.95"]
        C2 --> NAT["Nativo<br/>1.00"]
    end

    style A1 fill:#FFEBEE,stroke:#F44336
    style A2 fill:#FFF3E0,stroke:#FF9800
    style B1 fill:#FFFDE7,stroke:#FFEB3B
    style B2 fill:#E8F5E9,stroke:#4CAF50
    style C1 fill:#E3F2FD,stroke:#2196F3
    style C2 fill:#EDE7F6,stroke:#673AB7
    style NAT fill:#FCE4EC,stroke:#E91E63
```

---

## 16. STACK TECNOLÓGICO

```mermaid
flowchart TB
    subgraph STACK["🛠️ STACK TECNOLÓGICO"]
        direction TB

        subgraph FRONT["📱 FRONTEND"]
            VUE["Vue.js 3"]
            VITE["Vite"]
            PINIA["Pinia"]
            TAILWIND["TailwindCSS"]
            ROUTER["Vue Router"]
        end

        subgraph BACK["⚙️ BACKEND"]
            FASTAPI["FastAPI"]
            PYDANTIC["Pydantic"]
            SKLEARN["scikit-learn"]
            GEMINI["Google Gemini"]
            JWT["python-jose"]
        end

        subgraph DATA["💾 BASE DE DATOS"]
            SUPABASE["Supabase<br/>(PostgreSQL)"]
            RLS["Row Level Security"]
        end

        subgraph DEPLOY["🚀 DEPLOYMENT"]
            UVICORN["Uvicorn"]
            NPM["npm dev server"]
        end

        FRONT <--> BACK
        BACK <--> DATA
        BACK --> DEPLOY
        FRONT --> DEPLOY
    end

    style VUE fill:#42B883,stroke:#35495E,color:#fff
    style FASTAPI fill:#009688,stroke:#00695C,color:#fff
    style SUPABASE fill:#3ECF8E,stroke:#2B9F6D,color:#fff
    style GEMINI fill:#4285F4,stroke:#3367D6,color:#fff
```

---

## 17. RESUMEN DE CASOS DE USO POR ACTOR

### Estudiante (12 casos de uso)
| Módulo | Casos de Uso |
|--------|--------------|
| M1 - Autenticación | UC1.1, UC1.2, UC1.3, UC1.4, UC1.5 |
| M3 - Digitalización | UC3.1, UC3.2, UC3.3, UC3.4, UC3.5, UC3.6, UC3.7, UC3.8 |
| M7 - Recomendaciones | UC7.1*, UC7.2, UC7.3, UC7.4, UC7.5, UC7.6, UC7.7 |

*Solo pasantías

### Titulado (12 casos de uso)
| Módulo | Casos de Uso |
|--------|--------------|
| M1 - Autenticación | UC1.1, UC1.2, UC1.3, UC1.4, UC1.5 |
| M3 - Digitalización | UC3.1, UC3.2, UC3.3, UC3.4, UC3.5, UC3.6, UC3.7, UC3.8 |
| M7 - Recomendaciones | UC7.1**, UC7.2, UC7.3, UC7.4, UC7.5, UC7.6, UC7.7 |

**Solo empleos

### Administrador (30+ casos de uso)
| Módulo | Casos de Uso |
|--------|--------------|
| M1 - Autenticación | UC1.2, UC1.3, UC1.4 |
| M2 - Gestión Usuarios | UC2.1 - UC2.9 |
| M3 - Digitalización | UC3.1 - UC3.8 |
| M4 - Gestión Ofertas | UC4.1 - UC4.9 |
| M5 - Perfiles Inst. | UC5.1 - UC5.11 |
| M7 - Recomendaciones | UC7.1 - UC7.7 (todos) |
| M8 - Reportes | UC8.1 - UC8.8 |

---

## 18. CONCLUSIONES

Este documento presenta el diagrama de casos de uso de alto nivel para el **Sistema de Intermediación Laboral con Recomendaciones basadas en Machine Learning**.

### Módulos Identificados (8):
1. **M1:** Autenticación
2. **M2:** Gestión de Usuarios
3. **M3:** Digitalización de Perfiles
4. **M4:** Gestión de Ofertas Laborales
5. **M5:** Perfiles Institucionales
6. **M6:** Evaluación de Correspondencia (ML)
7. **M7:** Sistema de Recomendaciones
8. **M8:** Informes y Reportes

### Roles del Sistema (3):
- **Estudiante:** Acceso a pasantías
- **Titulado:** Acceso a empleos
- **Administrador:** Control total del sistema

### Total de Casos de Uso: **50+**

---

**Documento generado para el Trabajo de Grado**
**Plataforma de Intermediación Laboral Universitaria**
**Febrero 2026**
