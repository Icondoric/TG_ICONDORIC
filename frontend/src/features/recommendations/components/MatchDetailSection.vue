<template>
  <div class="space-y-5">

    <!-- Rechazo por pre-filtro de elegibilidad -->
    <div
      v-if="props.matchDetails?.eligibility_reason"
      class="p-4 bg-danger-50 border border-danger-200 rounded-xl flex items-start gap-3"
    >
      <svg class="w-5 h-5 text-danger-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M18.364 5.636l-12.728 12.728M5.636 5.636l12.728 12.728" />
      </svg>
      <div>
        <p class="text-sm font-semibold text-danger-800">No cumples los requisitos de elegibilidad</p>
        <p class="text-sm text-danger-700 mt-0.5">{{ props.matchDetails.eligibility_reason }}</p>
        <p class="text-xs text-danger-500 mt-1">No fue posible evaluar tu compatibilidad con esta oferta.</p>
      </div>
    </div>

    <template v-if="!props.matchDetails?.eligibility_reason">

      <!-- ── Competencias Técnicas ── -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <h5 class="text-sm font-semibold text-emi-navy-800">Competencias Técnicas</h5>
          <span v-if="hardTotal > 0" class="text-xs text-gray-500">
            {{ hardMatchedCount }} de {{ hardTotal }} cumplidas
          </span>
        </div>

        <div v-if="hardTotal > 0" class="mb-3">
          <div class="w-full bg-gray-100 rounded-full h-2">
            <div class="h-2 rounded-full transition-all duration-500"
              :class="hardCoverageColor"
              :style="{ width: hardCoveragePercent + '%' }"/>
          </div>
          <p class="text-xs mt-1" :class="hardCoverageTextColor">
            Tienes el {{ hardCoveragePercent }}% de las competencias técnicas requeridas
          </p>
        </div>

        <div v-if="hardRequired.length > 0" class="mb-2">
          <span class="text-xs text-gray-400 block mb-1.5">Habilidades requeridas por la oferta:</span>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="skill in hardRequired"
              :key="skill.name"
              :class="[
                'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium',
                skill.matched
                  ? 'bg-success-100 text-success-700'
                  : 'bg-danger-100 text-danger-700'
              ]"
            >
              <svg class="h-3 w-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="skill.matched" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              {{ skill.name }}
            </span>
          </div>
        </div>

        <div v-if="preferredMatched.length > 0" class="mb-2">
          <span class="text-xs text-gray-400 block mb-1.5">Habilidades deseables que ya tienes:</span>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="skill in preferredMatched"
              :key="skill"
              class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-emi-navy-100 text-emi-navy-700"
            >
              <svg class="h-3 w-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              {{ skill }}
            </span>
          </div>
        </div>

        <p v-if="hardRequired.length === 0 && preferredMatched.length === 0"
          class="text-sm text-gray-400 italic">
          Esta oferta no especificó competencias técnicas requeridas.
        </p>
      </div>

      <!-- ── Habilidades Blandas ── -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <h5 class="text-sm font-semibold text-emi-navy-800">Habilidades Blandas</h5>
          <span v-if="softTotal > 0" class="text-xs text-gray-500">
            {{ softMatchedCount }} de {{ softTotal }} cumplidas
          </span>
        </div>

        <div v-if="softTotal > 0" class="mb-3">
          <div class="w-full bg-gray-100 rounded-full h-2">
            <div class="h-2 rounded-full transition-all duration-500"
              :class="softCoverageColor"
              :style="{ width: softCoveragePercent + '%' }"/>
          </div>
          <p class="text-xs mt-1" :class="softCoverageTextColor">
            Tienes el {{ softCoveragePercent }}% de las habilidades blandas requeridas
          </p>
        </div>

        <div v-if="softRequired.length > 0">
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="skill in softRequired"
              :key="skill.name"
              :class="[
                'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium',
                skill.matched
                  ? 'bg-success-100 text-success-700'
                  : 'bg-danger-100 text-danger-700'
              ]"
            >
              <svg class="h-3 w-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="skill.matched" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              {{ skill.name }}
            </span>
          </div>
        </div>

        <p v-if="softRequired.length === 0" class="text-sm text-gray-400 italic">
          Esta oferta no especificó habilidades blandas requeridas.
        </p>
      </div>

      <!-- ── Idiomas ── -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <h5 class="text-sm font-semibold text-emi-navy-800">Idiomas</h5>
          <span v-if="langTotal > 0" class="text-xs text-gray-500">
            {{ langMatchedCount }} de {{ langTotal }} requeridos
          </span>
        </div>

        <div v-if="langTotal > 0" class="mb-3">
          <div class="w-full bg-gray-100 rounded-full h-2">
            <div class="h-2 rounded-full transition-all duration-500"
              :class="langCoverageColor"
              :style="{ width: langCoveragePercent + '%' }"/>
          </div>
          <p class="text-xs mt-1" :class="langCoverageTextColor">
            Dominas el {{ langCoveragePercent }}% de los idiomas solicitados
          </p>
        </div>

        <div v-if="langRequired.length > 0" class="mb-2">
          <span class="text-xs text-gray-400 block mb-1.5">Idiomas requeridos:</span>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="lang in langRequired"
              :key="lang.name"
              :class="[
                'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium',
                lang.matched
                  ? 'bg-success-100 text-success-700'
                  : 'bg-danger-100 text-danger-700'
              ]"
            >
              <svg class="h-3 w-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="lang.matched" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              {{ lang.name }}
            </span>
          </div>
        </div>

        <div v-if="extraLangs.length > 0" class="mb-2">
          <span class="text-xs text-gray-400 block mb-1.5">Idiomas adicionales que tienes (no requeridos):</span>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="lang in extraLangs"
              :key="lang"
              class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emi-navy-50 text-emi-navy-600"
            >
              {{ lang }}
            </span>
          </div>
        </div>

        <p v-if="langRequired.length === 0 && extraLangs.length === 0"
          class="text-sm text-gray-400 italic">
          Esta oferta no requiere idiomas específicos.
        </p>
      </div>

      <!-- ── Otras habilidades del CV ── -->
      <div v-if="extraHardSkills.length > 0">
        <h5 class="text-sm font-semibold text-emi-navy-800 mb-2">Otras habilidades que tienes</h5>
        <p class="text-xs text-gray-400 mb-2">Habilidades de tu CV que no fueron exigidas pero suman valor:</p>
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="skill in extraHardSkills"
            :key="skill"
            class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emi-navy-50 text-emi-navy-600 border border-emi-navy-100"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <!-- Mensaje contextual según clasificación -->
      <div v-if="contextMessage" class="p-3 rounded-xl text-sm" :class="contextMessageStyle">
        {{ contextMessage }}
      </div>

    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  matchDetails: { type: Object, default: null },
  clasificacion: { type: String, default: '' }
})

