<template>
  <AppLayout>
    <div class="flex-1 min-w-0">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- Header -->
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-emi-navy-500">Correspondencia entre Perfiles</h1>
          <p class="mt-2 text-gray-600">
            Explora las ofertas disponibles, analiza tu compatibilidad y postúlate
          </p>
        </div>

        <!-- Loading inicial -->
        <div v-if="loadingInit" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
        </div>

        <!-- Sin elegibilidad -->
        <EligibilityWarning
          v-else-if="!isEligible"
          :reason="eligibilityReason"
          :action="eligibilityAction"
          :missingFields="missingFields"
        />

        <!-- Contenido principal -->
        <div v-else>

          <div v-if="loadingOfertas" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
          </div>

          <Card v-else-if="ofertas.length === 0" class="text-center py-12">
            <svg class="mx-auto h-14 w-14 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <p class="text-gray-500">No hay ofertas disponibles en este momento</p>
          </Card>

          <div v-else>
            <!-- Filtros -->
            <div class="flex items-center gap-2 mb-4 flex-wrap">
              <button
                v-for="f in ofertaFilters"
                :key="f.key"
                @click="ofertaFilter = f.key"
                :class="[
                  'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  ofertaFilter === f.key
                    ? 'bg-emi-navy-500 text-white shadow-sm'
                    : 'bg-white text-gray-600 border border-gray-200 hover:border-emi-navy-300 hover:text-emi-navy-500'
                ]"
              >
                {{ f.label }}
                <span :class="[
                  'text-xs px-1.5 py-0.5 rounded-full font-semibold',
                  ofertaFilter === f.key ? 'bg-white/25 text-white' : 'bg-gray-100 text-gray-500'
                ]">{{ f.count }}</span>
              </button>
            </div>

            <p v-if="filteredOfertas.length === 0" class="text-center py-8 text-gray-400">
              No hay ofertas para el filtro seleccionado
            </p>

            <div v-else class="space-y-4">
              <Card
                v-for="oferta in filteredOfertas"
                :key="oferta.id"
                class="hover:shadow-md transition-shadow"
              >
                <!-- Fila principal -->
                <div class="flex items-start justify-between gap-4">

                  <!-- Info resumida -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 flex-wrap mb-1.5">
                      <Badge
                        :variant="oferta.tipo === 'pasantia' ? 'purple' : 'navy'"
                      >
                        {{ oferta.tipo === 'pasantia' ? 'Pasantía' : 'Empleo' }}
                      </Badge>
                      <span v-if="oferta.modalidad"
                        class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-600">
                        {{ oferta.modalidad }}
                      </span>
                      <span v-if="oferta.area"
                        class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-emi-gold-100 text-emi-gold-700">
                        {{ oferta.area }}
                      </span>
                    </div>

                    <h3 class="text-base font-semibold text-gray-900 leading-snug">{{ oferta.titulo }}</h3>
                    <p v-if="oferta.institution_name" class="text-sm text-gray-500 mt-0.5">
                      {{ oferta.institution_name }}
                      <span v-if="oferta.sector" class="text-gray-400"> · {{ oferta.sector }}</span>
                    </p>

                    <div class="mt-2 flex flex-wrap gap-3 text-xs text-gray-400">
                      <span v-if="oferta.ubicacion" class="flex items-center gap-1">
                        <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        </svg>
                        {{ oferta.ubicacion }}
                      </span>
                      <span v-if="oferta.cupos_disponibles" class="flex items-center gap-1">
                        <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {{ oferta.cupos_disponibles }} cupo{{ oferta.cupos_disponibles !== 1 ? 's' : '' }}
                      </span>
                      <span v-if="oferta.fecha_cierre" class="flex items-center gap-1">
                        <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Cierra {{ formatDate(oferta.fecha_cierre) }}
                      </span>
                    </div>
                  </div>

                  <!-- Puntaje (si ya postuló) o botón postular -->
                  <div class="flex-shrink-0 text-right">
                    <template v-if="getPostulacion(oferta.id)">
                      <Badge
                        :variant="getPostulacion(oferta.id).clasificacion === 'APTO' ? 'gold'
                          : getPostulacion(oferta.id).clasificacion === 'CONSIDERADO' ? 'navy' : 'danger'"
                      >
                        {{ getPostulacion(oferta.id).clasificacion }}
                      </Badge>
                      <div :class="[
                        'text-3xl font-bold leading-none mt-1',
                        getPostulacion(oferta.id).clasificacion === 'APTO' ? 'text-emi-gold-600'
                          : getPostulacion(oferta.id).clasificacion === 'CONSIDERADO' ? 'text-emi-navy-600'
                          : 'text-red-500'
                      ]">
                        {{ Math.round(getPostulacion(oferta.id).match_score * 100) }}%
                      </div>
                    </template>

                    <template v-else>
                      <button
                        @click="postular(oferta.id)"
                        :disabled="postulando === oferta.id"
                        class="inline-flex items-center gap-2 btn-emi-primary text-sm px-4 py-2 disabled:opacity-60 disabled:cursor-not-allowed"
                      >
                        <svg v-if="postulando === oferta.id" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                        </svg>
                        {{ postulando === oferta.id ? 'Analizando...' : 'Postularme' }}
                      </button>
                    </template>
                  </div>
                </div>

                <!-- "Ver detalles" siempre visible -->
                <div class="mt-3 pt-3 border-t border-gray-100 flex items-center justify-between">
                  <button
                    @click="toggleExpand(oferta.id)"
                    class="inline-flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    <svg
                      :class="['h-4 w-4 transition-transform duration-200', expandedId === oferta.id ? 'rotate-180' : '']"
                      fill="none" viewBox="0 0 24 24" stroke="currentColor"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                    {{ expandedId === oferta.id ? 'Ocultar detalles' : 'Ver detalles' }}
                  </button>
                  <span v-if="getPostulacion(oferta.id)" class="text-xs text-gray-400 italic">
                    Postulado · {{ formatDate(getPostulacion(oferta.id).created_at) }}
                  </span>
                </div>

                <!-- Panel expandible -->
                <div v-if="expandedId === oferta.id" class="mt-4 pt-2">

                  <!-- Información completa de la oferta -->
                  <div class="space-y-4">
                    <div class="flex items-center gap-2">
                      <div class="flex-1 h-px bg-gray-200"></div>
                      <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2">Información de la oferta</span>
                      <div class="flex-1 h-px bg-gray-200"></div>
                    </div>

                    <p v-if="oferta.descripcion" class="text-sm text-gray-700 leading-relaxed">
                      {{ oferta.descripcion }}
                    </p>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <!-- Institución -->
                      <div v-if="oferta.institution_name" class="bg-gray-50 rounded-lg p-3">
                        <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Institución</h4>
                        <p class="text-sm font-medium text-gray-800">{{ oferta.institution_name }}</p>
                        <p v-if="oferta.sector" class="text-xs text-gray-500 mt-0.5">{{ oferta.sector }}</p>
                        <div class="mt-2 space-y-1">
                          <a v-if="oferta.contact_email" :href="'mailto:' + oferta.contact_email"
                            class="flex items-center gap-1.5 text-xs text-blue-600 hover:underline">
                            <svg class="h-3.5 w-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                            </svg>
                            {{ oferta.contact_email }}
                          </a>
                          <p v-if="oferta.contact_phone" class="flex items-center gap-1.5 text-xs text-gray-600">
                            <svg class="h-3.5 w-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                            </svg>
                            {{ oferta.contact_phone }}
                          </p>
                        </div>
                      </div>

                      <!-- Detalles -->
                      <div class="bg-gray-50 rounded-lg p-3">
                        <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Detalles</h4>
                        <dl class="space-y-1.5">
                          <div v-if="oferta.modalidad" class="flex gap-2">
                            <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Modalidad</dt>
                            <dd class="text-xs text-gray-700 capitalize">{{ oferta.modalidad }}</dd>
                          </div>
                          <div v-if="oferta.ubicacion" class="flex gap-2">
                            <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Ubicación</dt>
                            <dd class="text-xs text-gray-700">{{ oferta.ubicacion }}</dd>
                          </div>
                          <div v-if="oferta.area" class="flex gap-2">
                            <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Área</dt>
                            <dd class="text-xs text-gray-700">{{ oferta.area }}</dd>
                          </div>
                          <div v-if="oferta.cupos_disponibles" class="flex gap-2">
                            <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Cupos</dt>
                            <dd class="text-xs text-gray-700">{{ oferta.cupos_disponibles }}</dd>
                          </div>
                          <div v-if="oferta.fecha_inicio" class="flex gap-2">
                            <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Inicio</dt>
                            <dd class="text-xs text-gray-700">{{ formatDate(oferta.fecha_inicio) }}</dd>
                          </div>
                          <div v-if="oferta.fecha_cierre" class="flex gap-2">
                            <dt class="text-xs text-gray-400 w-20 flex-shrink-0">Cierre</dt>
                            <dd class="text-xs text-gray-700 font-medium">{{ formatDate(oferta.fecha_cierre) }}</dd>
                          </div>
                        </dl>
                      </div>
                    </div>

                    <!-- Requisitos -->
                    <div v-if="oferta.requirements && hasRequisitos(oferta.requirements)" class="bg-gray-50 rounded-lg p-3">
                      <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Requisitos</h4>
                      <dl class="space-y-2">
                        <div v-if="oferta.requirements.required_education_level" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-36 flex-shrink-0">Nivel educativo mín.</dt>
                          <dd class="text-xs text-gray-700 font-medium">{{ oferta.requirements.required_education_level }}</dd>
                        </div>
                        <div v-if="oferta.requirements.min_experience_years > 0" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-36 flex-shrink-0">Experiencia mín.</dt>
                          <dd class="text-xs text-gray-700 font-medium">{{ oferta.requirements.min_experience_years }} año(s)</dd>
                        </div>
                        <div v-if="oferta.requirements.required_skills?.length > 0">
                          <dt class="text-xs text-gray-400 mb-1">Habilidades requeridas</dt>
                          <div class="flex flex-wrap gap-1.5">
                            <span v-for="s in oferta.requirements.required_skills" :key="s"
                              class="px-2 py-0.5 bg-emi-navy-50 text-emi-navy-700 border border-emi-navy-200 rounded-full text-xs">
                              {{ s }}
                            </span>
                          </div>
                        </div>
                        <div v-if="oferta.requirements.preferred_skills?.length > 0">
                          <dt class="text-xs text-gray-400 mb-1">Habilidades deseables</dt>
                          <div class="flex flex-wrap gap-1.5">
                            <span v-for="s in oferta.requirements.preferred_skills" :key="s"
                              class="px-2 py-0.5 bg-gray-100 text-gray-600 border border-gray-200 rounded-full text-xs">
                              {{ s }}
                            </span>
                          </div>
                        </div>
                        <div v-if="oferta.requirements.required_languages?.length > 0" class="flex gap-2">
                          <dt class="text-xs text-gray-400 w-36 flex-shrink-0">Idiomas</dt>
                          <dd class="text-xs text-gray-700">{{ oferta.requirements.required_languages.join(', ') }}</dd>
                        </div>
                      </dl>
                    </div>
                  </div>

                  <!-- Análisis de compatibilidad (solo si ya postuló) -->
                  <template v-if="getPostulacion(oferta.id)">
                    <div class="flex items-center gap-2 mt-6 mb-4">
                      <div class="flex-1 h-px bg-gray-200"></div>
                      <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2">
                        Análisis de Compatibilidad
                      </span>
                      <div class="flex-1 h-px bg-gray-200"></div>
                    </div>

                    <div v-if="getPostulacion(oferta.id).scores_detalle" class="mb-4">
                      <h4 class="font-semibold text-gray-900 mb-3">Detalle de Scores</h4>
                      <div class="space-y-3">
                        <div v-for="(value, key) in getPostulacion(oferta.id).scores_detalle" :key="key">
                          <ProgressBar :value="value * 100" :label="formatScoreLabel(key)" />
                        </div>
                      </div>
                    </div>

                    <MatchDetailSection
                      v-if="getPostulacion(oferta.id).match_details"
                      :matchDetails="getPostulacion(oferta.id).match_details"
                      :clasificacion="getPostulacion(oferta.id).clasificacion"
                    />
                  </template>

                </div>

                <!-- Error al postular -->
                <div v-if="errorPostulando === oferta.id" class="mt-3 p-3 bg-red-50 rounded-lg border border-red-200">
                  <p class="text-sm text-red-700">{{ errorMensaje }}</p>
                </div>

              </Card>
            </div>
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
import { getOfertasDisponibles, postularAOferta, getMyPostulaciones } from '../api/postulaciones.api'
import { formatApiError } from '@/shared/utils/apiError'
import { checkRecommendationEligibility } from '../api/recommendations.api'
import { useAuthStore } from '@/features/auth/store/auth.store'

