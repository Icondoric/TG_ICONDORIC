<template>
  <AppLayout>
    <div class="py-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-emi-navy-500">Lista de Convocatorias Laborales</h1>
          <p class="mt-2 text-slate-600">Gestiona convocatorias de pasantías y empleos disponibles</p>
        </div>
        <router-link
          to="/admin/convocatorias/new"
          class="btn-emi-primary flex items-center shadow-sm"
        >
          <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Convocatoria
        </router-link>
      </div>

      <!-- Stats Cards -->
      <div class="mb-3">
        <h2 class="text-sm font-semibold text-slate-600 uppercase tracking-wider">Resumen de convocatorias</h2>
        <p class="text-xs text-slate-400 mt-0.5">Estado actual de todas las convocatorias registradas en el sistema</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="card-emi p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-info-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-info-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-slate-500">Pasantias Activas</p>
              <p class="text-2xl font-semibold text-slate-800">{{ stats.pasantias_activas }}</p>
            </div>
          </div>
        </div>

        <div class="card-emi p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-success-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-success-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-slate-500">Empleos Activos</p>
              <p class="text-2xl font-semibold text-slate-800">{{ stats.empleos_activos }}</p>
            </div>
          </div>
        </div>

        <div class="card-emi p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-warning-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-warning-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-slate-500">Expiradas</p>
              <p class="text-2xl font-semibold text-slate-800">{{ stats.ofertas_expiradas }}</p>
            </div>
          </div>
        </div>

        <div class="card-emi p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-slate-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-slate-500">Inactivas</p>
              <p class="text-2xl font-semibold text-slate-800">{{ stats.ofertas_inactivas }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="card-emi p-4 mb-6">
        <div class="flex flex-col md:flex-row flex-wrap gap-4">
          <!-- Búsqueda por texto -->
          <div class="flex-1 min-w-[200px]">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar por título o institución..."
              class="w-full border-slate-200 rounded-md shadow-sm focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
            />
          </div>

          <select
            v-model="filters.tipo"
            class="border-slate-200 rounded-md shadow-sm focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
          >
            <option value="">Todos los tipos</option>
            <option value="pasantia">Pasantias</option>
            <option value="empleo">Empleos</option>
          </select>

          <select
            v-model="filters.is_active"
            class="border-slate-200 rounded-md shadow-sm focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
          >
            <option value="">Todos los estados</option>
            <option value="true">Activas</option>
            <option value="false">Inactivas</option>
          </select>

          <label class="flex items-center">
            <input
              type="checkbox"
              v-model="filters.include_expired"
              class="rounded border-slate-300 text-emi-navy-600 focus:ring-emi-navy-500"
            />
            <span class="ml-2 text-sm text-slate-600">Incluir expiradas</span>
          </label>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12 card-emi">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-gold"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-danger-50 border border-danger-200 rounded-lg p-4 mb-6">
        <p class="text-danger-700">{{ error }}</p>
        <button @click="loadOfertas" class="mt-2 text-danger-600 hover:text-danger-800 underline">
          Reintentar
        </button>
      </div>

      <!-- Table -->
      <div v-else class="card-emi overflow-hidden">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Convocatoria
              </th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Tipo
              </th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Institucion
              </th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Estado
              </th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Vigencia
              </th>
              <th class="px-6 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-slate-200">
            <tr v-for="oferta in filteredOfertas" :key="oferta.id" class="hover:bg-slate-50 transition-colors">
              <td class="px-6 py-4">
                <div class="text-sm font-semibold text-slate-900">{{ oferta.titulo }}</div>
                <div v-if="oferta.ubicacion" class="text-sm text-slate-500">{{ oferta.ubicacion }}</div>
              </td>
              <td class="px-6 py-4">
                <span :class="[
                  'badge-emi',
                  oferta.tipo === 'pasantia' ? 'bg-info-100 text-info-800' : 'bg-success-100 text-success-800'
                ]">
                  {{ oferta.tipo === 'pasantia' ? 'Pasantia' : 'Empleo' }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-slate-500">
                {{ oferta.institution_name || 'Sin asignar' }}
              </td>
              <td class="px-6 py-4">
                <span :class="[
                  'badge-emi',
                  oferta.is_active ? 'bg-success-100 text-success-800' : 'bg-slate-100 text-slate-600'
                ]">
                  {{ oferta.is_active ? 'Activa' : 'Inactiva' }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-slate-500">
                <span v-if="oferta.fecha_cierre">
                  {{ formatDate(oferta.fecha_cierre) }}
                </span>
                <span v-else class="text-slate-400">Sin fecha</span>
              </td>
              <td class="px-6 py-4">
                <div class="flex flex-col gap-2 items-end">
                  <router-link
                    :to="`/admin/convocatorias/edit/${oferta.id}`"
                    class="px-3 py-1.5 bg-emi-navy-100 text-emi-navy-700 rounded-lg hover:bg-emi-navy-200 transition-colors text-sm font-medium"
                  >
                    Editar
                  </router-link>
                  <button
                    v-if="oferta.is_active"
                    @click="deactivateOferta(oferta)"
                    class="px-3 py-1.5 bg-warning-100 text-warning-700 rounded-lg hover:bg-warning-200 transition-colors text-sm font-medium"
                  >
                    Desactivar
                  </button>
                  <button
                    v-else
                    @click="activateOferta(oferta)"
                    class="px-3 py-1.5 bg-success-100 text-success-700 rounded-lg hover:bg-success-200 transition-colors text-sm font-medium"
                  >
                    Activar
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="filteredOfertas.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-slate-500">
                No hay convocatorias que coincidan con los filtros
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-6 py-4 border-t border-slate-200 flex justify-between items-center">
          <p class="text-sm text-slate-500">
            Mostrando {{ ofertas.length }} de {{ total }} convocatorias
          </p>
          <div class="flex gap-2">
            <button
              @click="page--; loadOfertas()"
              :disabled="page <= 1"
              class="px-3 py-1 border border-slate-300 rounded text-sm disabled:opacity-50 hover:bg-slate-50 transition-colors"
            >
              Anterior
            </button>
            <button
              @click="page++; loadOfertas()"
              :disabled="page >= totalPages"
              class="px-3 py-1 border border-slate-300 rounded text-sm disabled:opacity-50 hover:bg-slate-50 transition-colors"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Desactivar Oferta -->
    <Teleport to="body">
      <div
        v-if="deactivateConfirm"
        class="fixed inset-0 bg-slate-900 bg-opacity-60 flex items-center justify-center z-50 p-4"
        @click.self="deactivateConfirm = null"
      >
        <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="flex-shrink-0 w-10 h-10 bg-warning-100 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-slate-800">Desactivar Convocatoria</h3>
          </div>
          <p class="text-slate-600 mb-4">
            ¿Deseas desactivar la convocatoria
            <span class="font-semibold text-slate-800">{{ deactivateConfirm.titulo }}</span>?
            Podras reactivarla posteriormente.
          </p>
          <div class="flex gap-3 justify-end">
            <button @click="deactivateConfirm = null" class="px-4 py-2 text-slate-600 hover:bg-slate-50 transition-colors rounded-lg font-medium">
              Cancelar
            </button>
            <button @click="confirmDeactivate" class="px-4 py-2 bg-warning-500 text-white rounded-lg hover:bg-warning-600 transition-colors font-medium">
              Desactivar
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </AppLayout>
</template>

<script setup>
import { ref, reactive, watch, onMounted, computed } from 'vue'
import { listOfertas, deleteOferta, activateOferta as activateOfertaApi, getOfertasStats } from '@/features/admin/api/ofertas.api'
import AppLayout from '@/shared/components/AppLayout.vue'
import { formatApiError } from '@/shared/utils/apiError'

const ofertas = ref([])
const stats = ref({
  pasantias_activas: 0,
  empleos_activos: 0,
  ofertas_expiradas: 0,
  ofertas_inactivas: 0
})
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(true)
const error = ref(null)
const deactivateConfirm = ref(null)

const filters = reactive({
  tipo: '',
  is_active: '',
  include_expired: false
})
const searchQuery = ref('')

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const filteredOfertas = computed(() => {
  let list = ofertas.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    list = list.filter(o => 
      o.titulo.toLowerCase().includes(query) || 
      (o.institution_name && o.institution_name.toLowerCase().includes(query))
    )
  }
  
  return list
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const loadOfertas = async () => {
  loading.value = true
  error.value = null

  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      include_expired: filters.include_expired
    }

    if (filters.tipo) params.tipo = filters.tipo
    if (filters.is_active !== '') params.is_active = filters.is_active === 'true'

    const result = await listOfertas(params)
    ofertas.value = result.ofertas
    total.value = result.total

  } catch (e) {
    error.value = formatApiError(e, 'Error cargando ofertas')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const result = await getOfertasStats()
    stats.value = result
  } catch (e) {
    console.error('Error loading stats:', e)
  }
}

const deactivateOferta = (oferta) => {
  deactivateConfirm.value = oferta
}

const confirmDeactivate = async () => {
  if (!deactivateConfirm.value) return
  try {
    await deleteOferta(deactivateConfirm.value.id)
    deactivateConfirm.value.is_active = false
    deactivateConfirm.value = null
    loadStats()
  } catch (e) {
    error.value = formatApiError(e, 'Error desactivando oferta')
    deactivateConfirm.value = null
  }
}

const activateOferta = async (oferta) => {
  try {
    await activateOfertaApi(oferta.id)
    oferta.is_active = true
    loadStats()
  } catch (e) {
    error.value = formatApiError(e, 'Error activando oferta')
  }
}

// Watch filters
watch(filters, () => {
  page.value = 1
  loadOfertas()
}, { deep: true })

onMounted(() => {
  loadOfertas()
  loadStats()
})
</script>
