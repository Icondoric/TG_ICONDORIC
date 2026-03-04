<template>
  <div class="space-y-6">

    <!-- ── HABILIDADES TÉCNICAS ── -->
    <div>
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
          Habilidades Técnicas
        </h3>
        <button
          v-if="!readOnly"
          @click="$emit('edit', 'skills')"
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
      <div class="mt-2 flex flex-wrap gap-2">
        <Badge v-for="skill in profile.hard_skills" :key="skill" variant="navy">{{ skill }}</Badge>
        <span v-if="!profile.hard_skills?.length" class="text-sm text-gray-400 italic">
          Sin habilidades técnicas registradas<template v-if="!readOnly"> —
            <button @click="$emit('edit', 'skills')"
              class="text-emi-navy-500 hover:underline not-italic">Agregar</button>
          </template>
        </span>
      </div>
    </div>

    <!-- ── HABILIDADES BLANDAS ── -->
    <div>
      <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
        Habilidades Blandas
      </h3>
      <div class="mt-1 h-px bg-emi-navy-300"></div>
      <div class="mt-2 flex flex-wrap gap-2">
        <Badge v-for="skill in profile.soft_skills" :key="skill" variant="gold">{{ skill }}</Badge>
        <span v-if="!profile.soft_skills?.length" class="text-sm text-gray-400 italic">
          Sin habilidades blandas registradas<template v-if="!readOnly"> —
            <button @click="$emit('edit', 'skills')"
              class="text-emi-navy-500 hover:underline not-italic">Agregar</button>
          </template>
        </span>
      </div>
    </div>

    <!-- ── IDIOMAS ── -->
    <div>
      <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
        Idiomas
      </h3>
      <div class="mt-1 h-px bg-emi-navy-300"></div>
      <div class="mt-2 flex flex-wrap gap-2">
        <Badge v-for="lang in profile.languages" :key="lang" variant="neutral">{{ lang }}</Badge>
        <span v-if="!profile.languages?.length" class="text-sm text-gray-400 italic">
          Sin idiomas registrados<template v-if="!readOnly"> —
            <button @click="$emit('edit', 'skills')"
              class="text-emi-navy-500 hover:underline not-italic">Agregar</button>
          </template>
        </span>
      </div>
    </div>

  </div>
</template>

<script setup>
import Badge from '@/shared/components/ui/Badge.vue'

defineProps({
  profile: { type: Object, required: true },
  readOnly: { type: Boolean, default: false }
})

defineEmits(['edit'])
</script>
