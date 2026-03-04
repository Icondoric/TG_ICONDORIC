<template>
  <aside
    class="sticky top-0 h-screen flex-shrink-0 border-l border-gray-200 bg-white transition-all duration-300 ease-in-out hidden lg:flex flex-col overflow-hidden relative"
    :style="{ width: isExpanded ? '220px' : '52px' }"
  >
    <!-- Toggle Button -->
    <button
      @click="toggle"
      class="absolute top-4 -left-3 z-10 w-6 h-6 bg-white border border-gray-200 rounded-full flex items-center justify-center text-gray-500 hover:text-emi-navy-500 hover:border-emi-navy-300 transition-colors shadow-sm focus:outline-none"
    >
      <div :class="{ 'rotate-180': isExpanded }" class="transition-transform duration-300">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </div>
    </button>

    <!-- Scrollable Content -->
    <div class="flex-1 overflow-y-auto overflow-x-hidden">

      <!-- Expanded -->
      <div v-show="isExpanded" class="p-4 space-y-4 pt-10" style="width: 220px">

        <!-- Gauge Chart -->
        <div class="text-center">
          <GaugeChart
            :value="Math.round(profile.completeness_score * 100)"
            size="sm"
            label="Completitud"
          />
          <Badge :variant="profile.is_complete ? 'gold' : 'danger'" size="sm" class="mt-1">
            {{ profile.is_complete ? 'Completo' : 'Incompleto' }}
          </Badge>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 gap-1.5">
          <div class="p-2 bg-emi-navy-50 rounded-lg text-center">
            <span class="block text-base font-bold text-emi-navy-600">{{ profile.hard_skills.length }}</span>
            <span class="text-[11px] text-gray-500">Técnicas</span>
          </div>
          <div class="p-2 bg-emi-gold-50 rounded-lg text-center">
            <span class="block text-base font-bold text-emi-gold-600">{{ profile.soft_skills.length }}</span>
            <span class="text-[11px] text-gray-500">Blandas</span>
          </div>
          <div class="p-2 bg-purple-50 rounded-lg text-center">
            <span class="block text-base font-bold text-purple-600">{{ profile.languages.length }}</span>
            <span class="text-[11px] text-gray-500">Idiomas</span>
          </div>
          <div class="p-2 bg-green-50 rounded-lg text-center">
            <span class="block text-base font-bold text-green-600">{{ profile.experience_years }}</span>
            <span class="text-[11px] text-gray-500">Años exp.</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="pt-3 border-t border-gray-100">
          <button
            @click="$emit('refresh')"
            class="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-emi-navy-600 bg-emi-navy-50 hover:bg-emi-navy-100 rounded-lg transition-colors"
            title="Actualizar datos"
          >
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
        </div>
      </div>

      <!-- Collapsed Icons -->
      <div v-show="!isExpanded" class="flex flex-col items-center pt-12 space-y-5 px-2">
        <!-- Score circular -->
        <div class="text-center" :title="`Completitud: ${Math.round(profile.completeness_score * 100)}%`">
          <div class="relative w-10 h-10 flex items-center justify-center">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="20" cy="20" r="16" fill="transparent" stroke="#e2e8f0" stroke-width="4" />
              <circle
                cx="20" cy="20" r="16"
                fill="transparent"
                :stroke="profile.is_complete ? '#10b981' : '#f59e0b'"
                stroke-width="4"
                :stroke-dasharray="100"
                :stroke-dashoffset="100 - (profile.completeness_score * 100)"
              />
            </svg>
            <span class="absolute text-[10px] font-bold">{{ Math.round(profile.completeness_score * 100) }}</span>
          </div>
        </div>

        <!-- Mini stats -->
        <div class="flex flex-col gap-2.5 w-full border-t border-gray-100 pt-3">
          <div class="flex flex-col items-center" title="Skills Técnicas">
            <span class="text-xs font-bold text-emi-navy-600">{{ profile.hard_skills.length }}</span>
            <div class="w-1 h-1 rounded-full bg-emi-navy-500 mt-0.5"></div>
          </div>
          <div class="flex flex-col items-center" title="Skills Blandas">
            <span class="text-xs font-bold text-emi-gold-600">{{ profile.soft_skills.length }}</span>
            <div class="w-1 h-1 rounded-full bg-emi-gold-500 mt-0.5"></div>
          </div>
          <div class="flex flex-col items-center" title="Idiomas">
            <span class="text-xs font-bold text-purple-600">{{ profile.languages.length }}</span>
            <div class="w-1 h-1 rounded-full bg-purple-400 mt-0.5"></div>
          </div>
        </div>

        <!-- Refresh icon -->
        <button
          @click="$emit('refresh')"
          class="w-8 h-8 flex items-center justify-center rounded-lg text-emi-navy-500 hover:bg-emi-navy-50 transition-colors"
          title="Actualizar"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

    </div>
  </aside>
</template>

<script setup>
import { ref, watch } from 'vue'
import GaugeChart from '@/shared/components/ui/GaugeChart.vue'
import Badge from '@/shared/components/ui/Badge.vue'

const props = defineProps({
  profile: { type: Object, required: true },
  isOpen: { type: Boolean, default: true }
})

const emit = defineEmits(['update:isOpen', 'refresh'])

const isExpanded = ref(props.isOpen)

watch(() => props.isOpen, (val) => {
  isExpanded.value = val
})

const toggle = () => {
  isExpanded.value = !isExpanded.value
  emit('update:isOpen', isExpanded.value)
}
</script>
