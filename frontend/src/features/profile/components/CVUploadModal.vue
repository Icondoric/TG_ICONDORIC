<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50 p-4">
    <Card class="w-full max-w-lg" :hoverable="false">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">Subir CV</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div
        @dragover.prevent="$emit('dragOver')"
        @dragleave.prevent="$emit('dragLeave')"
        @drop.prevent="$emit('drop', $event)"
        :class="[
          'border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer',
          isDragging ? 'border-emi-gold-500 bg-emi-gold-50' : 'border-gray-300 hover:border-emi-navy-400'
        ]"
        @click="$refs.fileInput.click()"
      >
        <template v-if="!uploadFile">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="mt-2 text-gray-600">Arrastra tu CV aqui o <span class="text-emi-navy-500 font-medium">selecciona un archivo</span></p>
          <p class="mt-1 text-sm text-gray-500">Solo archivos PDF (max. 10MB)</p>
        </template>
        <template v-else>
          <svg class="mx-auto h-12 w-12 text-emi-gold-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-2 font-medium text-gray-900">{{ uploadFile.name }}</p>
          <p class="mt-1 text-sm text-gray-500">{{ formatFileSize(uploadFile.size) }}</p>
        </template>
      </div>
      <input ref="fileInput" type="file" accept=".pdf" @change="$emit('fileSelect', $event)" class="hidden" />

      <div class="mt-4 flex justify-end gap-3">
        <button
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          Cancelar
        </button>
        <button
          @click="$emit('process')"
          :disabled="!uploadFile || uploading"
          class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ uploading ? 'Procesando...' : 'Procesar CV' }}
        </button>
      </div>
    </Card>
  </div>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'

defineProps({
  show: { type: Boolean, default: false },
  uploadFile: { type: Object, default: null },
  uploading: { type: Boolean, default: false },
  isDragging: { type: Boolean, default: false },
  formatFileSize: { type: Function, required: true }
})

defineEmits(['close', 'dragOver', 'dragLeave', 'drop', 'fileSelect', 'process'])
</script>
