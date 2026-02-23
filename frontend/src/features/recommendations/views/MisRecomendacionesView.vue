<template>
  <AppLayout>
    <div class="flex min-h-screen">
      <!-- Main Content -->
      <div class="flex-1 min-w-0">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- Header -->
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-emi-navy-500">Mis Recomendaciones</h1>
            <p class="mt-2 text-gray-600">
              {{ userRole === 'estudiante' ? 'Pasantias recomendadas' : ['admin', 'administrador'].includes(userRole) ? 'Pasantias y empleos recomendados' : 'Empleos recomendados' }} basados en tu perfil
            </p>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
          </div>

          <!-- Not Eligible -->
          <EligibilityWarning
            v-else-if="!isEligible"
            :reason="eligibilityReason"
            :action="eligibilityAction"
            :missingFields="missingFields"
          />

          <!-- Error -->
          <Card v-else-if="error" class="border-red-200 bg-red-50">
            <p class="text-red-700">{{ error }}</p>
            <button @click="loadRecommendations" class="mt-2 text-red-600 hover:text-red-800 underline">
              Reintentar
            </button>
          </Card>

          <!-- Results -->
          <div v-else>
            <!-- Mobile Stats Bar -->
            <Card class="lg:hidden mb-6">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-2xl font-bold text-emi-navy-500">{{ recommendations.length }}</span>
                  <span class="text-gray-500 ml-1">recomendaciones</span>
                </div>
                <div v-if="newCount > 0">
                  <Badge variant="gold">{{ newCount }} nuevas</Badge>
                </div>
              </div>
              <div class="mt-4 flex gap-2">
                <button
                  @click="loadRecommendations(true)"
                  :disabled="refreshing"
                  class="flex-1 flex items-center justify-center gap-2 btn-emi-primary text-sm"
                >
                  <svg :class="['h-4 w-4', refreshing ? 'animate-spin' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  {{ refreshing ? 'Actualizando...' : 'Actualizar' }}
                </button>
              </div>
            </Card>

            <!-- ── Resumen de Correspondencia (desktop) ───────────────────── -->
            <div v-if="recommendations.length > 0" class="hidden lg:grid grid-cols-3 gap-4 mb-6">

              <!-- Clasificación + tipos + convenio -->
              <Card class="col-span-2">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <svg class="h-4 w-4 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  Correspondencia con el mercado EMI
                </h3>

                <!-- Contadores APTO / CONSIDERADO / NO APTO -->
                <div class="grid grid-cols-3 gap-3">
                  <div class="text-center p-3 bg-emi-gold-50 rounded-xl border border-emi-gold-200">
                    <span class="block text-2xl font-bold text-emi-gold-600">{{ aptoCount }}</span>
                    <span class="text-xs font-medium text-emi-gold-700">APTO</span>
                    <div class="mt-2 w-full bg-emi-gold-200 rounded-full h-1.5">
                      <div
                        class="bg-emi-gold-500 h-1.5 rounded-full transition-all duration-500"
                        :style="{ width: recommendations.length ? (aptoCount / recommendations.length * 100) + '%' : '0%' }"
                      ></div>
                    </div>
                  </div>
                  <div class="text-center p-3 bg-emi-navy-50 rounded-xl border border-emi-navy-200">
                    <span class="block text-2xl font-bold text-emi-navy-600">{{ consideradoCount }}</span>
                    <span class="text-xs font-medium text-emi-navy-700">CONSIDERADO</span>
                    <div class="mt-2 w-full bg-emi-navy-200 rounded-full h-1.5">
                      <div
                        class="bg-emi-navy-500 h-1.5 rounded-full transition-all duration-500"
                        :style="{ width: recommendations.length ? (consideradoCount / recommendations.length * 100) + '%' : '0%' }"
                      ></div>
                    </div>
                  </div>
                  <div class="text-center p-3 bg-red-50 rounded-xl border border-red-200">
                    <span class="block text-2xl font-bold text-red-500">{{ noAptoCount }}</span>
                    <span class="text-xs font-medium text-red-600">NO APTO</span>
                    <div class="mt-2 w-full bg-red-200 rounded-full h-1.5">
                      <div
                        class="bg-red-500 h-1.5 rounded-full transition-all duration-500"
                        :style="{ width: recommendations.length ? (noAptoCount / recommendations.length * 100) + '%' : '0%' }"
                      ></div>
                    </div>
                  </div>
                </div>

                <!-- Tipos + convenio EMI -->
                <div class="mt-4 pt-4 border-t border-gray-100 flex items-center gap-5 text-sm">
                  <span class="flex items-center gap-1.5 text-gray-600">
                    <span class="w-2.5 h-2.5 rounded-full bg-purple-400 flex-shrink-0"></span>
                    <strong class="text-gray-900">{{ pasantiaCount }}</strong> pasantías
                  </span>
                  <span class="flex items-center gap-1.5 text-gray-600">
                    <span class="w-2.5 h-2.5 rounded-full bg-emi-navy-400 flex-shrink-0"></span>
                    <strong class="text-gray-900">{{ laboralCount }}</strong> empleos
                  </span>
                  <span class="ml-auto inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emi-navy-50 text-emi-navy-600 text-xs font-medium border border-emi-navy-200">
                    <svg class="h-3.5 w-3.5 text-emi-gold-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                    </svg>
                    Convenio EMI
                  </span>
                </div>
              </Card>

              <!-- Skills más solicitados (faltantes) -->
              <Card>
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
                  Skills más solicitados
                </h3>
                <div v-if="topMissingSkills.length > 0" class="space-y-2.5">
                  <div v-for="item in topMissingSkills" :key="item.skill">
                    <div class="flex justify-between items-center mb-1">
                      <span class="text-xs font-medium text-gray-700 truncate">{{ item.skill }}</span>
                      <span class="text-xs text-gray-400 flex-shrink-0 ml-2">{{ item.count }}/{{ recommendations.length }}</span>
                    </div>
                    <div class="w-full bg-gray-100 rounded-full h-1.5">
                      <div
                        class="bg-emi-navy-400 h-1.5 rounded-full transition-all duration-500"
                        :style="{ width: (item.count / recommendations.length * 100) + '%' }"
                      ></div>
                    </div>
                  </div>
                  <p class="pt-1 text-xs text-gray-400">Frecuencia en ofertas disponibles</p>
                </div>
                <p v-else class="text-sm text-gray-400 italic">Sin datos de skills faltantes</p>
              </Card>
            </div>
            <!-- ─────────────────────────────────────────────────────────────── -->

            <!-- No Recommendations -->
            <Card v-if="recommendations.length === 0" class="text-center py-12">
              <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 class="mt-4 text-lg font-semibold text-gray-900">No hay recomendaciones disponibles</h3>
              <p class="mt-2 text-gray-500">
                No hay {{ userRole === 'estudiante' ? 'pasantias' : ['admin', 'administrador'].includes(userRole) ? 'pasantias ni empleos' : 'empleos' }} activos en este momento.
              </p>
              <div class="mt-4 space-y-2">
                <p class="text-sm text-gray-400">Posibles razones:</p>
                <ul class="text-sm text-gray-400 list-disc list-inside">
                  <li>No hay ofertas publicadas para tu perfil</li>
                  <li>Tu perfil necesita mas informacion</li>
                  <li>El sistema esta procesando las ofertas</li>
                </ul>
              </div>
              <div class="mt-6 flex justify-center gap-4">
                <router-link
                  to="/digitalizacion/mi-perfil"
                  class="inline-flex items-center gap-2 px-4 py-2 border border-emi-navy-300 text-emi-navy-600 rounded-lg hover:bg-emi-navy-50 transition-colors"
                >
                  Revisar Mi Perfil
                </router-link>
                <button @click="loadRecommendations(true)" class="btn-emi-primary">
                  Reintentar
                </button>
              </div>
            </Card>

            <!-- Lista con filtros -->
            <div v-else>
              <!-- Tabs de filtro -->
              <div class="flex items-center gap-2 mb-4 flex-wrap">
                <button
                  v-for="tab in [
                    { key: 'todos',    label: 'Todos',      count: recommendations.length },
                    { key: 'pasantia', label: 'Pasantías',  count: pasantiaCount },
                    { key: 'laboral',  label: 'Empleos',    count: laboralCount }
                  ]"
                  :key="tab.key"
                  @click="activeFilter = tab.key"
                  :class="[
                    'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                    activeFilter === tab.key
                      ? 'bg-emi-navy-500 text-white shadow-sm'
                      : 'bg-white text-gray-600 border border-gray-200 hover:border-emi-navy-300 hover:text-emi-navy-500'
                  ]"
                >
                  {{ tab.label }}
                  <span :class="[
                    'text-xs px-1.5 py-0.5 rounded-full font-semibold',
                    activeFilter === tab.key ? 'bg-white/25 text-white' : 'bg-gray-100 text-gray-500'
                  ]">{{ tab.count }}</span>
                </button>
              </div>

              <!-- Sin resultados para el filtro activo -->
              <p v-if="filteredRecommendations.length === 0" class="text-center py-10 text-gray-400">
                No hay {{ activeFilter === 'pasantia' ? 'pasantías' : 'empleos' }} disponibles en este momento.
              </p>

              <!-- Lista -->
              <div v-else class="space-y-4">
                <RecommendationCard
                  v-for="rec in filteredRecommendations"
                  :key="rec.id"
                  :rec="rec"
                  :expanded="expandedId === rec.id"
                  :formatScoreLabel="formatScoreLabel"
                  :formatDate="formatDate"
                  @toggle="toggleExpand"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommendations Panel (derecho) -->
      <RecommendationsSidebar
        v-model:isOpen="isSecondarySidebarOpen"
        :bestMatch="bestMatch"
        :perfilSummary="perfilSummary"
        :totalCount="recommendations.length"
        :newCount="newCount"
        :aptoCount="aptoCount"
        :consideradoCount="consideradoCount"
        :refreshing="refreshing"
        @refresh="loadRecommendations(true)"
      />
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import RecommendationsSidebar from '../components/RecommendationsSidebar.vue'
import RecommendationCard from '../components/RecommendationCard.vue'
import EligibilityWarning from '../components/EligibilityWarning.vue'
import { useRecommendations } from '../composables/useRecommendations'

