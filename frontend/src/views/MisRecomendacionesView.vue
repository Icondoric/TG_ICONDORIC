<template>
  <StudentLayout>
    <div class="flex">
      <!-- Secondary Sidebar (Recommendations Info) -->
      <CollapsibleSidebar 
        v-model:isOpen="isSecondarySidebarOpen" 
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
            <GaugeChart
              :value="0"
              size="lg"
              label="Sin recomendaciones"
            />
          </div>

          <!-- Stats Summary -->
          <div class="mb-6 p-4 bg-emi-navy-50 rounded-xl border border-emi-navy-100">
            <h3 class="text-sm font-semibold text-emi-navy-700 mb-3">Resumen</h3>
            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Total</span>
                <Badge variant="navy" size="sm">{{ recommendations.length }}</Badge>
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
                  <Badge
                    v-for="skill in perfilSummary.top_skills.slice(0, 4)"
                    :key="skill"
                    variant="navy"
                    size="sm"
                  >
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

          <!-- Filter/Actions -->
          <div class="space-y-3 pt-4 border-t border-gray-100">
            <button
              @click="loadRecommendations(true)"
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
                        <span class="text-xs font-bold text-emi-navy-600">{{ recommendations.length }}</span>
                        <div class="w-1 h-1 rounded-full bg-emi-navy-500 mt-0.5"></div>
                     </div>
                </div>
            </div>
        </template>
      </CollapsibleSidebar>

      <!-- Main Content Container with Dynamic Margin -->
      <div 
        class="flex-1 transition-[margin] duration-300 ease-in-out min-h-screen"
        :style="{ marginLeft: isSecondarySidebarOpen ? '280px' : '60px' }"
      >
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- Header -->
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-emi-navy-500">Mis Recomendaciones</h1>
            <p class="mt-2 text-gray-600">
              {{ userRole === 'estudiante' ? 'Pasantias recomendadas' : 'Empleos recomendados' }} basados en tu perfil
            </p>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
          </div>

          <!-- Not Eligible -->
          <Card v-else-if="!isEligible" class="border-emi-gold-200 bg-emi-gold-50">
            <div class="flex items-start gap-4">
              <div class="p-3 bg-emi-gold-100 rounded-full">
                <svg class="h-6 w-6 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-emi-gold-800">{{ eligibilityReason }}</h3>
                <p v-if="eligibilityAction" class="mt-2 text-emi-gold-700">{{ eligibilityAction }}</p>

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

            <!-- No Recommendations -->
            <Card v-if="recommendations.length === 0" class="text-center py-12">
              <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 class="mt-4 text-lg font-semibold text-gray-900">No hay recomendaciones disponibles</h3>
              <p class="mt-2 text-gray-500">
                No hay {{ userRole === 'estudiante' ? 'pasantias' : 'empleos' }} activos en este momento.
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
                  to="/mi-perfil"
                  class="inline-flex items-center gap-2 px-4 py-2 border border-emi-navy-300 text-emi-navy-600 rounded-lg hover:bg-emi-navy-50 transition-colors"
                >
                  Revisar Mi Perfil
                </router-link>
                <button
                  @click="loadRecommendations(true)"
                  class="btn-emi-primary"
                >
                  Reintentar
                </button>
              </div>
            </Card>

            <!-- Recommendations List -->
            <div v-else class="space-y-4">
              <Card
                v-for="rec in recommendations"
                :key="rec.id"
                :hoverable="true"
                class="overflow-visible"
              >
                <!-- Main Card Content -->
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <!-- Badges Row -->
                    <div class="flex items-center gap-2 mb-3">
                      <Badge
                        :variant="rec.clasificacion === 'APTO' ? 'gold' : rec.clasificacion === 'CONSIDERADO' ? 'navy' : 'danger'"
                      >
                        {{ rec.clasificacion }}
                      </Badge>
                      <Badge v-if="!rec.fue_vista" variant="navy" size="sm">
                        Nueva
                      </Badge>
                    </div>

                    <!-- Title -->
                    <h3 class="text-lg font-semibold text-gray-900">{{ rec.oferta?.titulo }}</h3>

                    <!-- Meta Info -->
                    <div class="flex flex-wrap items-center gap-4 mt-2 text-sm text-gray-600">
                      <span v-if="rec.oferta?.institution_name" class="flex items-center gap-1">
                        <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                        {{ rec.oferta.institution_name }}
                      </span>
                      <span v-if="rec.oferta?.sector" class="text-gray-400">
                        {{ rec.oferta.sector }}
                      </span>
                      <span v-if="rec.oferta?.modalidad" class="flex items-center gap-1">
                        <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        </svg>
                        {{ rec.oferta.modalidad }}
                      </span>
                    </div>
                  </div>

                  <!-- Match Score Circle -->
                  <div class="ml-4 flex-shrink-0">
                    <div
                      :class="[
                        'w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold border-4',
                        rec.match_score >= 0.7
                          ? 'bg-emi-gold-50 text-emi-gold-600 border-emi-gold-200'
                          : rec.match_score >= 0.5
                            ? 'bg-emi-navy-50 text-emi-navy-600 border-emi-navy-200'
                            : 'bg-red-50 text-red-600 border-red-200'
                      ]"
                    >
                      {{ Math.round(rec.match_score * 100) }}%
                    </div>
                    <p class="text-xs text-gray-500 text-center mt-1">Match</p>
                  </div>
                </div>

                <!-- Description -->
                <p v-if="rec.oferta?.descripcion" class="mt-4 text-gray-600 text-sm line-clamp-2">
                  {{ rec.oferta.descripcion }}
                </p>

                <!-- Strengths & Weaknesses -->
                <div class="mt-4 flex flex-wrap gap-4">
                  <div v-if="rec.fortalezas?.length > 0">
                    <span class="text-xs text-gray-500">Fortalezas:</span>
                    <div class="flex flex-wrap gap-1 mt-1">
                      <Badge
                        v-for="f in rec.fortalezas.slice(0, 2)"
                        :key="f"
                        variant="gold"
                        size="sm"
                      >
                        {{ f }}
                      </Badge>
                    </div>
                  </div>
                  <div v-if="rec.debilidades?.length > 0">
                    <span class="text-xs text-gray-500">Areas de mejora:</span>
                    <div class="flex flex-wrap gap-1 mt-1">
                      <Badge
                        v-for="d in rec.debilidades.slice(0, 2)"
                        :key="d"
                        variant="neutral"
                        size="sm"
                      >
                        {{ d }}
                      </Badge>
                    </div>
                  </div>
                </div>

                <!-- Expand Button -->
                <button
                  @click="toggleExpand(rec.id)"
                  class="mt-4 text-emi-navy-500 hover:text-emi-gold-500 text-sm font-medium flex items-center transition-colors"
                >
                  {{ expandedId === rec.id ? 'Ver menos' : 'Ver detalles' }}
                  <svg :class="['h-4 w-4 ml-1 transition-transform', expandedId === rec.id ? 'rotate-180' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                <!-- Expanded Details -->
                <div v-if="expandedId === rec.id" class="mt-4 pt-4 border-t border-gray-100">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Left: Scores -->
                    <div>
                      <h4 class="font-semibold text-gray-900 mb-3">Detalle de Scores</h4>
                      <div class="space-y-3">
                        <div v-for="(value, key) in rec.scores_detalle" :key="key">
                          <ProgressBar
                            :value="value * 100"
                            :label="formatScoreLabel(key)"
                          />
                        </div>
                      </div>
                    </div>

                    <!-- Right: Oferta Details -->
                    <div>
                      <h4 class="font-semibold text-gray-900 mb-3">Detalles de la Oferta</h4>
                      <dl class="space-y-2 text-sm">
                        <div v-if="rec.oferta?.tipo" class="flex">
                          <dt class="text-gray-500 w-24">Tipo:</dt>
                          <dd class="text-gray-900 capitalize">{{ rec.oferta.tipo }}</dd>
                        </div>
                        <div v-if="rec.oferta?.ubicacion" class="flex">
                          <dt class="text-gray-500 w-24">Ubicacion:</dt>
                          <dd class="text-gray-900">{{ rec.oferta.ubicacion }}</dd>
                        </div>
                        <div v-if="rec.oferta?.cupos_disponibles" class="flex">
                          <dt class="text-gray-500 w-24">Cupos:</dt>
                          <dd class="text-gray-900">{{ rec.oferta.cupos_disponibles }}</dd>
                        </div>
                        <div v-if="rec.oferta?.fecha_cierre" class="flex">
                          <dt class="text-gray-500 w-24">Cierre:</dt>
                          <dd class="text-gray-900">{{ formatDate(rec.oferta.fecha_cierre) }}</dd>
                        </div>
                      </dl>
                    </div>
                  </div>

                  <!-- Action Note -->
                  <div class="mt-6 p-4 bg-emi-navy-50 rounded-xl">
                    <p class="text-sm text-emi-navy-700">
                      <strong>Nota:</strong> Para postular a esta oferta, contacta a la Unidad de Vinculacion de la EMI.
                      Este sistema solo genera recomendaciones de correspondencia.
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useUiStore } from '../stores/ui'
import { getMyRecommendations, checkRecommendationEligibility, markRecommendationViewed } from '../services/api'
import StudentLayout from '../components/student/StudentLayout.vue'
import CollapsibleSidebar from '../components/ui/CollapsibleSidebar.vue'
import Card from '../components/ui/Card.vue'
import Badge from '../components/ui/Badge.vue'
import GaugeChart from '../components/ui/GaugeChart.vue'
import ProgressBar from '../components/ui/ProgressBar.vue'

