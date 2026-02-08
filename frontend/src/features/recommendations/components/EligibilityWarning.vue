<template>
  <Card class="border-emi-gold-200 bg-emi-gold-50">
    <div class="flex items-start gap-4">
      <div class="p-3 bg-emi-gold-100 rounded-full">
        <svg class="h-6 w-6 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-emi-gold-800">{{ reason }}</h3>
        <p v-if="action" class="mt-2 text-emi-gold-700">{{ action }}</p>

        <!-- Missing Fields -->
        <div v-if="missingFields.length > 0" class="mt-4">
          <p class="text-sm text-emi-gold-700 mb-2">Campos faltantes:</p>
          <ul class="list-disc list-inside text-sm text-emi-gold-600">
            <li v-for="field in missingFields" :key="field">{{ field }}</li>
          </ul>
        </div>

        <router-link
          to="/subir-cv"
          class="mt-4 inline-flex items-center gap-2 btn-emi-secondary"
        >
          Completar Perfil
        </router-link>
      </div>
    </div>
  </Card>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'

defineProps({
  reason: { type: String, default: '' },
  action: { type: String, default: '' },
  missingFields: { type: Array, default: () => [] }
})
</script>
