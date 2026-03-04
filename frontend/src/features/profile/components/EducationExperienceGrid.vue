<template>
  <div class="space-y-8">

    <!-- ── FORMACIÓN ACADÉMICA ── -->
    <div>
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
          Formación Académica
        </h3>
        <button
          v-if="!readOnly"
          @click="$emit('edit', 'education')"
          class="inline-flex items-center gap-1.5 text-sm text-emi-navy-600 hover:text-emi-navy-800 font-medium transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
          Editar
        </button>
      </div>
      <div class="mt-1 h-px bg-emi-navy-300"></div>

      <div class="mt-3 space-y-3">
        <!-- Nivel educativo si no hay entradas de Gemini -->
        <div v-if="profile.education_level && !sortedEducation.length"
          class="flex justify-between items-baseline gap-4">
          <span class="text-sm font-semibold text-gray-900">{{ profile.education_level }}</span>
          <span class="text-xs text-gray-400 flex-shrink-0">Nivel más alto registrado</span>
        </div>

        <!-- Entradas de educación (Gemini, ordenadas desc por año) -->
        <div v-for="(edu, i) in sortedEducation" :key="i">
          <div class="flex justify-between items-baseline gap-4">
            <span class="text-sm font-semibold text-gray-900">{{ edu.degree }}</span>
            <span v-if="edu.year" class="text-xs text-gray-400 flex-shrink-0 italic">{{ edu.year }}</span>
          </div>
          <p class="text-sm text-gray-500 italic mt-0.5">{{ edu.institution }}</p>
        </div>

        <!-- Estado vacío -->
        <p v-if="!profile.education_level && !sortedEducation.length" class="text-sm text-gray-400 italic">
          Sin formación académica registrada<template v-if="!readOnly"> —
            <button @click="$emit('edit', 'education')"
              class="text-emi-navy-500 hover:underline not-italic">Agregar</button>
          </template>
        </p>
      </div>
    </div>

    <!-- ── EXPERIENCIA PROFESIONAL ── -->
    <div>
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
          Experiencia Profesional
        </h3>
        <button
          v-if="!readOnly"
          @click="$emit('edit', 'experience')"
          class="inline-flex items-center gap-1.5 text-sm text-emi-navy-600 hover:text-emi-navy-800 font-medium transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
          Editar
        </button>
      </div>
      <div class="mt-1 h-px bg-emi-navy-300"></div>

      <div class="mt-3 space-y-4">
        <!-- Total años si no hay entradas de Gemini -->
        <div v-if="profile.experience_years > 0 && !geminiExperience.length"
          class="flex justify-between items-baseline gap-4">
          <span class="text-sm font-semibold text-gray-900">Experiencia declarada</span>
          <span class="text-xs text-gray-400 flex-shrink-0 italic">{{ profile.experience_years }} año(s)</span>
        </div>

        <!-- Entradas de experiencia (Gemini) -->
        <div v-for="(exp, i) in geminiExperience" :key="i">
          <div class="flex justify-between items-baseline gap-4">
            <span class="text-sm font-semibold text-gray-900">{{ exp.role }}</span>
            <span v-if="exp.duration" class="text-xs text-gray-400 flex-shrink-0 italic">{{ exp.duration }}</span>
          </div>
          <p class="text-sm text-gray-500 italic mt-0.5">{{ exp.company }}</p>
        </div>

        <!-- Estado vacío -->
        <p v-if="!profile.experience_years && !geminiExperience.length" class="text-sm text-gray-400 italic">
          Sin experiencia profesional registrada<template v-if="!readOnly"> —
            <button @click="$emit('edit', 'experience')"
              class="text-emi-navy-500 hover:underline not-italic">Agregar</button>
          </template>
        </p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: { type: Object, required: true },
  geminiEducation: { type: Array, default: () => [] },
  geminiExperience: { type: Array, default: () => [] },
  readOnly: { type: Boolean, default: false }
})

defineEmits(['edit'])

const sortedEducation = computed(() =>
  [...props.geminiEducation].sort((a, b) => {
    const ya = parseInt(a.year) || 0
    const yb = parseInt(b.year) || 0
    return yb - ya
  })
)
</script>
