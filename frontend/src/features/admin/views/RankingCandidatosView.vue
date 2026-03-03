<template>
  <AppLayout>
    <div class="max-w-5xl mx-auto px-6 py-8">

      <!-- ═══ ENCABEZADO ESTÁNDAR (esquina derecha del main) ═══ -->
      <div class="flex items-start justify-between gap-6 mb-8">
        <div>
          <h1 class="text-3xl font-bold text-emi-navy-500">Evaluación de Candidatos</h1>
          <p class="mt-1 text-gray-600">
            Selecciona una convocatoria para ver los postulantes y su evaluación automática.
          </p>
        </div>
        <div class="flex items-center gap-2 flex-shrink-0">
          <!-- Botón actualizar -->
          <button
            @click="loadOfertas"
            :disabled="loadingOfertas"
            class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-emi-navy-200 hover:border-emi-navy-400 text-emi-navy-600 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <svg :class="['h-4 w-4', loadingOfertas && 'animate-spin']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Actualizar
          </button>
          <!-- Instrucción visual -->
          <div class="hidden sm:flex items-center gap-2 px-4 py-2 bg-emi-navy-50 border border-emi-navy-200 rounded-xl text-xs text-emi-navy-600">
            <svg class="w-4 h-4 text-emi-navy-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Haz clic en una oferta para ver su evaluación
          </div>
        </div>
      </div>

      <!-- ═══ FILTROS ═══ -->
      <div class="card-emi mb-6">
        <div class="flex flex-wrap items-center gap-3">

          <!-- Buscador -->
          <div class="relative flex-1 min-w-[200px]">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-emi-navy-400"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              v-model="filters.search"
              @input="debouncedLoad"
              type="text"
              placeholder="Buscar por título o institución..."
              class="w-full pl-9 pr-3 py-2 text-sm border border-emi-navy-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emi-navy-300"
            />
          </div>

          <!-- Tipo -->
          <div class="flex gap-1.5">
            <button
              v-for="t in tipoOptions"
              :key="t.value"
              @click="filters.tipo = t.value; loadOfertas()"
              :class="[
                'px-3 py-2 text-xs rounded-lg font-medium transition-colors',
                filters.tipo === t.value
                  ? 'bg-emi-navy-500 text-white'
                  : 'bg-white text-gray-500 border border-emi-navy-200 hover:border-emi-navy-400'
              ]"
            >{{ t.label }}</button>
          </div>

          <!-- Estado -->
          <div class="flex gap-1.5">
            <button
              v-for="e in estadoOptions"
              :key="e.value"
              @click="setEstado(e.value)"
              :class="[
                'px-3 py-2 text-xs rounded-lg font-medium transition-colors',
                estadoKey === e.value
                  ? 'bg-emi-navy-500 text-white'
                  : 'bg-white text-gray-500 border border-emi-navy-200 hover:border-emi-navy-400'
              ]"
            >{{ e.label }}</button>
          </div>

        </div>
      </div>

      <!-- ═══ ESTADO LOADING ═══ -->
      <div v-if="loadingOfertas" class="flex justify-center py-20">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
      </div>

      <!-- ═══ ESTADO VACÍO ═══ -->
      <div v-else-if="ofertas.length === 0" class="card-emi text-center py-16">
        <div class="w-16 h-16 bg-emi-navy-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="h-8 w-8 text-emi-navy-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
        </div>
        <p class="text-emi-navy-500 font-semibold">No hay ofertas que coincidan</p>
        <p class="text-sm text-gray-400 mt-1">Intenta modificar los filtros de búsqueda</p>
      </div>

      <!-- ═══ GRILLA DE OFERTAS ═══ -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <button
          v-for="oferta in ofertas"
          :key="oferta.id"
          @click="irADetalle(oferta.id)"
          class="card-emi text-left hover:shadow-md hover:border-emi-navy-300 active:scale-[0.98] transition-all group"
        >
          <!-- Tipo + Estado -->
          <div class="flex items-center gap-2 mb-3">
            <span :class="[
              'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
              oferta.tipo === 'pasantia' ? 'bg-info-100 text-info-700' : 'bg-emi-navy-100 text-emi-navy-700'
            ]">
              {{ oferta.tipo === 'pasantia' ? 'Pasantía' : 'Empleo' }}
            </span>
            <span v-if="!oferta.is_active"
              class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-500">
              Cerrada
            </span>
            <span v-else
              class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-success-100 text-success-700">
              Activa
            </span>
          </div>

          <!-- Título -->
          <h2 class="text-sm font-bold text-emi-navy-800 mb-1 line-clamp-2 group-hover:text-emi-navy-600 transition-colors">
            {{ oferta.titulo }}
          </h2>

          <!-- Institución -->
          <p v-if="oferta.institution_name" class="text-xs text-gray-400 mb-4 truncate">
            {{ oferta.institution_name }}
            <span v-if="oferta.sector" class="opacity-70"> · {{ oferta.sector }}</span>
          </p>

          <!-- Stats de postulaciones -->
          <div class="mt-auto">
            <!-- Barra de distribución -->
            <div v-if="oferta.stats?.total > 0" class="mb-2">
              <div class="flex justify-between text-xs text-gray-400 mb-1">
                <span>{{ oferta.stats.total }} postulante{{ oferta.stats.total !== 1 ? 's' : '' }}</span>
                <span class="text-emi-gold-600 font-semibold">{{ oferta.stats.apto }} APTO</span>
              </div>
              <div class="flex h-1.5 rounded-full overflow-hidden bg-gray-100">
                <div
                  :style="{ width: (oferta.stats.apto / oferta.stats.total * 100) + '%' }"
                  class="bg-emi-gold-400"
                  :title="`APTO: ${oferta.stats.apto}`"
                />
                <div
                  :style="{ width: (oferta.stats.considerado / oferta.stats.total * 100) + '%' }"
                  class="bg-emi-navy-400"
                  :title="`CONSIDERADO: ${oferta.stats.considerado}`"
                />
                <div
                  :style="{ width: (oferta.stats.no_apto / oferta.stats.total * 100) + '%' }"
                  class="bg-danger-400"
                  :title="`NO APTO: ${oferta.stats.no_apto}`"
                />
              </div>
            </div>
            <!-- Sin postulaciones -->
            <div v-else class="text-xs text-gray-400 italic mb-2">
              Sin postulaciones aún
            </div>

            <!-- CTA row -->
            <div class="flex items-center justify-between pt-2 border-t border-emi-navy-100">
              <span class="text-xs font-bold text-emi-navy-600">
                {{ oferta.stats?.total ?? 0 }} postulante{{ (oferta.stats?.total ?? 0) !== 1 ? 's' : '' }}
              </span>
              <span class="inline-flex items-center gap-1 text-xs font-semibold text-emi-navy-500 group-hover:text-emi-navy-700 transition-colors">
                Ver evaluación
                <svg class="h-3.5 w-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </span>
            </div>
          </div>
        </button>
      </div>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/shared/components/AppLayout.vue'
