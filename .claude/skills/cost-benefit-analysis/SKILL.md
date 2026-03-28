---
name: cost-benefit-analysis
description: "Generate a complete Cost-Benefit Analysis (Análisis Costo-Beneficio) chapter for a software project as a professional Word document (.docx). Use this skill whenever the user asks for a cost-benefit analysis, 'análisis costo-beneficio', 'ACB', 'relación costo-beneficio', 'RCB', 'COCOMO', cost estimation for a thesis/project, or any request to produce an economic feasibility chapter for a 'Trabajo de Grado', 'tesis', or software project. Also trigger when the user mentions calculating development costs with COCOMO II, hardware/software cost tables, tangible/intangible benefits, or cost-benefit ratio. This skill produces a structured .docx document following Bolivian academic standards with all formulas, tables, and calculations included."
---

# Cost-Benefit Analysis Document Generator

## Overview

This skill generates a professional Chapter 4 (or equivalent) "Análisis Costo-Beneficio" Word document for software projects, following the standard academic structure used in Bolivian universities for Trabajo de Grado. The output is a `.docx` file with proper formatting, tables, formulas, and calculations.

## When to Use

- User asks for a cost-benefit analysis for a software project
- User needs a "Capítulo de Análisis Costo-Beneficio" for a thesis
- User wants COCOMO II estimation in a document
- User needs hardware/software cost tables + benefit analysis + RCB calculation

## Required Information

Before generating the document, gather the following from the user. Ask concisely — group related questions together.

### Mandatory Inputs

1. **Project Name & Description**: What the software does, who it serves
2. **Hardware List**: Equipment needed (servers, laptops, peripherals) with specs and costs in Bs.
3. **Software List**: Licenses, services, subscriptions with costs and periodicity
4. **Lines of Code Estimate** (or let COCOMO estimate from project scope):
   - By language (e.g., Python: 24,500 LOC, JavaScript: 102,800 LOC)
   - Or total KLOC
5. **COCOMO Mode**: Orgánico / Semi-Acoplado / Regido (default: Semi-Acoplado)
6. **Salary**: Monthly salary for developers (default: Bs. 2,750 — salario mínimo nacional Bolivia)
7. **Variable Costs**: Internet, electricity, printing, binding, etc.
8. **Tangible Benefits**: Measurable savings the system provides (time reduction, cost savings, etc.) with amounts
9. **Intangible Benefits**: Non-quantifiable improvements (user satisfaction, institutional image, etc.)

### Optional Inputs

- **Number of chapter** (default: 4)
- **Currency** (default: Bs. — Bolivianos)
- **Cost adjustment factors (FAE)** for COCOMO II (default: 1.0 or user-specified)
- **Pilot group size** for benefit calculations (default: 100)
- **Custom table numbering start** (default: auto-numbered)

## Document Structure

The generated document follows this exact structure:

```
CAPÍTULO [N]: ANÁLISIS COSTO-BENEFICIO
├── [N].1. DETERMINACIÓN DE COSTOS
│   ├── [N].1.1. Costos
│   │   ├── [N].1.1.1. Costos Fijos
│   │   │   ├── Costos de Hardware (Table)
│   │   │   ├── Costos de Software (Table)
│   │   │   └── Desarrollo del Sistema (COCOMO II calculations)
│   │   ├── [N].1.1.2. Costos Variables (Table)
│   │   └── [N].1.1.3. Costos Totales (Summary Table)
├── [N].2. ESTIMACIÓN DE BENEFICIOS
│   ├── [N].2.1. Beneficios Intangibles (bullet list)
│   └── [N].2.2. Beneficios Tangibles
│       ├── Subcategory 1 (with calculations)
│       ├── Subcategory 2 (with calculations)
│       ├── ...
│       └── Beneficios Totales (Summary Table)
└── [N].3. RELACIÓN COSTO-BENEFICIO
    └── RCB calculation + interpretation
```

## COCOMO II Formulas

Read `references/cocomo.md` for the complete COCOMO II formula reference before generating calculations. The key formulas are:

### Coefficients Table

