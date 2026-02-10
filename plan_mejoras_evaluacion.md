# Plan de Mejoras - Modulo de Evaluacion de Perfiles

## Resumen de Problemas Detectados

| # | Problema | Impacto | Prioridad |
|---|---------|---------|-----------|
| 1 | `EvaluationView` y `HistoryView` no usan `AppLayout` | Se ven desconectadas del sistema (sin sidebar de navegacion) | Alta |
| 2 | El modal de detalle en `HistoryView` no muestra fortalezas/debilidades | El usuario pierde informacion valiosa al revisar evaluaciones pasadas | Media |
| 3 | Falta conexion visual entre Evaluar CV, Historial y Recomendaciones | El usuario no entiende la relacion entre los 3 subflujos | Media |

---

## Cambio 1: Integrar `EvaluationView` con `AppLayout` + Sidebar

### Estado actual
- `EvaluationView.vue` es una pagina standalone (`<div class="max-w-5xl mx-auto py-8 px-4">`)
- No tiene sidebar de navegacion ni sidebar secundario
- Se siente como una pagina aislada del sistema

### Cambios propuestos

**Archivo: `frontend/src/features/evaluation/views/EvaluationView.vue`**

1. **Envolver el contenido con `<AppLayout>`** siguiendo el mismo patron de `MisRecomendacionesView.vue` y `MiPerfilView.vue`:

```html
<template>
  <AppLayout>
    <div class="flex">
      <!-- Secondary Sidebar -->
      <EvaluationSidebar
        v-model:isOpen="isSecondarySidebarOpen"
        :lastEvaluation="mlStore.currentEvaluation"
        :profileCount="mlStore.activeProfiles.length"
        :isEvaluating="mlStore.isEvaluating"
      />

      <!-- Main Content (contenido actual) -->
      <div
        class="flex-1 transition-[margin] duration-300 ease-in-out min-h-screen"
        :style="{ marginLeft: isSecondarySidebarOpen ? '280px' : '60px' }"
      >
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- ...contenido actual sin cambios... -->
        </div>
      </div>
    </div>
  </AppLayout>
</template>
```

2. **Imports adicionales necesarios:**
```js
import AppLayout from '@/shared/components/AppLayout.vue'
import EvaluationSidebar from '../components/EvaluationSidebar.vue'
const isSecondarySidebarOpen = ref(true)
```

**Archivo nuevo: `frontend/src/features/evaluation/components/EvaluationSidebar.vue`**

Crear sidebar secundario siguiendo el patron de `RecommendationsSidebar.vue`:

- **Contenido expandido:**
  - GaugeChart con el score de la ultima evaluacion (o 0 si no hay)
  - Clasificacion de la ultima evaluacion (badge APTO/CONSIDERADO/NO_APTO)
  - Contador de perfiles institucionales disponibles
  - Links de navegacion interna:
    - "Evaluar CV" -> `/evaluation` (activo)
    - "Mi Historial" -> `/history`
    - "Recomendaciones" -> `/mis-recomendaciones`
  - Boton "Ver Mi Perfil" -> `/digitalizacion/mi-perfil`

- **Contenido colapsado:**
  - Mini gauge con score de ultima evaluacion
  - Icono de historial
  - Icono de recomendaciones

- **Props:**
  - `isOpen` (Boolean)
  - `lastEvaluation` (Object, nullable) - ultima evaluacion realizada
  - `profileCount` (Number) - cantidad de perfiles disponibles
  - `isEvaluating` (Boolean) - si esta procesando

- **Emits:** `update:isOpen`

- **Usa:** `CollapsibleSidebar`, `GaugeChart`, `Badge` de `@/shared/components/ui/`

---

## Cambio 2: Integrar `HistoryView` con `AppLayout` + Sidebar reutilizado

### Estado actual
- `HistoryView.vue` es standalone sin sidebar
- El modal de detalle solo muestra scores por dimension, no fortalezas/debilidades

### Cambios propuestos

**Archivo: `frontend/src/features/evaluation/views/HistoryView.vue`**

1. **Envolver con `<AppLayout>` + mismo `EvaluationSidebar`** (reutilizando el sidebar del Cambio 1):

```html
<template>
  <AppLayout>
    <div class="flex">
      <EvaluationSidebar
        v-model:isOpen="isSecondarySidebarOpen"
        :lastEvaluation="selectedEvaluation"
        :profileCount="0"
        :isEvaluating="false"
      />

      <div
        class="flex-1 transition-[margin] duration-300 ease-in-out min-h-screen"
        :style="{ marginLeft: isSecondarySidebarOpen ? '280px' : '60px' }"
      >
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- ...contenido actual... -->
        </div>
      </div>
    </div>
  </AppLayout>
</template>
```