const isSecondarySidebarOpen = ref(true)
const activeFilter = ref('todos')

const {
  recommendations,
  perfilSummary,
  loading,
  refreshing,
  error,
  isEligible,
  eligibilityReason,
  eligibilityAction,
  missingFields,
  expandedId,
  userRole,
  newCount,
  aptoCount,
  consideradoCount,
  bestMatch,
  formatScoreLabel,
  formatDate,
  toggleExpand,
  loadRecommendations
} = useRecommendations()

// --- Conteos derivados
const noAptoCount = computed(() =>
  Math.max(0, recommendations.value.length - (aptoCount.value || 0) - (consideradoCount.value || 0))
)

const pasantiaCount = computed(() =>
  recommendations.value.filter(r => (r.oferta?.tipo || '').toLowerCase().includes('pasant')).length
)

const laboralCount = computed(() =>
  recommendations.value.filter(r => {
    const t = (r.oferta?.tipo || '').toLowerCase()
    return t.includes('laboral') || t.includes('empleo')
  }).length
)

// Top skills faltantes agregados de todas las recomendaciones
const topMissingSkills = computed(() => {
  const freq = {}
  for (const rec of recommendations.value) {
    const missing = rec.match_details?.hard_skills?.missing || []
    for (const skill of missing) {
      freq[skill] = (freq[skill] || 0) + 1
    }
  }
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([skill, count]) => ({ skill, count }))
})

// Lista filtrada por tipo de oferta
const filteredRecommendations = computed(() => {
  if (activeFilter.value === 'todos') return recommendations.value
  return recommendations.value.filter(rec => {
    const tipo = (rec.oferta?.tipo || '').toLowerCase()
    if (activeFilter.value === 'pasantia') return tipo.includes('pasant')
    if (activeFilter.value === 'laboral') return tipo.includes('laboral') || tipo.includes('empleo')
    return true
  })
})
</script>
