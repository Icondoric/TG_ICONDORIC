<template>
  <CollapsibleSidebar
    :isOpen="isOpen"
    @update:isOpen="$emit('update:isOpen', $event)"
    width="280px"
    collapsedWidth="60px"
    persistenceKey="studentProfileSidebar"
    :leftOffset="uiStore.isSidebarOpen ? '256px' : '80px'"
  >
    <!-- Expanded Content -->
    <div class="p-4 space-y-6">
      <!-- Gauge Chart -->
      <div class="text-center">
        <GaugeChart
          :value="Math.round(profile.completeness_score * 100)"
          size="md"
          label="Completitud"
        />
        <div class="mt-2">
          <Badge :variant="profile.is_complete ? 'gold' : 'danger'" size="sm">
            {{ profile.is_complete ? 'Completo' : 'Incompleto' }}
          </Badge>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-2 gap-2">
        <div class="p-2 bg-emi-navy-50 rounded-lg text-center">
          <span class="block text-lg font-bold text-emi-navy-600">{{ profile.hard_skills.length }}</span>
          <span class="text-xs text-gray-500">Skills</span>
        </div>
        <div class="p-2 bg-emi-gold-50 rounded-lg text-center">
          <span class="block text-lg font-bold text-emi-gold-600">{{ profile.soft_skills.length }}</span>
          <span class="text-xs text-gray-500">Soft</span>
        </div>
        <div class="p-2 bg-purple-50 rounded-lg text-center">
          <span class="block text-lg font-bold text-purple-600">{{ profile.languages.length }}</span>
          <span class="text-xs text-gray-500">Idiomas</span>
        </div>
        <div class="p-2 bg-green-50 rounded-lg text-center">
          <span class="block text-lg font-bold text-green-600">{{ profile.experience_years }}</span>
          <span class="text-xs text-gray-500">Años</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="space-y-2 pt-4 border-t border-gray-100">
        <button
          @click="$emit('refresh')"
          class="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-emi-navy-600 bg-emi-navy-50 hover:bg-emi-navy-100 rounded-lg transition-colors"
          title="Actualizar datos"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Actualizar
        </button>
        <router-link
          to="/mis-recomendaciones"
          class="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-white bg-emi-navy-500 hover:bg-emi-navy-600 rounded-lg transition-colors shadow-sm"
        >
          Ver Recomendaciones
        </router-link>
      </div>
    </div>

    <!-- Collapsed Icons -->
    <template #collapsed>
      <div class="space-y-6 flex flex-col items-center w-full px-2">
        <div class="w-10 h-10 bg-emi-navy-100 rounded-full flex items-center justify-center text-lg font-bold text-emi-navy-600" title="Perfil">
          {{ profile.names ? profile.names.charAt(0) : 'U' }}
        </div>

        <div class="text-center" :title="`Completitud: ${Math.round(profile.completeness_score * 100)}%`">
          <div class="relative w-10 h-10 flex items-center justify-center">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="20" cy="20" r="16" fill="transparent" stroke="#e2e8f0" stroke-width="4"></circle>
              <circle cx="20" cy="20" r="16" fill="transparent" :stroke="profile.is_complete ? '#10b981' : '#f59e0b'" stroke-width="4"
                :stroke-dasharray="100" :stroke-dashoffset="100 - (profile.completeness_score * 100)"></circle>
            </svg>
            <span class="absolute text-[10px] font-bold">{{ Math.round(profile.completeness_score * 100) }}</span>
          </div>
        </div>

        <div class="flex flex-col gap-3 w-full border-t border-gray-100 pt-4">
          <div class="flex flex-col items-center" title="Skills Técnicas">
            <span class="text-xs font-bold text-emi-navy-600">{{ profile.hard_skills.length }}</span>
            <div class="w-1 h-1 rounded-full bg-emi-navy-500 mt-0.5"></div>
          </div>
          <div class="flex flex-col items-center" title="Skills Blandas">
            <span class="text-xs font-bold text-emi-gold-600">{{ profile.soft_skills.length }}</span>
            <div class="w-1 h-1 rounded-full bg-emi-gold-500 mt-0.5"></div>
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
  profile: { type: Object, required: true },
  isOpen: { type: Boolean, default: true }
})

defineEmits(['update:isOpen', 'refresh'])
</script>
