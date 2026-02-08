<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- Education -->
    <Card id="formacion">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-900">Formacion Academica</h2>
        <button
          @click="$emit('edit', 'education')"
          class="flex items-center gap-1 text-sm text-emi-navy-500 hover:text-emi-gold-500 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
          Editar
        </button>
      </div>

      <div v-if="profile.education_level" class="flex items-center mb-4">
        <div class="p-3 bg-emi-navy-100 rounded-xl mr-4">
          <svg class="h-8 w-8 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path d="M12 14l9-5-9-5-9 5 9 5z" />
            <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
          </svg>
        </div>
        <div>
          <p class="font-semibold text-gray-900">{{ profile.education_level }}</p>
          <p class="text-sm text-gray-500">Nivel educativo mas alto</p>
        </div>
      </div>
      <p v-else class="text-gray-400 text-sm">
        No hay formacion registrada -
        <button @click="$emit('edit', 'education')" class="text-emi-navy-500 hover:underline">Agregar</button>
      </p>

      <!-- Education Details from Gemini -->
      <div v-if="geminiEducation.length > 0" class="mt-4 pt-4 border-t border-gray-100 space-y-3">
        <div v-for="(edu, index) in geminiEducation" :key="index" class="p-3 bg-gray-50 rounded-lg">
          <p class="font-medium text-gray-800">{{ edu.degree }}</p>
          <p class="text-sm text-gray-600">{{ edu.institution }}</p>
          <p v-if="edu.year" class="text-xs text-gray-400 mt-1">{{ edu.year }}</p>
        </div>
      </div>
    </Card>

    <!-- Experience -->
    <Card id="experiencia">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-900">Experiencia Laboral</h2>
        <button
          @click="$emit('edit', 'experience')"
          class="flex items-center gap-1 text-sm text-emi-navy-500 hover:text-emi-gold-500 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
          Editar
        </button>
      </div>

      <div class="flex items-center mb-4">
        <div class="p-3 bg-emi-gold-100 rounded-xl mr-4">
          <svg class="h-8 w-8 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <p class="font-semibold text-gray-900">{{ profile.experience_years }} anos</p>
          <p class="text-sm text-gray-500">Experiencia total</p>
        </div>
      </div>

      <!-- Experience Details from Gemini -->
      <div v-if="geminiExperience.length > 0" class="mt-4 pt-4 border-t border-gray-100 space-y-3">
        <div v-for="(exp, index) in geminiExperience" :key="index" class="p-3 bg-gray-50 rounded-lg">
          <p class="font-medium text-gray-800">{{ exp.role }}</p>
          <p class="text-sm text-gray-600">{{ exp.company }}</p>
          <p v-if="exp.duration" class="text-xs text-gray-400 mt-1">{{ exp.duration }}</p>
        </div>
      </div>
      <p v-else-if="geminiExperience.length === 0 && profile.experience_years === 0" class="text-gray-400 text-sm">
        No hay experiencia registrada -
        <button @click="$emit('edit', 'experience')" class="text-emi-navy-500 hover:underline">Agregar</button>
      </p>
    </Card>
  </div>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'

defineProps({
  profile: { type: Object, required: true },
  geminiEducation: { type: Array, default: () => [] },
  geminiExperience: { type: Array, default: () => [] }
})

defineEmits(['edit'])
</script>
