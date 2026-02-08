<template>
  <Card class="mb-6 border-2 border-emi-gold-200 bg-gradient-to-br from-emi-gold-50 to-white">
    <div class="flex items-start gap-4">
      <div class="p-3 bg-emi-gold-500 rounded-xl shadow-md">
        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <div class="flex-1">
        <h2 class="text-xl font-bold text-gray-900 mb-2">
          {{ profile.cv_filename ? 'CV Cargado' : 'Sube tu Curriculum Vitae' }}
        </h2>

        <!-- CV Info if exists -->
        <div v-if="profile.cv_filename" class="mb-4 p-4 bg-white rounded-lg border border-emi-gold-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-emi-navy-100 rounded-lg">
                <svg class="h-6 w-6 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <p class="font-semibold text-gray-900">{{ profile.cv_filename }}</p>
                <p class="text-sm text-gray-500">Subido {{ formatDate(profile.cv_uploaded_at) }}</p>
              </div>
            </div>
            <Badge variant="gold">
              <svg class="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Procesado
            </Badge>
          </div>
        </div>

        <p class="text-gray-600 mb-4">
          {{ profile.cv_filename
            ? 'Actualiza tu CV para refrescar la información extraída de tu perfil profesional.'
            : 'Nuestro sistema de IA extraerá automáticamente tus competencias, formación y experiencia laboral.'
          }}
        </p>

        <div class="flex flex-wrap gap-3">
          <button
            @click="$emit('showUpload')"
            class="inline-flex items-center gap-2 px-6 py-3 bg-emi-gold-500 text-emi-navy-800 rounded-lg font-semibold hover:bg-emi-gold-400 transition-all hover:shadow-lg hover:-translate-y-0.5"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            {{ profile.cv_filename ? 'Actualizar CV' : 'Subir CV (PDF)' }}
          </button>

          <button
            v-if="profile.cv_filename"
            @click="$emit('showDelete')"
            class="inline-flex items-center gap-2 px-6 py-3 border-2 border-red-300 text-red-700 rounded-lg font-semibold hover:bg-red-50 transition-colors"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Limpiar Perfil
          </button>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'

defineProps({
  profile: { type: Object, required: true },
  formatDate: { type: Function, required: true }
})

defineEmits(['showUpload', 'showDelete'])
</script>