// ── Hard skills ───────────────────────────────────────────
const hardRequired = computed(() => {
  if (!props.matchDetails?.hard_skills) return []
  const matched = (props.matchDetails.hard_skills.matched || []).map(s => ({ name: s, matched: true }))
  const missing = (props.matchDetails.hard_skills.missing || []).map(s => ({ name: s, matched: false }))
  return [...matched, ...missing]
})
const preferredMatched = computed(() => props.matchDetails?.hard_skills?.preferred_matched || [])
const hardMatchedCount = computed(() => (props.matchDetails?.hard_skills?.matched || []).length)
const hardTotal        = computed(() => hardMatchedCount.value + (props.matchDetails?.hard_skills?.missing || []).length)
const hardCoveragePercent = computed(() =>
  hardTotal.value === 0 ? 0 : Math.round((hardMatchedCount.value / hardTotal.value) * 100)
)
const hardCoverageColor = computed(() => {
  if (hardCoveragePercent.value >= 70) return 'bg-success-500'
  if (hardCoveragePercent.value >= 40) return 'bg-warning-500'
  return 'bg-danger-500'
})
const hardCoverageTextColor = computed(() => {
  if (hardCoveragePercent.value >= 70) return 'text-success-600'
  if (hardCoveragePercent.value >= 40) return 'text-warning-600'
  return 'text-danger-600'
})

