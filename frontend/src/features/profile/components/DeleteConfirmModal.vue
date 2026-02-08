<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
    <Card class="max-w-md mx-4" :hoverable="false">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Confirmar limpieza de perfil</h3>
      <p class="text-gray-600 mb-6">
        Esto eliminara todos los datos de tu CV y competencias. Tendras que subir tu CV nuevamente.
        Esta accion no se puede deshacer.
      </p>
      <div class="flex justify-end gap-3">
        <button
          @click="$emit('cancel')"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          Cancelar
        </button>
        <button
          @click="$emit('confirm')"
          :disabled="deleting"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors"
        >
          {{ deleting ? 'Eliminando...' : 'Eliminar' }}
        </button>
      </div>
    </Card>
  </div>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'

defineProps({
  show: { type: Boolean, default: false },
  deleting: { type: Boolean, default: false }
})

defineEmits(['cancel', 'confirm'])
</script>
