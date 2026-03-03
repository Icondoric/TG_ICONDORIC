<template>
  <div class="space-y-6">

    <!-- Elegibilidad: rechazo por pre-filtro -->
    <div
      v-if="props.matchDetails?.eligibility_reason"
      class="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3"
    >
      <svg class="w-5 h-5 text-red-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M18.364 5.636l-12.728 12.728M5.636 5.636l12.728 12.728" />
      </svg>
      <div>
        <p class="text-sm font-semibold text-red-800">No cumples los requisitos de elegibilidad</p>
        <p class="text-sm text-red-700 mt-0.5">{{ props.matchDetails.eligibility_reason }}</p>
        <p class="text-xs text-red-500 mt-1">Este candidato no fue evaluado por el modelo de aptitudes.</p>
      </div>
    </div>

    <!-- Detalle de aptitudes (se oculta cuando hay rechazo por elegibilidad) -->
    <template v-if="!props.matchDetails?.eligibility_reason">

    <!-- Hard Skills -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h5 class="font-semibold text-gray-900">Competencias Tecnicas</h5>
        <span v-if="hardTotal > 0" class="text-sm text-gray-500">
          {{ hardMatchedCount }} de {{ hardTotal }} requisitos
        </span>
      </div>

      <!-- Progress bar for hard skills coverage -->
      <div v-if="hardTotal > 0" class="mb-3">
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="h-2 rounded-full transition-all duration-300"
            :class="hardCoverageColor"
            :style="{ width: hardCoveragePercent + '%' }"
          ></div>
        </div>
        <p class="text-xs mt-1" :class="hardCoverageTextColor">
          Cubres {{ hardCoveragePercent }}% de los requisitos tecnicos
        </p>
      </div>

      <!-- Required skills: matched (green) and missing (red) -->
      <div v-if="hardRequired.length > 0" class="mb-2">
        <span class="text-xs text-gray-500 block mb-1">Requeridas:</span>
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="skill in hardRequired"
            :key="skill.name"
            :class="[
              'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium',
              skill.matched
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            ]"
          >
            <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                v-if="skill.matched"
                stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M5 13l4 4L19 7"
              />
              <path
                v-else
                stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            {{ skill.name }}
          </span>
        </div>
      </div>

      <!-- Preferred skills matched (blue) -->
      <div v-if="preferredMatched.length > 0" class="mb-2">
        <span class="text-xs text-gray-500 block mb-1">Preferidas que tienes:</span>
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="skill in preferredMatched"
            :key="skill"
            class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
          >
            <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ skill }}
          </span>
        </div>
      </div>

      <p v-if="hardRequired.length === 0 && preferredMatched.length === 0" class="text-sm text-gray-400 italic">
        No se especificaron requisitos tecnicos para esta oferta
      </p>
    </div>

    <!-- Soft Skills -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h5 class="font-semibold text-gray-900">Habilidades Blandas</h5>
        <span v-if="softTotal > 0" class="text-sm text-gray-500">
          {{ softMatchedCount }} de {{ softTotal }} requisitos
        </span>
      </div>

      <!-- Progress bar for soft skills coverage -->
      <div v-if="softTotal > 0" class="mb-3">
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="h-2 rounded-full transition-all duration-300"
            :class="softCoverageColor"
            :style="{ width: softCoveragePercent + '%' }"
          ></div>
        </div>
        <p class="text-xs mt-1" :class="softCoverageTextColor">
          Cubres {{ softCoveragePercent }}% de las habilidades blandas requeridas
        </p>
      </div>

      <!-- Soft skills: matched (green) and missing (red) -->
      <div v-if="softRequired.length > 0">
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="skill in softRequired"
            :key="skill.name"
            :class="[
              'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium',
              skill.matched
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            ]"
          >
            <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                v-if="skill.matched"
                stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M5 13l4 4L19 7"
              />
              <path
                v-else
                stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            {{ skill.name }}
          </span>
        </div>
      </div>

      <p v-if="softRequired.length === 0" class="text-sm text-gray-400 italic">
        No se especificaron habilidades blandas requeridas
      </p>
    </div>

    <!-- Languages -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h5 class="font-semibold text-gray-900">Idiomas</h5>
        <span v-if="langTotal > 0" class="text-sm text-gray-500">
          {{ langMatchedCount }} de {{ langTotal }} requeridos
        </span>
      </div>

      <!-- Progress bar -->
      <div v-if="langTotal > 0" class="mb-3">
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="h-2 rounded-full transition-all duration-300"
            :class="langCoverageColor"
            :style="{ width: langCoveragePercent + '%' }"
          ></div>
        </div>
        <p class="text-xs mt-1" :class="langCoverageTextColor">
          Cubres {{ langCoveragePercent }}% de los idiomas requeridos
        </p>
      </div>

      <!-- Required languages: matched (green) and missing (red) -->
      <div v-if="langRequired.length > 0" class="mb-2">
        <span class="text-xs text-gray-500 block mb-1">Requeridos:</span>
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="lang in langRequired"
            :key="lang.name"
            :class="[
              'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium',
              lang.matched
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            ]"
          >
            <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                v-if="lang.matched"
                stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M5 13l4 4L19 7"
              />
              <path
                v-else
                stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            {{ lang.name }}
          </span>
        </div>
      </div>

      <!-- Extra languages from CV -->
      <div v-if="extraLangs.length > 0" class="mb-2">
        <span class="text-xs text-gray-500 block mb-1">Idiomas adicionales que tienes:</span>
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="lang in extraLangs"
            :key="lang"
            class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700"
          >
            {{ lang }}
          </span>
        </div>
      </div>

      <p v-if="langRequired.length === 0 && extraLangs.length === 0" class="text-sm text-gray-400 italic">
        No se especificaron requisitos de idiomas para esta oferta
      </p>
    </div>

    <!-- Nivel Educativo -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h5 class="font-semibold text-gray-900">Nivel Educativo</h5>
      </div>
      <div v-if="props.matchDetails?.education" class="flex items-center gap-3">
        <span :class="[
          'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium',
          props.matchDetails.education.meets_requirement ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]">
          <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="props.matchDetails.education.meets_requirement"
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
          {{ props.matchDetails.education.cv_level || 'Sin especificar' }}
        </span>
        <span class="text-xs text-gray-400">
          Requerido: <strong>{{ props.matchDetails.education.required_level }}</strong>
        </span>
      </div>
      <p v-else class="text-sm text-gray-400 italic">Sin información de nivel educativo</p>
    </div>

    <!-- Experiencia Laboral -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h5 class="font-semibold text-gray-900">Experiencia Laboral</h5>
      </div>
      <div v-if="props.matchDetails?.experience" class="flex items-center gap-3">
        <span :class="[
          'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium',
          props.matchDetails.experience.meets_minimum ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]">
          <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="props.matchDetails.experience.meets_minimum"
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
          {{ props.matchDetails.experience.cv_years }} año(s)
        </span>
        <span class="text-xs text-gray-400">
          Requerido: <strong>{{ props.matchDetails.experience.required_years }} año(s) mínimo</strong>
        </span>
      </div>
      <p v-else class="text-sm text-gray-400 italic">Sin información de experiencia requerida</p>
    </div>

    <!-- Extra CV skills (not required but the user has) -->
    <div v-if="extraHardSkills.length > 0">
      <h5 class="font-semibold text-gray-900 mb-2">Tus fortalezas adicionales</h5>
      <div class="flex flex-wrap gap-1.5">
        <span
          v-for="skill in extraHardSkills"
          :key="skill"
          class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600"
        >
          {{ skill }}
        </span>
      </div>
    </div>

    <!-- Contextual message -->
    <div
      v-if="contextMessage"
      :class="[
        'p-3 rounded-lg text-sm',
        contextMessageStyle
      ]"
    >
      {{ contextMessage }}
    </div>

    </template>
    <!-- fin detalle aptitudes -->

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  matchDetails: { type: Object, default: null },
  clasificacion: { type: String, default: '' }
})

