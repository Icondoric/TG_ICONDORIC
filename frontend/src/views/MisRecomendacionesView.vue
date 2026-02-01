<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Mis Recomendaciones</h1>
        <p class="mt-2 text-gray-600">
          {{ userRole === 'estudiante' ? 'Pasantias recomendadas' : 'Empleos recomendados' }} basados en tu perfil
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Not Eligible -->
      <div v-else-if="!isEligible" class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <div class="flex">
          <svg class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div class="ml-3">
            <h3 class="text-lg font-medium text-yellow-800">{{ eligibilityReason }}</h3>
            <p v-if="eligibilityAction" class="mt-2 text-yellow-700">{{ eligibilityAction }}</p>

            <!-- Missing Fields -->
            <div v-if="missingFields.length > 0" class="mt-4">
              <p class="text-sm text-yellow-700 mb-2">Campos faltantes:</p>
              <ul class="list-disc list-inside text-sm text-yellow-600">
                <li v-for="field in missingFields" :key="field">{{ field }}</li>
              </ul>
            </div>

            <router-link
              to="/subir-cv"
              class="mt-4 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700"
            >
              Completar Perfil
            </router-link>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
        <button @click="loadRecommendations" class="mt-2 text-red-600 hover:text-red-800 underline">
          Reintentar
        </button>
      </div>

      <!-- Results -->
      <div v-else>
        <!-- Stats Bar -->
        <div class="bg-white rounded-lg shadow p-4 mb-6">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-6">
              <div>
                <span class="text-2xl font-bold text-gray-900">{{ recommendations.length }}</span>
                <span class="text-gray-500 ml-1">recomendaciones</span>
              </div>
              <div v-if="newCount > 0" class="flex items-center">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ newCount }} nuevas
                </span>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="loadRecommendations(true)"
                :disabled="refreshing"
                class="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                <svg :class="['h-4 w-4 mr-2', refreshing ? 'animate-spin' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {{ refreshing ? 'Actualizando...' : 'Actualizar' }}
              </button>
            </div>
          </div>

          <!-- Profile Summary -->
          <div v-if="perfilSummary" class="mt-4 pt-4 border-t border-gray-200">
            <p class="text-sm text-gray-500">
              Basado en tu perfil:
              <span class="font-medium text-gray-700">{{ perfilSummary.top_skills?.slice(0, 3).join(', ') }}</span>
              <span v-if="perfilSummary.experience_years"> - {{ perfilSummary.experience_years }} anos exp.</span>
            </p>
          </div>
        </div>

        <!-- No Recommendations -->
        <div v-if="recommendations.length === 0" class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No hay recomendaciones disponibles</h3>
          <p class="mt-2 text-gray-500">
            No hay {{ userRole === 'estudiante' ? 'pasantias' : 'empleos' }} activos en este momento.
          </p>
        </div>

        <!-- Recommendations List -->
        <div v-else class="space-y-4">
          <div
            v-for="rec in recommendations"
            :key="rec.id"
            class="bg-white rounded-lg shadow hover:shadow-md transition-shadow"
          >
            <!-- Main Card -->
            <div class="p-6">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <!-- Institution & Title -->
                  <div class="flex items-center gap-3 mb-2">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      rec.clasificacion === 'APTO' ? 'bg-green-100 text-green-800' :
                      rec.clasificacion === 'CONSIDERADO' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]">
                      {{ rec.clasificacion }}
                    </span>
                    <span v-if="!rec.fue_vista" class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                      Nueva
                    </span>
                  </div>

                  <h3 class="text-lg font-semibold text-gray-900">{{ rec.oferta?.titulo }}</h3>

                  <div class="flex items-center gap-4 mt-2 text-sm text-gray-600">
                    <span v-if="rec.oferta?.institution_name" class="flex items-center">
                      <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      {{ rec.oferta.institution_name }}
                    </span>
                    <span v-if="rec.oferta?.sector" class="text-gray-400">
                      {{ rec.oferta.sector }}
                    </span>
                    <span v-if="rec.oferta?.modalidad" class="flex items-center">
                      <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      </svg>
                      {{ rec.oferta.modalidad }}
                    </span>
                  </div>
                </div>

                <!-- Match Score -->
                <div class="text-center ml-6">
                  <div :class="[
                    'w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold',
                    rec.match_score >= 0.7 ? 'bg-green-100 text-green-700' :
                    rec.match_score >= 0.5 ? 'bg-yellow-100 text-yellow-700' :
                    'bg-red-100 text-red-700'
                  ]">
                    {{ Math.round(rec.match_score * 100) }}%
                  </div>
                  <p class="text-xs text-gray-500 mt-1">Match</p>
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
                    <span
                      v-for="f in rec.fortalezas.slice(0, 2)"
                      :key="f"
                      class="px-2 py-0.5 bg-green-50 text-green-700 rounded text-xs"
                    >
                      {{ f }}
                    </span>
                  </div>
                </div>
                <div v-if="rec.debilidades?.length > 0">
                  <span class="text-xs text-gray-500">Areas de mejora:</span>
                  <div class="flex flex-wrap gap-1 mt-1">
                    <span
                      v-for="d in rec.debilidades.slice(0, 2)"
                      :key="d"
                      class="px-2 py-0.5 bg-orange-50 text-orange-700 rounded text-xs"
                    >
                      {{ d }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Expand Button -->
              <button
                @click="toggleExpand(rec.id)"
                class="mt-4 text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center"
              >
                {{ expandedId === rec.id ? 'Ver menos' : 'Ver detalles' }}
                <svg :class="['h-4 w-4 ml-1 transition-transform', expandedId === rec.id ? 'rotate-180' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>

            <!-- Expanded Details -->
            <div v-if="expandedId === rec.id" class="px-6 pb-6 border-t border-gray-100">
              <div class="pt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Left: Scores -->
                <div>
                  <h4 class="font-medium text-gray-900 mb-3">Detalle de Scores</h4>
                  <div class="space-y-3">
                    <div v-for="(value, key) in rec.scores_detalle" :key="key">
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-gray-600">{{ formatScoreLabel(key) }}</span>
                        <span class="font-medium">{{ Math.round(value * 100) }}%</span>
                      </div>
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div
                          class="h-2 rounded-full transition-all"
                          :class="value >= 0.7 ? 'bg-green-500' : value >= 0.5 ? 'bg-yellow-500' : 'bg-red-500'"
                          :style="{ width: `${value * 100}%` }"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Right: Oferta Details -->
                <div>
                  <h4 class="font-medium text-gray-900 mb-3">Detalles de la Oferta</h4>
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
              <div class="mt-6 p-4 bg-blue-50 rounded-lg">
                <p class="text-sm text-blue-800">
                  <strong>Nota:</strong> Para postular a esta oferta, contacta a la Unidad de Vinculacion de la EMI.
                  Este sistema solo genera recomendaciones de correspondencia.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getMyRecommendations, checkRecommendationEligibility, markRecommendationViewed } from '../services/api'

const authStore = useAuthStore()

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

const userRole = computed(() => authStore.user?.rol || 'estudiante')
const newCount = computed(() => recommendations.value.filter(r => !r.fue_vista).length)

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
