# COCOMO II Formula Reference

## Overview

COCOMO II (COnstructive COst MOdel II) is a mathematical model for estimating software development effort, time, and cost. This reference covers the simplified (early design) version commonly used in Bolivian academic Trabajo de Grado projects.

## Project Classification

| Classification | KLOC Range | Description |
|---|---|---|
| Orgánico | < 50 KLOC | Small teams, familiar environment, flexible requirements |
| Semi-Acoplado | 50–300 KLOC | Medium teams, mixed experience, moderate constraints |
| Regido (Empotrado) | > 300 KLOC | Large teams, tight constraints, real-time or embedded systems |

**Selection guidance**: Most academic thesis projects with web applications use **Semi-Acoplado** due to mixed technology stacks (frontend + backend + DB) and moderate complexity.

## Coefficient Table

| Modo | a | b | c | d |
|------|------|------|------|------|
| Orgánico | 2.40 | 1.05 | 2.50 | 0.38 |
| Semi-Acoplado | 3.00 | 1.12 | 2.50 | 0.35 |
| Regido | 3.50 | 1.20 | 2.50 | 0.32 |

**Source**: Gómez, C., López, Migani & Otazú, 2020

## Step-by-Step Calculation

### Step 1: Count Lines of Code

Break down by language/component:

```
| Lenguaje                          | Líneas | KLOC  |
|-----------------------------------|--------|-------|
| Python (backend, Flask, ML)       | 24,500 | 24.5  |
| JavaScript (React + frontend)     | 102,800| 102.8 |
| HTML/CSS (Tailwind)               | 8,600  | 8.6   |
| SQL/Firebase config               | 10,300 | 10.3  |
| Otros (config, JSON, utils)       | 63,900 | 63.9  |
| TOTAL                             | 210,100| 210.1 |
```

Convert total lines to KLOC: `KLOC = Total Lines / 1000`

### Step 2: Esfuerzo Nominal

```
Esfuerzo = a × (KLOC)^b [persona/mes]
```

Where:
- **Esfuerzo**: Person-months needed for the project
- **KLOC**: Thousands of lines of code
- **a, b**: Mode-dependent coefficients from the table above

**Example (Semi-Acoplado, 210.1 KLOC)**:
```
Esfuerzo = 3.0 × (210.1)^1.12 = 1197.82 persona/mes
```

### Step 3: Cost Drivers (Conductores de Coste) and FAE

The Factor de Ajuste del Esfuerzo (FAE) is the product of all selected cost driver multipliers.

#### Cost Driver Table

| Conductor de Coste | Muy Bajo | Bajo | Nominal | Alto | Muy Alto | Extra Alto |
|---|---|---|---|---|---|---|
| Fiabilidad requerida del software | 0.75 | 0.88 | 1.00 | 1.15 | 1.40 | — |
| Tamaño de la base de datos | — | 0.94 | 1.00 | 1.08 | 1.16 | — |
| Complejidad del producto | 0.70 | 0.85 | 1.00 | 1.15 | 1.30 | 1.65 |
| Restricciones del tiempo de ejecución | — | — | 1.00 | 1.11 | 1.30 | 1.66 |
| Restricciones del almacenamiento principal | — | — | 1.00 | 1.06 | 1.21 | 1.56 |
| Volatilidad de la máquina virtual | — | 0.87 | 1.00 | 1.15 | 1.30 | — |
| Tiempo de respuesta del ordenador | — | 0.87 | 1.00 | 1.07 | 1.17 | — |
| Capacidad del analista | 1.46 | 1.19 | 1.00 | 0.86 | 0.71 | — |
| Experiencia en la aplicación | 1.29 | 1.13 | 1.00 | 0.91 | 0.82 | — |
| Capacidad de los programadores | 1.42 | 1.17 | 1.00 | 0.86 | 0.70 | — |
| Experiencia en el Sistema Operativo utilizado | 1.21 | 1.10 | 1.00 | 0.90 | — | — |
| Experiencia en el lenguaje de programación | 1.14 | 1.07 | 1.00 | 0.95 | — | — |
| Prácticas de programación modernas | 1.24 | 1.10 | 1.00 | 0.91 | 0.82 | — |
| Utilización de herramientas de software | 1.24 | 1.10 | 1.00 | 0.91 | 0.83 | — |
| Limitaciones de planificación del proyecto | 1.23 | 1.08 | 1.00 | 1.04 | 1.10 | — |