const authStore = useAuthStore()
const uiStore = useUiStore()
const isSecondarySidebarOpen = ref(true)

const recommendations = ref([])
const perfilSummary = ref(null)
const loading = ref(true)
const refreshing = ref(false)
const error = ref(null)
const isEligible = ref(true)
const eligibilityReason = ref('')
const eligibilityAction = ref('')
const missingFields = ref([])
const expandedId = ref(null)
const isMobileSidebarOpen = ref(false)

const userRole = computed(() => authStore.user?.rol || 'estudiante')
const newCount = computed(() => recommendations.value.filter(r => !r.fue_vista).length)
const aptoCount = computed(() => recommendations.value.filter(r => r.clasificacion === 'APTO').length)
const consideradoCount = computed(() => recommendations.value.filter(r => r.clasificacion === 'CONSIDERADO').length)
const bestMatch = computed(() => {
  if (recommendations.value.length === 0) return null
  return recommendations.value.reduce((best, rec) =>
    rec.match_score > (best?.match_score || 0) ? rec : best
  , null)
})

const formatScoreLabel = (key) => {
  const labels = {
    hard_skills_score: 'Habilidades Tecnicas',
    soft_skills_score: 'Habilidades Blandas',
    education_score: 'Formacion Academica',
    experience_score: 'Experiencia',
    languages_score: 'Idiomas'
  }
  return labels[key] || key
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const toggleExpand = async (recId) => {
  if (expandedId.value === recId) {
    expandedId.value = null
  } else {
    expandedId.value = recId

    // Mark as viewed
    const rec = recommendations.value.find(r => r.id === recId)
    if (rec && !rec.fue_vista) {
      try {
        await markRecommendationViewed(recId)
        rec.fue_vista = true
      } catch (e) {
        console.error('Error marking as viewed:', e)
      }
    }
  }
}

const checkEligibility = async () => {
  try {
    const result = await checkRecommendationEligibility()

    isEligible.value = result.eligible
    eligibilityReason.value = result.reason || ''
    eligibilityAction.value = result.action_required || ''
    missingFields.value = result.missing_fields || []

    return result.eligible
  } catch (e) {
    // If error, assume eligible and let loadRecommendations handle it
    return true
  }
}

const loadRecommendations = async (forceRefresh = false) => {
  if (forceRefresh) {
    refreshing.value = true
  } else {
    loading.value = true
  }
  error.value = null

  try {
    // Check eligibility first
    const eligible = await checkEligibility()

    if (!eligible) {
      loading.value = false
      refreshing.value = false
      return
    }

    // Get recommendations
    const result = await getMyRecommendations({
      top_n: 20,
      recalcular: forceRefresh
    })

    recommendations.value = result.recomendaciones || []
    perfilSummary.value = result.perfil_summary

  } catch (e) {
    error.value = e.response?.data?.detail || 'Error cargando recomendaciones'
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

onMounted(() => {
  loadRecommendations()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