// ── Soft skills ───────────────────────────────────────────
const softRequired = computed(() => {
  if (!props.matchDetails?.soft_skills) return []
  const matched = (props.matchDetails.soft_skills.matched || []).map(s => ({ name: s, matched: true }))
  const missing = (props.matchDetails.soft_skills.missing || []).map(s => ({ name: s, matched: false }))
  return [...matched, ...missing]
})
const softMatchedCount = computed(() => (props.matchDetails?.soft_skills?.matched || []).length)
const softTotal        = computed(() => softMatchedCount.value + (props.matchDetails?.soft_skills?.missing || []).length)
const softCoveragePercent = computed(() =>
  softTotal.value === 0 ? 0 : Math.round((softMatchedCount.value / softTotal.value) * 100)
)
const softCoverageColor = computed(() => {
  if (softCoveragePercent.value >= 70) return 'bg-success-500'
  if (softCoveragePercent.value >= 40) return 'bg-warning-500'
  return 'bg-danger-500'
})
const softCoverageTextColor = computed(() => {
  if (softCoveragePercent.value >= 70) return 'text-success-600'
  if (softCoveragePercent.value >= 40) return 'text-warning-600'
  return 'text-danger-600'
})

// ── Idiomas ───────────────────────────────────────────────
const langRequired = computed(() => {
  if (!props.matchDetails?.languages) return []
  const matched = (props.matchDetails.languages.matched || []).map(l => ({ name: l, matched: true }))
  const missing = (props.matchDetails.languages.missing || []).map(l => ({ name: l, matched: false }))
  return [...matched, ...missing]
})
const langMatchedCount = computed(() => (props.matchDetails?.languages?.matched || []).length)
const langTotal        = computed(() =>
  langMatchedCount.value + (props.matchDetails?.languages?.missing || []).length
)
const langCoveragePercent = computed(() =>
  langTotal.value === 0 ? 0 : Math.round((langMatchedCount.value / langTotal.value) * 100)
)
const langCoverageColor = computed(() => {
  if (langCoveragePercent.value >= 70) return 'bg-success-500'
  if (langCoveragePercent.value >= 40) return 'bg-warning-500'
  return 'bg-danger-500'
})
const langCoverageTextColor = computed(() => {
  if (langCoveragePercent.value >= 70) return 'text-success-600'
  if (langCoveragePercent.value >= 40) return 'text-warning-600'
  return 'text-danger-600'
})

const extraLangs = computed(() => {
  if (!props.matchDetails?.languages) return []
  const cvLangs = props.matchDetails.languages.cv_languages || []
  const required = new Set([
    ...(props.matchDetails.languages.matched || []).map(l => l.toLowerCase()),
    ...(props.matchDetails.languages.missing || []).map(l => l.toLowerCase())
  ])
  return cvLangs.filter(l => {
    const lower = l.toLowerCase()
    return ![...required].some(r => lower.includes(r) || r.includes(lower))
  })
})

// ── Habilidades extra del CV ──────────────────────────────
const extraHardSkills = computed(() => {
  if (!props.matchDetails) return []
  const cvHard  = props.matchDetails.cv_skills?.hard || []
  const matched = new Set((props.matchDetails.hard_skills?.matched || []).map(s => s.toLowerCase()))
  const missing = new Set((props.matchDetails.hard_skills?.missing || []).map(s => s.toLowerCase()))
  const preferred = new Set((props.matchDetails.hard_skills?.preferred_matched || []).map(s => s.toLowerCase()))
  const required  = new Set((props.matchDetails.required_skills?.hard || []).map(s => s.toLowerCase()))
  const known = new Set([...matched, ...missing, ...preferred, ...required])
  return cvHard.filter(s => !known.has(s.toLowerCase())).slice(0, 8)
})

// ── Mensaje contextual ────────────────────────────────────
const contextMessage = computed(() => {
  if (props.matchDetails?.eligibility_reason) return null
  switch (props.clasificacion) {
    case 'APTO':
      return 'Tus competencias se alinean bien con lo que busca esta oferta. ¡Eres un candidato fuerte!'
    case 'CONSIDERADO':
      return 'Tu perfil tiene potencial para esta oferta. Reforzar las áreas marcadas en rojo aumentaría tus posibilidades.'
    default:
      return 'Tu perfil aún no cubre los requisitos principales. Revisa las competencias faltantes para mejorar tu compatibilidad.'
  }
})

const contextMessageStyle = computed(() => {
  switch (props.clasificacion) {
    case 'APTO':       return 'bg-success-50 text-success-800 border border-success-200'
    case 'CONSIDERADO': return 'bg-warning-50 text-warning-800 border border-warning-200'
    default:           return 'bg-danger-50 text-danger-800 border border-danger-200'
  }
})
</script>
