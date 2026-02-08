<template>
  <Card id="competencias">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-gray-900">Competencias</h2>
      <button
        @click="$emit('edit', 'skills')"
        class="flex items-center gap-1 text-sm text-emi-navy-500 hover:text-emi-gold-500 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
        Editar
      </button>
    </div>

    <!-- Hard Skills -->
    <div class="mb-6">
      <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 bg-emi-navy-500 rounded-full"></span>
        Habilidades Tecnicas
      </h3>
      <div class="flex flex-wrap gap-2">
        <Badge v-for="skill in profile.hard_skills" :key="skill" variant="navy">
          {{ skill }}
        </Badge>
        <span v-if="profile.hard_skills.length === 0" class="text-gray-400 text-sm">
          No hay habilidades registradas -
          <button @click="$emit('edit', 'skills')" class="text-emi-navy-500 hover:underline">Agregar</button>
        </span>
      </div>
    </div>

    <!-- Soft Skills -->
    <div class="mb-6">
      <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 bg-emi-gold-500 rounded-full"></span>
        Habilidades Blandas
      </h3>
      <div class="flex flex-wrap gap-2">
        <Badge v-for="skill in profile.soft_skills" :key="skill" variant="gold">
          {{ skill }}
        </Badge>
        <span v-if="profile.soft_skills.length === 0" class="text-gray-400 text-sm">
          No hay habilidades registradas -
          <button @click="$emit('edit', 'skills')" class="text-emi-navy-500 hover:underline">Agregar</button>
        </span>
      </div>
    </div>

    <!-- Languages -->
    <div>
      <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
        Idiomas
      </h3>
      <div class="flex flex-wrap gap-2">
        <Badge v-for="lang in profile.languages" :key="lang" variant="neutral">
          {{ lang }}
        </Badge>
        <span v-if="profile.languages.length === 0" class="text-gray-400 text-sm">
          No hay idiomas registrados -
          <button @click="$emit('edit', 'skills')" class="text-emi-navy-500 hover:underline">Agregar</button>
        </span>
      </div>
    </div>
  </Card>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'

defineProps({
  profile: { type: Object, required: true }
})

defineEmits(['edit'])
</script>
