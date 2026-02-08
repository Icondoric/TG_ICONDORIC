<template>
  <Card v-if="hasGeminiData" title="Datos Extraidos del CV (Digitalizacion)">
    <div class="space-y-4">
      <!-- Personal Info / Summary -->
      <div v-if="geminiPersonalInfo?.summary">
        <h4 class="text-sm font-semibold text-gray-700 mb-2">Resumen Profesional</h4>
        <p class="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">{{ geminiPersonalInfo.summary }}</p>
      </div>

      <!-- Detected Names -->
      <div v-if="geminiPersonalInfo?.detected_names?.length > 0">
        <h4 class="text-sm font-semibold text-gray-700 mb-2">Nombres Detectados</h4>
        <div class="flex flex-wrap gap-2">
          <Badge v-for="name in geminiPersonalInfo.detected_names" :key="name" variant="neutral">
            {{ name }}
          </Badge>
        </div>
      </div>

      <!-- Contact Info -->
      <div v-if="geminiPersonalInfo?.email || geminiPersonalInfo?.phone" class="grid grid-cols-2 gap-4">
        <div v-if="geminiPersonalInfo?.email">
          <h4 class="text-sm font-semibold text-gray-700 mb-1">Email Detectado</h4>
          <p class="text-sm text-gray-600">{{ geminiPersonalInfo.email }}</p>
        </div>
        <div v-if="geminiPersonalInfo?.phone">
          <h4 class="text-sm font-semibold text-gray-700 mb-1">Telefono Detectado</h4>
          <p class="text-sm text-gray-600">{{ geminiPersonalInfo.phone }}</p>
        </div>
      </div>

      <!-- Extraction Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-gray-100">
        <div class="text-center p-2 bg-emi-navy-50 rounded-lg">
          <p class="text-xl font-bold text-emi-navy-600">{{ profile.hard_skills?.length || 0 }}</p>
          <p class="text-xs text-gray-500">Skills Tecnicos</p>
        </div>
        <div class="text-center p-2 bg-emi-gold-50 rounded-lg">
          <p class="text-xl font-bold text-emi-gold-600">{{ profile.soft_skills?.length || 0 }}</p>
          <p class="text-xs text-gray-500">Skills Blandos</p>
        </div>
        <div class="text-center p-2 bg-green-50 rounded-lg">
          <p class="text-xl font-bold text-green-600">{{ geminiEducation?.length || 0 }}</p>
          <p class="text-xs text-gray-500">Formacion</p>
        </div>
        <div class="text-center p-2 bg-purple-50 rounded-lg">
          <p class="text-xl font-bold text-purple-600">{{ geminiExperience?.length || 0 }}</p>
          <p class="text-xs text-gray-500">Experiencias</p>
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
  geminiPersonalInfo: { type: Object, default: () => ({}) },
  geminiEducation: { type: Array, default: () => [] },
  geminiExperience: { type: Array, default: () => [] },
  hasGeminiData: { type: Boolean, default: false }
})
</script>
