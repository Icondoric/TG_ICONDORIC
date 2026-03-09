<template>
  <AppLayout>
    <div class="flex-1 min-w-0">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- Header -->
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-emi-navy-500">Historial de Postulaciones</h1>
          <p class="mt-2 text-gray-600">
            Revisa todas tus postulaciones y el resultado de cada análisis de compatibilidad
          </p>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
        </div>

        <!-- Sin elegibilidad -->
        <EligibilityWarning
          v-else-if="!isEligible"
          :reason="eligibilityReason"
          :action="eligibilityAction"
          :missingFields="missingFields"
        />

        <!-- Sin postulaciones -->
        <Card v-else-if="postulaciones.length === 0" class="text-center py-12">
          <svg class="mx-auto h-14 w-14 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="text-gray-500 mb-4">Aún no te has postulado a ninguna oferta</p>
          <router-link to="/mis-recomendaciones" class="btn-emi-primary">
            Explorar Ofertas
          </router-link>
        </Card>

        <!-- Contenido -->
        <div v-else>

          <!-- Resumen APTO / CONSIDERADO / NO APTO -->
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div class="text-center p-3 bg-emi-gold-50 rounded-xl border border-emi-gold-200">
              <span class="block text-2xl font-bold text-emi-gold-600">{{ aptoCount }}</span>
              <span class="text-xs font-medium text-emi-gold-700">APTO</span>
              <div class="mt-2 w-full bg-emi-gold-200 rounded-full h-1.5">
                <div class="bg-emi-gold-500 h-1.5 rounded-full transition-all duration-500"
                  :style="{ width: (aptoCount / postulaciones.length * 100) + '%' }"/>
              </div>
            </div>
            <div class="text-center p-3 bg-emi-navy-50 rounded-xl border border-emi-navy-200">
              <span class="block text-2xl font-bold text-emi-navy-600">{{ consideradoCount }}</span>
              <span class="text-xs font-medium text-emi-navy-700">CONSIDERADO</span>
              <div class="mt-2 w-full bg-emi-navy-200 rounded-full h-1.5">
                <div class="bg-emi-navy-500 h-1.5 rounded-full transition-all duration-500"
                  :style="{ width: (consideradoCount / postulaciones.length * 100) + '%' }"/>
              </div>
            </div>
            <div class="text-center p-3 bg-red-50 rounded-xl border border-red-200">
              <span class="block text-2xl font-bold text-red-500">{{ noAptoCount }}</span>
              <span class="text-xs font-medium text-red-600">NO APTO</span>
              <div class="mt-2 w-full bg-red-200 rounded-full h-1.5">
                <div class="bg-red-500 h-1.5 rounded-full transition-all duration-500"
                  :style="{ width: (noAptoCount / postulaciones.length * 100) + '%' }"/>
              </div>
            </div>
          </div>

          <!-- Cards -->
          <div class="space-y-4">
            <Card
              v-for="p in postulaciones"
              :key="p.id"
              class="hover:shadow-md transition-shadow"
            >
              <!-- Fila principal -->
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap mb-1.5">
                    <Badge :variant="p.oferta?.tipo === 'pasantia' ? 'purple' : 'navy'">
                      {{ p.oferta?.tipo === 'pasantia' ? 'Pasantía' : 'Empleo' }}
                    </Badge>
                    <span v-if="p.oferta?.modalidad"
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-600">
                      {{ p.oferta.modalidad }}
                    </span>
                  </div>
                  <h3 class="text-base font-semibold text-gray-900">{{ p.oferta?.titulo || 'Oferta' }}</h3>
                  <p v-if="p.oferta?.institution_name" class="text-sm text-gray-500 mt-0.5">
                    {{ p.oferta.institution_name }}
                    <span v-if="p.oferta?.sector" class="text-gray-400"> · {{ p.oferta.sector }}</span>
                  </p>
                </div>

                <!-- Puntaje -->
                <div class="flex-shrink-0 text-right">
                  <Badge :variant="p.clasificacion === 'APTO' ? 'gold' : p.clasificacion === 'CONSIDERADO' ? 'navy' : 'danger'">
                    {{ p.clasificacion }}
                  </Badge>
                  <div :class="[
                    'text-3xl font-bold mt-1',
                    p.clasificacion === 'APTO' ? 'text-emi-gold-600'
                      : p.clasificacion === 'CONSIDERADO' ? 'text-emi-navy-600'
                      : 'text-red-500'
                  ]">
                    {{ Math.round(p.match_score * 100) }}%
                  </div>
                </div>
              </div>

              <!-- "Ver detalles" -->
              <div class="mt-3 pt-3 border-t border-gray-100 flex items-center justify-between">
                <button
                  @click="toggleExpand(p.id)"
                  class="inline-flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors"
                >
                  <svg
                    :class="['h-4 w-4 transition-transform duration-200', expandedId === p.id ? 'rotate-180' : '']"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                  {{ expandedId === p.id ? 'Ocultar detalles' : 'Ver detalles' }}
                </button>
                <span class="text-xs text-gray-400">Postulado {{ formatDate(p.created_at) }}</span>
              </div>

              <!-- Panel expandible -->
              <div v-if="expandedId === p.id" class="mt-4 pt-2">

                <!-- Info de la oferta -->
                <div class="space-y-4">
                  <div class="flex items-center gap-2">
                    <div class="flex-1 h-px bg-gray-200"></div>
                    <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2">Información de la oferta</span>
                    <div class="flex-1 h-px bg-gray-200"></div>
                  </div>

                  <p v-if="p.oferta?.descripcion" class="text-sm text-gray-700 leading-relaxed">
                    {{ p.oferta.descripcion }}
                  </p>

                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div v-if="p.oferta?.institution_name" class="bg-gray-50 rounded-lg p-3">
                      <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Institución</h4>
                      <p class="text-sm font-medium text-gray-800">{{ p.oferta.institution_name }}</p>
                      <p v-if="p.oferta.sector" class="text-xs text-gray-500 mt-0.5">{{ p.oferta.sector }}</p>
                      <div class="mt-2 space-y-1">
                        <a v-if="p.oferta.contact_email" :href="'mailto:' + p.oferta.contact_email"
                          class="flex items-center gap-1.5 text-xs text-blue-600 hover:underline">
                          <svg class="h-3.5 w-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                          </svg>
                          {{ p.oferta.contact_email }}
                        </a>
                        <p v-if="p.oferta.contact_phone" class="flex items-center gap-1.5 text-xs text-gray-600">
                          <svg class="h-3.5 w-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                          </svg>
                          {{ p.oferta.contact_phone }}
                        </p>
                      </div>
                    </div>

                    <div class="bg-gray-50 rounded-lg p-3">
                      <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Detalles</h4>
                      <dl class="space-y-1.5">
                        <div v-if="p.oferta?.modalidad" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Modalidad</dt>
                          <dd class="text-xs text-gray-700 capitalize">{{ p.oferta.modalidad }}</dd>
                        </div>
                        <div v-if="p.oferta?.ubicacion" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Ubicación</dt>
                          <dd class="text-xs text-gray-700">{{ p.oferta.ubicacion }}</dd>
                        </div>
                        <div v-if="p.oferta?.area" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Área</dt>
                          <dd class="text-xs text-gray-700">{{ p.oferta.area }}</dd>
                        </div>
                        <div v-if="p.oferta?.cupos_disponibles" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Cupos</dt>
                          <dd class="text-xs text-gray-700">{{ p.oferta.cupos_disponibles }}</dd>
                        </div>
                        <div v-if="p.oferta?.fecha_cierre" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Cierre</dt>
                          <dd class="text-xs text-gray-700 font-medium">{{ formatDate(p.oferta.fecha_cierre) }}</dd>
                        </div>
                      </dl>
                    </div>
                  </div>
                </div>

                <!-- Análisis de compatibilidad -->
                <div class="flex items-center gap-2 mt-6 mb-4">
                  <div class="flex-1 h-px bg-gray-200"></div>
                  <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2">
                    Análisis de Compatibilidad
                  </span>
                  <div class="flex-1 h-px bg-gray-200"></div>
                </div>

                <div v-if="p.scores_detalle" class="mb-4">
                  <h4 class="font-semibold text-gray-900 mb-3">Detalle de Scores</h4>
                  <div class="space-y-3">
                    <div v-for="(value, key) in p.scores_detalle" :key="key">
                      <ProgressBar :value="value * 100" :label="formatScoreLabel(key)" />
                    </div>
                  </div>
                </div>

                <MatchDetailSection
                  v-if="p.match_details"
                  :matchDetails="p.match_details"
                  :clasificacion="p.clasificacion"
                />

              </div>
            </Card>
          </div>

        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'
