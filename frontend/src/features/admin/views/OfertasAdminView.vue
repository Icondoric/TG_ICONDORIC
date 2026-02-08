<template>
  <AppLayout :menuItems="adminMenuItems" variant="dark">
    <div class="py-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Ofertas Laborales</h1>
          <p class="mt-2 text-gray-600">Gestiona pasantias y empleos disponibles</p>
        </div>
        <router-link
          to="/admin/ofertas/new"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
        >
          <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Oferta
        </router-link>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-blue-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-500">Pasantias Activas</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.pasantias_activas }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-500">Empleos Activos</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.empleos_activos }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-yellow-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-500">Expiradas</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.ofertas_expiradas }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-gray-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-gray-500">Inactivas</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.ofertas_inactivas }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-lg shadow p-4 mb-6">
        <div class="flex flex-wrap gap-4">
          <select
            v-model="filters.tipo"
            class="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Todos los tipos</option>
            <option value="pasantia">Pasantias</option>
            <option value="empleo">Empleos</option>
          </select>

          <select
            v-model="filters.is_active"
            class="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Todos los estados</option>
            <option value="true">Activas</option>
            <option value="false">Inactivas</option>
          </select>

          <label class="flex items-center">
            <input
              type="checkbox"
              v-model="filters.include_expired"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-600">Incluir expiradas</span>
          </label>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
        <button @click="loadOfertas" class="mt-2 text-red-600 hover:text-red-800 underline">
          Reintentar
        </button>
      </div>

      <!-- Table -->
      <div v-else class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Oferta
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tipo
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Institucion
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Vigencia
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="oferta in ofertas" :key="oferta.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="text-sm font-medium text-gray-900">{{ oferta.titulo }}</div>
                <div v-if="oferta.ubicacion" class="text-sm text-gray-500">{{ oferta.ubicacion }}</div>
              </td>
              <td class="px-6 py-4">
                <span :class="[
                  'px-2 py-1 text-xs font-medium rounded-full',
                  oferta.tipo === 'pasantia' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                ]">
                  {{ oferta.tipo === 'pasantia' ? 'Pasantia' : 'Empleo' }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ oferta.institution_name || 'Sin asignar' }}
              </td>
              <td class="px-6 py-4">
                <span :class="[
                  'px-2 py-1 text-xs font-medium rounded-full',
                  oferta.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                ]">
                  {{ oferta.is_active ? 'Activa' : 'Inactiva' }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                <span v-if="oferta.fecha_cierre">
                  {{ formatDate(oferta.fecha_cierre) }}
                </span>
                <span v-else class="text-gray-400">Sin fecha</span>
              </td>
              <td class="px-6 py-4 text-right text-sm font-medium">
                <router-link
                  :to="`/admin/ofertas/edit/${oferta.id}`"
                  class="text-blue-600 hover:text-blue-900 mr-4"
                >
                  Editar
                </router-link>
                <button
                  v-if="oferta.is_active"
                  @click="deactivateOferta(oferta)"
                  class="text-red-600 hover:text-red-900"
                >
                  Desactivar
                </button>
                <button
                  v-else
                  @click="activateOferta(oferta)"
                  class="text-green-600 hover:text-green-900"
                >
                  Activar
                </button>
              </td>
            </tr>

            <tr v-if="ofertas.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                No hay ofertas que coincidan con los filtros
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
          <p class="text-sm text-gray-500">
            Mostrando {{ ofertas.length }} de {{ total }} ofertas
          </p>
          <div class="flex gap-2">
            <button
              @click="page--; loadOfertas()"
              :disabled="page <= 1"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
            >
              Anterior
            </button>
            <button
              @click="page++; loadOfertas()"
              :disabled="page >= totalPages"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, watch, onMounted, computed } from 'vue'
import { listOfertas, deleteOferta, activateOferta as activateOfertaApi, getOfertasStats } from '@/features/admin/api/ofertas.api'
import AppLayout from '@/shared/components/AppLayout.vue'
import { adminMenuItems } from '@/shared/constants/navigation'

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

const filters = reactive({
  tipo: '',
  is_active: '',
  include_expired: false
})

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

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
    error.value = e.response?.data?.detail || 'Error cargando ofertas'
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

const deactivateOferta = async (oferta) => {
  if (!confirm(`Desactivar oferta "${oferta.titulo}"?`)) return

  try {
    await deleteOferta(oferta.id)
    oferta.is_active = false
    loadStats()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error desactivando oferta'
  }
}

const activateOferta = async (oferta) => {
  try {
    await activateOfertaApi(oferta.id)
    oferta.is_active = true
    loadStats()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error activando oferta'
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