const authStore = useAuthStore()
const userRole = computed(() => authStore.user?.rol || 'estudiante')

// ── Estado ─────────────────────────────────────────────
const loadingInit = ref(true)
const isEligible = ref(true)
const eligibilityReason = ref('')
const eligibilityAction = ref('')
const missingFields = ref([])

const ofertas = ref([])
const loadingOfertas = ref(false)
const ofertaFilter = ref('todos')

const postulaciones = ref([])
const postulando = ref(null)
const errorPostulando = ref(null)
const errorMensaje = ref('')
const expandedId = ref(null)

// ── Computed ───────────────────────────────────────────
const postulacionMap = computed(() => {
  const map = {}
  for (const p of postulaciones.value) map[p.oferta_id] = p
  return map
})

const ofertaFilters = computed(() => {
  const pasantiaCount = ofertas.value.filter(o => o.tipo === 'pasantia').length
  const empleoCount   = ofertas.value.filter(o => o.tipo === 'empleo').length
  return [
    { key: 'todos',    label: 'Todas',     count: ofertas.value.length },
    { key: 'pasantia', label: 'Pasantías', count: pasantiaCount },
    { key: 'empleo',   label: 'Empleos',   count: empleoCount }
  ].filter(f => f.key === 'todos' || f.count > 0)
})