import EligibilityWarning from '../components/EligibilityWarning.vue'
import MatchDetailSection from '../components/MatchDetailSection.vue'
import { getMyPostulaciones } from '../api/postulaciones.api'
import { checkRecommendationEligibility } from '../api/recommendations.api'

// ── Estado ─────────────────────────────────────────────
const loading = ref(true)
const isEligible = ref(true)
const eligibilityReason = ref('')
const eligibilityAction = ref('')
const missingFields = ref([])
const postulaciones = ref([])
const expandedId = ref(null)

// ── Computed ───────────────────────────────────────────
const aptoCount      = computed(() => postulaciones.value.filter(p => p.clasificacion === 'APTO').length)
const consideradoCount = computed(() => postulaciones.value.filter(p => p.clasificacion === 'CONSIDERADO').length)
const noAptoCount    = computed(() => postulaciones.value.filter(p => p.clasificacion === 'NO_APTO').length)

// ── Helpers ────────────────────────────────────────────
const toggleExpand = (id) => { expandedId.value = expandedId.value === id ? null : id }

const formatScoreLabel = (key) => ({
  hard_skills_score: 'Habilidades Técnicas',
  soft_skills_score: 'Habilidades Blandas',
  education_score:   'Formación Académica',
  experience_score:  'Experiencia',
  languages_score:   'Idiomas'
}[key] || key)

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}

// ── Ciclo de vida ──────────────────────────────────────
onMounted(async () => {
  try {
    const result = await checkRecommendationEligibility()
    isEligible.value = result.eligible
    eligibilityReason.value = result.reason || ''
    eligibilityAction.value = result.action_required || ''
    missingFields.value = result.missing_fields || []

    if (result.eligible) {
      const data = await getMyPostulaciones()
      postulaciones.value = data.postulaciones || []
    }
  } catch {
    // Si falla eligibility, igual intentamos cargar
    try {
      const data = await getMyPostulaciones()
      postulaciones.value = data.postulaciones || []
    } catch { /* silencioso */ }
  } finally {
    loading.value = false
  }
})
</script>
