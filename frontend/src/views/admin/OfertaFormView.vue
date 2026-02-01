<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <router-link to="/admin/ofertas" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Ofertas
        </router-link>
        <h1 class="text-3xl font-bold text-gray-900">
          {{ isEditing ? 'Editar Oferta' : 'Nueva Oferta' }}
        </h1>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Form -->
      <form v-else @submit.prevent="saveOferta" class="bg-white rounded-lg shadow p-6">
        <!-- Error -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-700">{{ error }}</p>
        </div>

        <!-- Basic Info -->
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700">Titulo *</label>
            <input
              v-model="form.titulo"
              type="text"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Ej: Pasantia en Desarrollo Web"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Descripcion</label>
            <textarea
              v-model="form.descripcion"
              rows="4"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Describe la oferta, responsabilidades, beneficios..."
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipo *</label>
              <select
                v-model="form.tipo"
                required
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Seleccionar...</option>
                <option value="pasantia">Pasantia</option>
                <option value="empleo">Empleo</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Modalidad</label>
              <select
                v-model="form.modalidad"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Seleccionar...</option>
                <option value="presencial">Presencial</option>
                <option value="remoto">Remoto</option>
                <option value="hibrido">Hibrido</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Ubicacion</label>
            <input
              v-model="form.ubicacion"
              type="text"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Ej: La Paz, Bolivia"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Perfil Institucional</label>
            <select
              v-model="form.institutional_profile_id"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Sin perfil asociado</option>
              <option v-for="profile in profiles" :key="profile.id" :value="profile.id">
                {{ profile.institution_name }} - {{ profile.sector }}
              </option>
            </select>
            <p class="mt-1 text-sm text-gray-500">
              Asociar a un perfil institucional permite evaluaciones mas precisas
            </p>
          </div>

          <!-- Dates -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Fecha de Inicio</label>
              <input
                v-model="form.fecha_inicio"
                type="date"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Fecha de Cierre</label>
              <input
                v-model="form.fecha_cierre"
                type="date"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Cupos Disponibles</label>
            <input
              v-model.number="form.cupos_disponibles"
              type="number"
              min="1"
              class="mt-1 block w-32 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <!-- Status (only for editing) -->
          <div v-if="isEditing" class="flex items-center">
            <input
              v-model="form.is_active"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label class="ml-2 block text-sm text-gray-700">
              Oferta activa
            </label>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-8 pt-6 border-t border-gray-200 flex justify-end gap-4">
          <router-link
            to="/admin/ofertas"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </router-link>
          <button
            type="submit"
            :disabled="saving"
            class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {{ saving ? 'Guardando...' : (isEditing ? 'Guardar Cambios' : 'Crear Oferta') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getOferta, createOferta, updateOferta, listProfiles } from '../../services/api'

const route = useRoute()
const router = useRouter()

const ofertaId = computed(() => route.params.id)
const isEditing = computed(() => !!ofertaId.value)

const form = reactive({
  titulo: '',
  descripcion: '',
  tipo: '',
  modalidad: '',
  ubicacion: '',
  institutional_profile_id: '',
  fecha_inicio: '',
  fecha_cierre: '',
  cupos_disponibles: 1,
  is_active: true
})

const profiles = ref([])
const loading = ref(false)
const saving = ref(false)
const error = ref(null)

const loadProfiles = async () => {
  try {
    const result = await listProfiles(false)
    profiles.value = result.profiles || []
  } catch (e) {
    console.error('Error loading profiles:', e)
  }
}

const loadOferta = async () => {
  if (!isEditing.value) return

  loading.value = true
  error.value = null

  try {
    const oferta = await getOferta(ofertaId.value)

    form.titulo = oferta.titulo
    form.descripcion = oferta.descripcion || ''
    form.tipo = oferta.tipo
    form.modalidad = oferta.modalidad || ''
    form.ubicacion = oferta.ubicacion || ''
    form.institutional_profile_id = oferta.institutional_profile_id || ''
    form.fecha_inicio = oferta.fecha_inicio || ''
    form.fecha_cierre = oferta.fecha_cierre || ''
    form.cupos_disponibles = oferta.cupos_disponibles || 1
    form.is_active = oferta.is_active

  } catch (e) {
    error.value = e.response?.data?.detail || 'Error cargando oferta'
  } finally {
    loading.value = false
  }
}

const saveOferta = async () => {
  saving.value = true
  error.value = null

  try {
    const data = {
      titulo: form.titulo,
      descripcion: form.descripcion || null,
      tipo: form.tipo,
      modalidad: form.modalidad || null,
      ubicacion: form.ubicacion || null,
      institutional_profile_id: form.institutional_profile_id || null,
      fecha_inicio: form.fecha_inicio || null,
      fecha_cierre: form.fecha_cierre || null,
      cupos_disponibles: form.cupos_disponibles
    }

    if (isEditing.value) {
      data.is_active = form.is_active
      await updateOferta(ofertaId.value, data)
    } else {
      await createOferta(data)
    }

    router.push('/admin/ofertas')

  } catch (e) {
    error.value = e.response?.data?.detail || 'Error guardando oferta'
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadProfiles()
  loadOferta()
})
</script>
