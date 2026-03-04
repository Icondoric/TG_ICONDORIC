<template>
  <div>
    <!-- Nombre + botón editar -->
    <div class="flex items-start justify-between gap-4">
      <div class="flex-1 min-w-0">
        <h2
          class="text-2xl font-bold text-emi-navy-600 uppercase tracking-wide leading-tight"
          :class="{ '!text-gray-400 !text-xl !normal-case !tracking-normal italic': !profile.nombre_completo }"
        >
          {{ profile.nombre_completo || 'Sin nombre registrado' }}
        </h2>

        <!-- Fila de contacto: email | teléfono | dirección | nacionalidad -->
        <div v-if="contactParts.length" class="mt-2 flex flex-wrap items-center gap-x-1 gap-y-0.5 text-sm text-gray-500">
          <template v-for="(part, i) in contactParts" :key="i">
            <span v-if="i > 0" class="text-gray-300 select-none">|</span>
            <span>{{ part }}</span>
          </template>
        </div>
        <p v-else class="mt-1.5 text-sm text-gray-400 italic">
          Sin información de contacto registrada
        </p>
      </div>

      <button
        v-if="!readOnly"
        @click="$emit('edit')"
        class="flex-shrink-0 inline-flex items-center gap-1.5 text-sm text-emi-navy-600 hover:text-emi-navy-800 font-medium transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
        Editar
      </button>
    </div>

    <!-- Línea divisoria navy -->
    <div class="mt-3 h-0.5 bg-emi-navy-500 rounded-full"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: { type: Object, required: true },
  readOnly: { type: Boolean, default: false }
})

defineEmits(['edit'])

const contactParts = computed(() => {
  const parts = []
  if (props.profile.email_contacto) parts.push(props.profile.email_contacto)
  if (props.profile.telefono) parts.push(props.profile.telefono)
  if (props.profile.direccion) parts.push(props.profile.direccion)
  if (props.profile.nacionalidad) parts.push(props.profile.nacionalidad)
  return parts
})
</script>