import { getOfertasConStats } from '../api/ranking.api'

const router = useRouter()

// ── Filtros ────────────────────────────────────────────
const filters = ref({ search: '', tipo: '' })
const estadoKey = ref('todas')
const searchTimeout = ref(null)

const tipoOptions = [
  { value: '', label: 'Todas' },
  { value: 'pasantia', label: 'Pasantías' },
  { value: 'empleo', label: 'Empleos' },
]
const estadoOptions = [
  { value: 'todas', label: 'Todas' },
  { value: 'activas', label: 'Activas' },
  { value: 'cerradas', label: 'Cerradas' },
]

// ── Estado ─────────────────────────────────────────────
const ofertas = ref([])
const loadingOfertas = ref(false)

// ── Helpers ────────────────────────────────────────────
const setEstado = (value) => {
  estadoKey.value = value
  loadOfertas()
}

const debouncedLoad = () => {
  clearTimeout(searchTimeout.value)
  searchTimeout.value = setTimeout(loadOfertas, 300)
}

const irADetalle = (id) => {
  router.push({ name: 'admin-ranking-detalle', params: { id } })
}

// ── Acciones ───────────────────────────────────────────
const loadOfertas = async () => {
  loadingOfertas.value = true
  try {
    const params = { include_expired: true }
    if (filters.value.tipo) params.tipo = filters.value.tipo
    if (estadoKey.value === 'activas') params.is_active = true
    if (estadoKey.value === 'cerradas') params.is_active = false
    if (filters.value.search) params.search = filters.value.search

    const data = await getOfertasConStats(params)
    ofertas.value = data.ofertas || []
  } catch (e) {
    console.error('Error cargando ofertas:', e)
  } finally {
    loadingOfertas.value = false
  }
}

onMounted(loadOfertas)
</script>