const filteredOfertas = computed(() =>
  ofertaFilter.value === 'todos'
    ? ofertas.value
    : ofertas.value.filter(o => o.tipo === ofertaFilter.value)
)

// ── Helpers ────────────────────────────────────────────
const getPostulacion = (ofertaId) => postulacionMap.value[ofertaId] || null

const hasRequisitos = (req) =>
  req && (
    req.required_education_level ||
    req.min_experience_years > 0 ||
    req.required_skills?.length > 0 ||
    req.preferred_skills?.length > 0 ||
    req.required_languages?.length > 0
  )

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

const toggleExpand = (id) => { expandedId.value = expandedId.value === id ? null : id }

// ── Acciones ───────────────────────────────────────────
const postular = async (ofertaId) => {
  errorPostulando.value = null
  errorMensaje.value = ''
  postulando.value = ofertaId

  try {
    const result = await postularAOferta(ofertaId)

    postulaciones.value.unshift({
      id:             result.id,
      oferta_id:      ofertaId,
      match_score:    result.match_score,
      clasificacion:  result.clasificacion,
      scores_detalle: result.scores_detalle,
      fortalezas:     result.fortalezas,
      debilidades:    result.debilidades,
      match_details:  result.match_details,
      estado:         result.estado || 'pendiente',
      created_at:     result.created_at || new Date().toISOString(),
      oferta:         result.oferta
    })

    expandedId.value = ofertaId

  } catch (e) {
    errorPostulando.value = ofertaId
    errorMensaje.value = formatApiError(e, 'Error al procesar la postulación')
  } finally {
    postulando.value = null
  }
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
      loadingOfertas.value = true
      await Promise.all([
        getOfertasDisponibles().then(d => { ofertas.value = d.ofertas || [] }),
        getMyPostulaciones().then(d => { postulaciones.value = d.postulaciones || [] })
      ])
      loadingOfertas.value = false
    }
  } catch {
    isEligible.value = true
  } finally {
    loadingInit.value = false
  }
})
</script>