| Modo | a | b | c | d |
|------|-----|------|------|------|
| Orgánico | 2.40 | 1.05 | 2.50 | 0.38 |
| Semi-Acoplado | 3.00 | 1.12 | 2.50 | 0.35 |
| Regido | 3.50 | 1.20 | 2.50 | 0.32 |

### Calculation Sequence

1. **Esfuerzo Nominal** = a × (KLOC)^b [persona/mes]
2. **Esfuerzo Estimado** = Esfuerzo Nominal × FAE [persona/mes]
3. **Tiempo de Desarrollo** = c × (Esfuerzo Estimado)^d [meses]
4. **Número de Personas** = Esfuerzo Estimado / Tiempo
5. **Costo Total Desarrollo** = Personas × Salario × Tiempo [Bs.]

### Cost-Benefit Ratio

```
RCB = Beneficios Totales / Costos Totales
```

- **RCB > 1**: Project is profitable and sustainable
- **RCB = 1**: Break-even
- **RCB < 1**: Project is not economically viable

## Generation Steps

### Step 1: Read the docx skill and references

```
1. Read /mnt/skills/public/docx/SKILL.md for docx creation patterns
2. Read references/cocomo.md for formula details
```

### Step 2: Collect inputs

Ask the user for the mandatory inputs listed above. If they provide a partial set, ask for the missing ones. Accept reasonable defaults where noted.

### Step 3: Perform calculations

Run all COCOMO II calculations and benefit estimations BEFORE writing the document. Store results in variables to ensure consistency across the document.

### Step 4: Generate the .docx

Use `docx-js` (npm `docx` package) following the docx skill patterns. Key formatting rules:

- **Page size**: Letter (12240 × 15840 DXA) with 1-inch margins
- **Font**: Arial, 12pt body, headings sized appropriately
- **Tables**: Full-width (9360 DXA), with header row shading (#D5E8F0), borders (#CCCCCC)
- **Formulas**: Rendered as styled paragraphs with variable names in italics
- **Nota paragraphs**: Below each table, italic, smaller font
- **Numbering**: Consistent chapter/section numbering throughout
- **Language**: Spanish (Bolivia) — all text, labels, and notes in Spanish

### Step 5: Validate and deliver

```bash
python /mnt/skills/public/docx/scripts/office/validate.py output.docx
```

## Table Formatting Standards

All tables in the document must follow this pattern:

```javascript
// Header row: shaded background, bold white text
new TableRow({
  tableHeader: true,
  children: [
    new TableCell({
      shading: { fill: "2E4057", type: ShadingType.CLEAR },
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "HEADER", bold: true, color: "FFFFFF", font: "Arial", size: 20 })]
      })]
    })
  ]
})

// Data rows: alternating white / light gray
// Total row: bold, slightly darker background
```

## Formula Display Standards

Mathematical formulas should be displayed as centered, styled paragraphs:

```javascript
// Formula name (bold, centered)
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 100 },
  children: [new TextRun({ text: "ECUACIÓN ESFUERZO NOMINAL", bold: true, font: "Arial", size: 22 })]
})

// Formula expression (centered, italicized variables)
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [
    new TextRun({ text: "Esfuerzo", italics: true, font: "Arial", size: 22 }),
    new TextRun({ text: " = a × (KLOC)", font: "Arial", size: 22 }),
    new TextRun({ text: "b", superScript: true, font: "Arial", size: 22 }),
    new TextRun({ text: " [persona/mes]", font: "Arial", size: 22 }),
  ]
})
```

## Important Notes

- All monetary values must be formatted with Bolivian convention: `Bs. 37.025,00` (dot for thousands, comma for decimals)
- The "Nota:" paragraph after each table must reference "Fuente: Elaboración propia, [year]"
- COCOMO II calculations should show step-by-step substitution of values
- The document should include a brief interpretive paragraph after each major calculation
- Round personnel count DOWN to nearest integer
- Round time UP to nearest integer month

## File Output

Save the final document to `/mnt/user-data/outputs/analisis_costo_beneficio.docx` and present it to the user.