// Hard skills: combine matched + missing into a single list with status
const hardRequired = computed(() => {
  if (!props.matchDetails?.hard_skills) return []
  const matched = (props.matchDetails.hard_skills.matched || []).map(s => ({ name: s, matched: true }))
  const missing = (props.matchDetails.hard_skills.missing || []).map(s => ({ name: s, matched: false }))
  return [...matched, ...missing]
})

const preferredMatched = computed(() => {
  return props.matchDetails?.hard_skills?.preferred_matched || []
})

const hardMatchedCount = computed(() => {
  return (props.matchDetails?.hard_skills?.matched || []).length
})

const hardTotal = computed(() => {
  return hardMatchedCount.value + (props.matchDetails?.hard_skills?.missing || []).length
})

const hardCoveragePercent = computed(() => {
  if (hardTotal.value === 0) return 0
  return Math.round((hardMatchedCount.value / hardTotal.value) * 100)
})

const hardCoverageColor = computed(() => {
  if (hardCoveragePercent.value >= 70) return 'bg-green-500'
  if (hardCoveragePercent.value >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
})

const hardCoverageTextColor = computed(() => {
  if (hardCoveragePercent.value >= 70) return 'text-green-600'
  if (hardCoveragePercent.value >= 40) return 'text-yellow-600'
  return 'text-red-600'
})

// Soft skills
const softRequired = computed(() => {
  if (!props.matchDetails?.soft_skills) return []
  const matched = (props.matchDetails.soft_skills.matched || []).map(s => ({ name: s, matched: true }))
  const missing = (props.matchDetails.soft_skills.missing || []).map(s => ({ name: s, matched: false }))
  return [...matched, ...missing]
})

const softMatchedCount = computed(() => {
  return (props.matchDetails?.soft_skills?.matched || []).length
})

const softTotal = computed(() => {
  return softMatchedCount.value + (props.matchDetails?.soft_skills?.missing || []).length
})

const softCoveragePercent = computed(() => {
  if (softTotal.value === 0) return 0
  return Math.round((softMatchedCount.value / softTotal.value) * 100)
})

const softCoverageColor = computed(() => {
  if (softCoveragePercent.value >= 70) return 'bg-green-500'
  if (softCoveragePercent.value >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
})

const softCoverageTextColor = computed(() => {
  if (softCoveragePercent.value >= 70) return 'text-green-600'
  if (softCoveragePercent.value >= 40) return 'text-yellow-600'
  return 'text-red-600'
})

// Languages
const langRequired = computed(() => {
  if (!props.matchDetails?.languages) return []
  const matched = (props.matchDetails.languages.matched || []).map(l => ({ name: l, matched: true }))
  const missing = (props.matchDetails.languages.missing || []).map(l => ({ name: l, matched: false }))
  return [...matched, ...missing]
})

const langMatchedCount = computed(() => (props.matchDetails?.languages?.matched || []).length)

const langTotal = computed(() =>
  langMatchedCount.value + (props.matchDetails?.languages?.missing || []).length
)

const langCoveragePercent = computed(() => {
  if (langTotal.value === 0) return 0
  return Math.round((langMatchedCount.value / langTotal.value) * 100)
})

const langCoverageColor = computed(() => {
  if (langCoveragePercent.value >= 70) return 'bg-green-500'
  if (langCoveragePercent.value >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
})

const langCoverageTextColor = computed(() => {
  if (langCoveragePercent.value >= 70) return 'text-green-600'
  if (langCoveragePercent.value >= 40) return 'text-yellow-600'
  return 'text-red-600'
})

// Idiomas del CV que no son requeridos
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

// Extra hard skills from CV that aren't in required/preferred
const extraHardSkills = computed(() => {
  if (!props.matchDetails) return []
  const cvHard = props.matchDetails.cv_skills?.hard || []
  const matched = new Set((props.matchDetails.hard_skills?.matched || []).map(s => s.toLowerCase()))
  const missing = new Set((props.matchDetails.hard_skills?.missing || []).map(s => s.toLowerCase()))
  const preferred = new Set((props.matchDetails.hard_skills?.preferred_matched || []).map(s => s.toLowerCase()))
  const required = new Set((props.matchDetails.required_skills?.hard || []).map(s => s.toLowerCase()))

  const known = new Set([...matched, ...missing, ...preferred, ...required])
  return cvHard.filter(s => !known.has(s.toLowerCase())).slice(0, 8)
})

// Contextual message based on classification
const contextMessage = computed(() => {
  if (props.matchDetails?.eligibility_reason) {
    return null // Ya se muestra el banner de elegibilidad arriba
  }
  switch (props.clasificacion) {
    case 'APTO':
      return 'Tienes un perfil fuerte para esta oferta. Tus competencias se alinean bien con los requisitos.'
    case 'CONSIDERADO':
      return 'Tu perfil tiene potencial para esta oferta. Considera fortalecer las areas marcadas en rojo.'
    default:
      return 'Tu perfil aun no cubre los requisitos principales. Revisa las competencias faltantes para mejorar tu compatibilidad.'
  }
})

const contextMessageStyle = computed(() => {
  switch (props.clasificacion) {
    case 'APTO':
      return 'bg-green-50 text-green-800'
    case 'CONSIDERADO':
      return 'bg-yellow-50 text-yellow-800'
    default:
      return 'bg-red-50 text-red-800'
  }
})
</script>
