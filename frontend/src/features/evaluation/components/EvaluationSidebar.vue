<template>
  <CollapsibleSidebar
    :isOpen="isOpen"
    @update:isOpen="$emit('update:isOpen', $event)"
    width="280px"
    collapsedWidth="60px"
    persistenceKey="evaluationSidebar"
    :leftOffset="uiStore.isSidebarOpen ? '256px' : '80px'"
  >
    <!-- Expanded Content -->
    <div class="p-6">
      <!-- Last Evaluation Gauge -->
      <div v-if="lastEvaluation" class="text-center mb-6">
        <GaugeChart
          :value="Math.round(lastEvaluation.overall_score * 100)"
          size="lg"
          label="Última Evaluación"
        />
        <Badge
          :variant="getClassificationVariant(lastEvaluation.classification)"
          size="sm"
          class="mt-3"
        >
          {{ lastEvaluation.classification }}
        </Badge>
      </div>
      <div v-else class="text-center mb-6">
        <GaugeChart :value="0" size="lg" label="Sin evaluaciones" />
      </div>

      <!-- Stats Summary -->
      <div class="mb-6 p-4 bg-emi-navy-50 rounded-xl border border-emi-navy-100">
        <h3 class="text-sm font-semibold text-emi-navy-700 mb-3">Resumen</h3>
        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Perfiles Disponibles</span>
            <Badge variant="navy" size="sm">{{ profileCount }}</Badge>
          </div>
          <div v-if="isEvaluating" class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Estado</span>
            <Badge variant="gold" size="sm">
              <span class="flex items-center gap-1">
                <svg class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Evaluando
              </span>
            </Badge>
          </div>
        </div>
      </div>

      <!-- Navigation Links -->
      <div class="mb-6">
        <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Navegación</h3>
        <div class="space-y-2">
          <router-link
            to="/evaluation"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors',
              isCurrentRoute('/evaluation')
                ? 'bg-emi-navy-100 text-emi-navy-700 font-medium'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Evaluar CV
          </router-link>

          <router-link
            to="/history"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors',
              isCurrentRoute('/history')
                ? 'bg-emi-navy-100 text-emi-navy-700 font-medium'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Mi Historial
          </router-link>

          <router-link
            to="/mis-recomendaciones"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors',
              isCurrentRoute('/mis-recomendaciones')
                ? 'bg-emi-navy-100 text-emi-navy-700 font-medium'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
            </svg>
            Recomendaciones
          </router-link>
        </div>
      </div>

      <!-- Actions -->
      <div class="space-y-3 pt-4 border-t border-gray-100">
        <router-link
          to="/digitalizacion/mi-perfil"
          class="w-full flex items-center justify-center gap-2 px-4 py-2 border border-emi-navy-300 text-emi-navy-600 rounded-lg hover:bg-emi-navy-50 transition-colors"
        >
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Ver Mi Perfil
        </router-link>
      </div>
    </div>

    <!-- Collapsed Icons -->
    <template #collapsed>
      <div class="space-y-6 flex flex-col items-center w-full px-2">
        <div class="text-center" title="Última Evaluación">
          <div v-if="lastEvaluation" class="relative w-10 h-10 flex items-center justify-center">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="20" cy="20" r="16" fill="transparent" stroke="#e2e8f0" stroke-width="4"></circle>
              <circle cx="20" cy="20" r="16" fill="transparent" :stroke="getScoreColor(lastEvaluation.overall_score)" stroke-width="4"
                :stroke-dasharray="100" :stroke-dashoffset="100 - (lastEvaluation.overall_score * 100)"></circle>
            </svg>
            <span class="absolute text-[10px] font-bold">{{ Math.round(lastEvaluation.overall_score * 100) }}</span>
          </div>
          <div v-else class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <span class="text-xs text-gray-400">0%</span>
          </div>
        </div>

        <div class="flex flex-col gap-3 w-full border-t border-gray-100 pt-4">
          <router-link
            to="/history"
            class="flex flex-col items-center hover:bg-gray-100 rounded p-1 transition-colors"
            title="Mi Historial"
          >
            <svg class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </router-link>
          <router-link
            to="/mis-recomendaciones"
            class="flex flex-col items-center hover:bg-gray-100 rounded p-1 transition-colors"
            title="Recomendaciones"
          >
            <svg class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
            </svg>
          </router-link>
        </div>
      </div>
    </template>
  </CollapsibleSidebar>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useUiStore } from '@/shared/stores/ui'
import CollapsibleSidebar from '@/shared/components/ui/CollapsibleSidebar.vue'
import GaugeChart from '@/shared/components/ui/GaugeChart.vue'
import Badge from '@/shared/components/ui/Badge.vue'

const route = useRoute()
const uiStore = useUiStore()

defineProps({
  isOpen: { type: Boolean, default: true },
  lastEvaluation: { type: Object, default: null },
  profileCount: { type: Number, default: 0 },
  isEvaluating: { type: Boolean, default: false }
})

defineEmits(['update:isOpen'])

const isCurrentRoute = (path) => {
  return route.path === path
}

const getClassificationVariant = (classification) => {
  const variants = {
    'APTO': 'gold',
    'CONSIDERADO': 'navy',
    'NO_APTO': 'default'
  }
  return variants[classification] || 'default'
}

const getScoreColor = (score) => {
  if (score >= 0.7) return '#10b981' // green
  if (score >= 0.5) return '#f59e0b' // amber
  return '#ef4444' // red
}
</script>
