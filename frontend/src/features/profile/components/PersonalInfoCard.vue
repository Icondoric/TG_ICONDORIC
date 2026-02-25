<template>
  <Card>
    <!-- Header con botón editar -->
    <div class="flex items-center justify-between mb-5">
      <div class="flex items-center gap-2">
        <div class="p-2 bg-emi-navy-100 rounded-lg">
          <svg class="w-5 h-5 text-emi-navy-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-900">Información Personal</h2>
      </div>
      <button
        @click="$emit('edit')"
        class="inline-flex items-center gap-1.5 text-sm text-emi-navy-600 hover:text-emi-navy-800 font-medium transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
        Editar
      </button>
    </div>

    <!-- Grid de campos -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <!-- Nombre -->
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 mt-0.5 p-1.5 bg-gray-100 rounded-md">
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Nombre completo</p>
          <p class="text-sm font-semibold text-gray-900 mt-0.5" :class="{ 'text-gray-400 italic': !profile.nombre_completo }">
            {{ profile.nombre_completo || 'Sin definir' }}
          </p>
        </div>
      </div>

      <!-- Nacionalidad -->
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 mt-0.5 p-1.5 bg-gray-100 rounded-md">
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Nacionalidad</p>
          <p class="text-sm font-semibold text-gray-900 mt-0.5" :class="{ 'text-gray-400 italic': !profile.nacionalidad }">
            {{ profile.nacionalidad || 'Sin definir' }}
          </p>
        </div>
      </div>

      <!-- Teléfono -->
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 mt-0.5 p-1.5 bg-gray-100 rounded-md">
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Teléfono</p>
          <p class="text-sm font-semibold text-gray-900 mt-0.5" :class="{ 'text-gray-400 italic': !profile.telefono }">
            {{ profile.telefono || 'Sin definir' }}
          </p>
        </div>
      </div>

      <!-- Email -->
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 mt-0.5 p-1.5 bg-gray-100 rounded-md">
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Email de contacto</p>
          <p class="text-sm font-semibold text-gray-900 mt-0.5 break-all" :class="{ 'text-gray-400 italic': !profile.email_contacto }">
            {{ profile.email_contacto || 'Sin definir' }}
          </p>
        </div>
      </div>

      <!-- Dirección (span 2 columnas) -->
      <div class="flex items-start gap-3 sm:col-span-2">
        <div class="flex-shrink-0 mt-0.5 p-1.5 bg-gray-100 rounded-md">
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Dirección / Ubicación</p>
          <p class="text-sm font-semibold text-gray-900 mt-0.5" :class="{ 'text-gray-400 italic': !profile.direccion }">
            {{ profile.direccion || 'Sin definir' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Banner si todos los campos están vacíos -->
    <div
      v-if="!hasAnyPersonalInfo"
      class="mt-5 pt-4 border-t border-gray-100 flex items-center justify-between"
    >
      <p class="text-sm text-gray-500">
        Sube tu CV para auto-completar estos datos o edítalos manualmente.
      </p>
      <button
        @click="$emit('edit')"
        class="text-sm font-medium text-emi-navy-600 hover:underline flex-shrink-0 ml-4"
      >
        Completar ahora →
      </button>
    </div>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import Card from '@/shared/components/ui/Card.vue'

const props = defineProps({
  profile: { type: Object, required: true }
})

defineEmits(['edit'])

const hasAnyPersonalInfo = computed(() =>
  props.profile.nombre_completo ||
  props.profile.telefono ||
  props.profile.email_contacto ||
  props.profile.direccion ||
  props.profile.nacionalidad
)
</script>