2. **Mejorar el modal de detalles** agregando fortalezas y debilidades:

En la seccion del modal `<!-- Contenido -->`, despues del bloque de "Scores por Dimension", agregar:

```html
<!-- Fortalezas y Debilidades -->
<div v-if="selectedEvaluation.top_strengths?.length || selectedEvaluation.top_weaknesses?.length"
     class="grid grid-cols-2 gap-4">
  <!-- Fortalezas -->
  <div v-if="selectedEvaluation.top_strengths?.length">
    <h4 class="font-medium text-green-700 mb-2 flex items-center">
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
      Fortalezas
    </h4>
    <ul class="space-y-1">
      <li v-for="(s, i) in selectedEvaluation.top_strengths" :key="i" class="text-sm text-slate-600 flex items-start">
        <span class="text-green-500 mr-1">+</span> {{ s }}
      </li>
    </ul>
  </div>
  <!-- Areas de Mejora -->
  <div v-if="selectedEvaluation.top_weaknesses?.length">
    <h4 class="font-medium text-red-700 mb-2 flex items-center">
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      Areas de Mejora
    </h4>
    <ul class="space-y-1">
      <li v-for="(w, i) in selectedEvaluation.top_weaknesses" :key="i" class="text-sm text-slate-600 flex items-start">
        <span class="text-red-500 mr-1">-</span> {{ w }}
      </li>
    </ul>
  </div>
</div>
```

3. **Imports adicionales:**
```js
import AppLayout from '@/shared/components/AppLayout.vue'
import EvaluationSidebar from '../components/EvaluationSidebar.vue'
const isSecondarySidebarOpen = ref(true)
```

---

## Cambio 3: Navegacion interna entre los 3 subflujos

### Estado actual
- No hay forma visual de navegar entre Evaluar CV, Historial y Recomendaciones desde dentro de cada vista
- El usuario depende del sidebar principal de navegacion

### Cambios propuestos

El `EvaluationSidebar` (creado en Cambio 1) ya incluye links de navegacion interna entre los 3 subflujos. Esto resuelve el problema de conexion visual porque:

- Desde **Evaluar CV** (`/evaluation`): sidebar muestra links a Historial y Recomendaciones
- Desde **Historial** (`/history`): sidebar muestra links a Evaluar CV y Recomendaciones
- Desde **Recomendaciones** (`/mis-recomendaciones`): ya tiene su propio sidebar (RecommendationsSidebar) con link a "Ver Mi Perfil"

Para que el sidebar sepa cual pagina esta activa, usara `useRoute()` y resaltara el link actual.

---

## Resumen de archivos a crear/modificar

| Archivo | Accion | Descripcion |
|---------|--------|-------------|
| `features/evaluation/components/EvaluationSidebar.vue` | **CREAR** | Sidebar secundario con gauge, links de navegacion interna, estadisticas |
| `features/evaluation/views/EvaluationView.vue` | MODIFICAR | Envolver con `AppLayout` + `EvaluationSidebar` |
| `features/evaluation/views/HistoryView.vue` | MODIFICAR | Envolver con `AppLayout` + `EvaluationSidebar` + agregar fortalezas/debilidades al modal |

## Archivos que NO se tocan

- `RecommendationsSidebar.vue` - ya funciona bien
- `MisRecomendacionesView.vue` - ya tiene layout correcto
- `navigation.js` - la estructura de menu esta bien
- Componentes de `shared/components/ui/` - solo se reutilizan
- Backend - no hay cambios en API

## Dependencias y componentes reutilizados

El `EvaluationSidebar.vue` reutiliza:
- `CollapsibleSidebar` de `@/shared/components/ui/CollapsibleSidebar.vue`
- `GaugeChart` de `@/shared/components/ui/GaugeChart.vue`
- `Badge` de `@/shared/components/ui/Badge.vue`
- `useUiStore` de `@/shared/stores/ui` (para leftOffset del sidebar principal)

## Orden de implementacion

1. Crear `EvaluationSidebar.vue` (es dependencia de los otros dos)
2. Modificar `EvaluationView.vue` (envolver con AppLayout + sidebar)
3. Modificar `HistoryView.vue` (envolver con AppLayout + sidebar + mejorar modal)
4. Verificar build con `npm run build`
