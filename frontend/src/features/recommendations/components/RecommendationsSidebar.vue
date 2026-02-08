<template>
  <CollapsibleSidebar
    :isOpen="isOpen"
    @update:isOpen="$emit('update:isOpen', $event)"
    width="280px"
    collapsedWidth="60px"
    persistenceKey="studentRecommendationsSidebar"
    :leftOffset="uiStore.isSidebarOpen ? '256px' : '80px'"
  >
    <!-- Expanded Content -->
    <div class="p-6">
      <!-- Best Match Gauge -->
      <div v-if="bestMatch" class="text-center mb-6">
        <GaugeChart
          :value="Math.round(bestMatch.match_score * 100)"
          size="lg"
          label="Mejor Match"
        />
        <p class="text-sm text-gray-600 mt-2 truncate" :title="bestMatch.oferta?.titulo">{{ bestMatch.oferta?.titulo }}</p>
      </div>
      <div v-else class="text-center mb-6">
        <GaugeChart :value="0" size="lg" label="Sin recomendaciones" />
      </div>

      <!-- Stats Summary -->
      <div class="mb-6 p-4 bg-emi-navy-50 rounded-xl border border-emi-navy-100">
        <h3 class="text-sm font-semibold text-emi-navy-700 mb-3">Resumen</h3>
        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Total</span>
            <Badge variant="navy" size="sm">{{ totalCount }}</Badge>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Nuevas</span>
            <Badge variant="gold" size="sm">{{ newCount }}</Badge>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">APTO</span>
            <Badge variant="gold" size="sm">{{ aptoCount }}</Badge>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Considerado</span>
            <Badge variant="navy" size="sm">{{ consideradoCount }}</Badge>
          </div>
        </div>
      </div>

      <!-- Profile Summary -->
      <div v-if="perfilSummary" class="mb-6">
        <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Tu Perfil</h3>
        <div class="space-y-3">
          <div v-if="perfilSummary.top_skills?.length > 0">
            <p class="text-xs text-gray-500 mb-2">Top Skills</p>
            <div class="flex flex-wrap gap-1">
              <Badge v-for="skill in perfilSummary.top_skills.slice(0, 4)" :key="skill" variant="navy" size="sm">
                {{ skill }}
              </Badge>
            </div>
          </div>
          <div v-if="perfilSummary.experience_years">
            <p class="text-xs text-gray-500">Experiencia</p>
            <p class="text-sm font-medium text-gray-700">{{ perfilSummary.experience_years }} años</p>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="space-y-3 pt-4 border-t border-gray-100">
        <button
          @click="$emit('refresh')"
          :disabled="refreshing"
          class="w-full flex items-center justify-center gap-2 btn-emi-primary"
        >
          <svg :class="['h-5 w-5', refreshing ? 'animate-spin' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ refreshing ? 'Actualizando...' : 'Actualizar' }}
        </button>

        <router-link
          to="/mi-perfil"
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
        <div class="text-center" title="Mejor Match">
          <div v-if="bestMatch" class="relative w-10 h-10 flex items-center justify-center">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="20" cy="20" r="16" fill="transparent" stroke="#e2e8f0" stroke-width="4"></circle>
              <circle cx="20" cy="20" r="16" fill="transparent" :stroke="bestMatch.match_score >= 0.7 ? '#10b981' : '#f59e0b'" stroke-width="4"
                :stroke-dasharray="100" :stroke-dashoffset="100 - (bestMatch.match_score * 100)"></circle>
            </svg>
            <span class="absolute text-[10px] font-bold">{{ Math.round(bestMatch.match_score * 100) }}</span>
          </div>
          <div v-else class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <span class="text-xs text-gray-400">0%</span>
          </div>
        </div>

        <div class="flex flex-col gap-3 w-full border-t border-gray-100 pt-4">
          <div class="flex flex-col items-center" title="Nuevas Ofertas">
            <span class="text-xs font-bold text-emi-gold-600">{{ newCount }}</span>
            <div class="w-1 h-1 rounded-full bg-emi-gold-500 mt-0.5"></div>
          </div>
          <div class="flex flex-col items-center" title="Total Ofertas">
            <span class="text-xs font-bold text-emi-navy-600">{{ totalCount }}</span>
            <div class="w-1 h-1 rounded-full bg-emi-navy-500 mt-0.5"></div>
          </div>
        </div>
      </div>
    </template>
  </CollapsibleSidebar>
</template>

<script setup>
import { useUiStore } from '@/shared/stores/ui'
import CollapsibleSidebar from '@/shared/components/ui/CollapsibleSidebar.vue'
import GaugeChart from '@/shared/components/ui/GaugeChart.vue'
import Badge from '@/shared/components/ui/Badge.vue'

const uiStore = useUiStore()

defineProps({
  isOpen: { type: Boolean, default: true },
  bestMatch: { type: Object, default: null },
  perfilSummary: { type: Object, default: null },
  totalCount: { type: Number, default: 0 },
  newCount: { type: Number, default: 0 },
  aptoCount: { type: Number, default: 0 },
  consideradoCount: { type: Number, default: 0 },
  refreshing: { type: Boolean, default: false }
})

defineEmits(['update:isOpen', 'refresh'])
</script>