**Calculating FAE**: Multiply all selected values together.

```
FAE = Π(selected_driver_values)
```

**Example**: If you select Nominal for most and a few specific values:
```
FAE = 1.00 × 0.94 × 1.15 × 1.00 × ... = 1.361
```

### Step 4: Esfuerzo Estimado

```
Esfuerzo Estimado = Esfuerzo Nominal × FAE [persona/mes]
```

**Example**:
```
Esfuerzo Estimado = 11.97 × 1.361 = 16.291 persona/mes
```

### Step 5: Tiempo de Desarrollo

```
Tiempo = c × (Esfuerzo Estimado)^d [meses]
```

**Example (Semi-Acoplado)**:
```
Tiempo = 2.50 × (16.29)^0.35 = 6.63 ≈ 6 meses
```

**Rounding rule**: Round time to nearest integer (typically down for academic projects).

### Step 6: Número de Personas

```
CostoH = Esfuerzo Estimado / Tiempo [personas]
```

**Example**:
```
CostoH = 16.291 / 6 = 2.71 ≈ 2 personas
```

**Rounding rule**: Round DOWN to nearest integer.

### Step 7: Costo Total de Desarrollo

```
CostoT = CostoH × Salario × Tiempo [Bs.]
```

Where:
- **Salario**: Monthly salary (default: Bs. 2,750 — salario mínimo nacional Bolivia 2025)

**Example**:
```
CostoT = 2 × 2,750 × 6 = Bs. 33,000
```

## Cost Summary Structure

```
| Categoría       | Subcategoría          | Monto (Bs.)  |
|-----------------|-----------------------|---------------|
| Costos Fijos    | Hardware              | XX,XXX        |
|                 | Software              | XX,XXX        |
|                 | Desarrollo del Sistema| XX,XXX        |
| Costos Variables| Material y servicio   | XX,XXX        |
| TOTAL           |                       | XX,XXX        |
```

## Benefit Categories

### Intangible Benefits
Non-quantifiable improvements. Present as bullet points describing qualitative improvements:
- Improved patient/user experience
- Enhanced institutional image
- Better decision-making support
- Training and knowledge transfer
- Innovation positioning

### Tangible Benefits
Quantifiable savings. Each subcategory needs:
1. **Base cost** of the activity being optimized
2. **Estimated reduction percentage** from the system
3. **Per-unit savings** calculation
4. **Pilot group extrapolation** (e.g., 100 users)
5. **Annual projection**

```
Savings per user/month = Base Cost × Reduction %
Monthly savings (pilot) = Savings per user × Pilot Size
Annual savings = Monthly savings × 12
```

### Benefits Summary Table

```
| Descripción                              | Beneficio (Bs.) |
|------------------------------------------|-----------------|
| Reducción de tiempos de control          | XX,XXX          |
| Asignación eficaz de recursos            | XX,XXX          |
| Minimización de costos operativos        | XX,XXX          |
| TOTAL                                    | XX,XXX          |
```

## Cost-Benefit Ratio (RCB)

```
RCB = Beneficios Totales / Costos Totales
```

### Interpretation

| RCB Value | Interpretation |
|-----------|----------------|
| RCB > 1 | El proyecto es rentable y sostenible. Los beneficios superan los costos. |
| RCB = 1 | Punto de equilibrio. Los beneficios igualan exactamente los costos. |
| RCB < 1 | El proyecto no es económicamente viable en estos términos. |

### Standard Conclusion Paragraph

> Una RCB de [X.XX] significa que los beneficios anuales del sistema superan los costos de inversión, lo que indica que el proyecto es rentable y sostenible. Se concluye que el sistema es rentable y viable en el contexto de [institución].

## Formatting Notes for Document Generation

### Number Formatting (Bolivian Convention)
- Thousands separator: dot (.)
- Decimal separator: comma (,)
- Currency prefix: Bs.
- Example: `Bs. 37.025,00`

### Table Notes
Every table must be followed by a "Nota:" paragraph:
```
Nota: [Brief description of what the table shows]. Fuente: Elaboración propia, [year]
```

### Formula Display
- Formula name: bold, centered, ALL CAPS
- Formula expression: centered, variables in italics
- "Donde:" section: bullet list defining each variable
- Substitution: show actual values replacing variables
- Result: bold

### Academic Citation for COCOMO II
```
Fuente: Gómez, C., López, Migani & Otazú, 2020
```
