<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Mi Perfil Profesional</h1>
        <p class="mt-2 text-gray-600">
          Gestiona tu informacion profesional para recibir recomendaciones personalizadas
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
        <button @click="loadProfile" class="mt-2 text-red-600 hover:text-red-800 underline">
          Reintentar
        </button>
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Completeness Card -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-gray-900">Estado del Perfil</h2>
            <span :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              profile.is_complete ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
            ]">
              {{ profile.is_complete ? 'Completo' : 'Incompleto' }}
            </span>
          </div>

          <!-- Progress Bar -->
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-1">
              <span>Completitud del perfil</span>
              <span>{{ Math.round(profile.completeness_score * 100) }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div
                class="h-3 rounded-full transition-all duration-500"
                :class="profile.completeness_score >= 0.7 ? 'bg-green-500' : 'bg-yellow-500'"
                :style="{ width: `${profile.completeness_score * 100}%` }"
              ></div>
            </div>
          </div>

          <!-- Missing Fields -->
          <div v-if="completeness && completeness.missing_fields.length > 0" class="mt-4">
            <p class="text-sm text-gray-600 mb-2">Para mejorar tu perfil:</p>
            <ul class="list-disc list-inside text-sm text-gray-500 space-y-1">
              <li v-for="rec in completeness.recommendations" :key="rec">{{ rec }}</li>
            </ul>
          </div>

          <!-- CV Info -->
          <div v-if="profile.cv_filename" class="mt-4 pt-4 border-t border-gray-200">
            <div class="flex items-center text-sm text-gray-600">
              <svg class="h-5 w-5 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>{{ profile.cv_filename }}</span>
              <span class="ml-2 text-gray-400">
                - Subido {{ formatDate(profile.cv_uploaded_at) }}
              </span>
            </div>
          </div>

          <!-- Upload CV Button -->
          <div class="mt-4">
            <router-link
              to="/subir-cv"
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              {{ profile.cv_filename ? 'Actualizar CV' : 'Subir CV' }}
            </router-link>
          </div>
        </div>

        <!-- Skills Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Competencias</h2>

          <!-- Hard Skills -->
          <div class="mb-6">
            <h3 class="text-sm font-medium text-gray-700 mb-2">Habilidades Tecnicas</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="skill in profile.hard_skills"
                :key="skill"
                class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
              >
                {{ skill }}
              </span>
              <span v-if="profile.hard_skills.length === 0" class="text-gray-400 text-sm">
                No hay habilidades registradas
              </span>
            </div>
          </div>

          <!-- Soft Skills -->
          <div class="mb-6">
            <h3 class="text-sm font-medium text-gray-700 mb-2">Habilidades Blandas</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="skill in profile.soft_skills"
                :key="skill"
                class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm"
              >
                {{ skill }}
              </span>
              <span v-if="profile.soft_skills.length === 0" class="text-gray-400 text-sm">
                No hay habilidades registradas
              </span>
            </div>
          </div>

          <!-- Languages -->
          <div>
            <h3 class="text-sm font-medium text-gray-700 mb-2">Idiomas</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="lang in profile.languages"
                :key="lang"
                class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
              >
                {{ lang }}
              </span>
              <span v-if="profile.languages.length === 0" class="text-gray-400 text-sm">
                No hay idiomas registrados
              </span>
            </div>
          </div>
        </div>

        <!-- Education & Experience -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Education -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Formacion Academica</h2>
            <div v-if="profile.education_level" class="flex items-center">
              <svg class="h-8 w-8 text-blue-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path d="M12 14l9-5-9-5-9 5 9 5z" />
                <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
              </svg>
              <div>
                <p class="font-medium text-gray-900">{{ profile.education_level }}</p>
                <p class="text-sm text-gray-500">Nivel educativo mas alto</p>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm">No hay formacion registrada</p>

            <!-- Education Details from Gemini -->
            <div v-if="geminiEducation.length > 0" class="mt-4 border-t pt-4">
              <div v-for="(edu, index) in geminiEducation" :key="index" class="mb-3 last:mb-0">
                <p class="font-medium text-gray-800">{{ edu.degree }}</p>
                <p class="text-sm text-gray-600">{{ edu.institution }}</p>
                <p v-if="edu.year" class="text-xs text-gray-400">{{ edu.year }}</p>
              </div>
            </div>
          </div>

          <!-- Experience -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Experiencia Laboral</h2>
            <div class="flex items-center mb-4">
              <svg class="h-8 w-8 text-green-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <div>
                <p class="font-medium text-gray-900">{{ profile.experience_years }} anos</p>
                <p class="text-sm text-gray-500">Experiencia total</p>
              </div>
            </div>

            <!-- Experience Details from Gemini -->
            <div v-if="geminiExperience.length > 0" class="border-t pt-4">
              <div v-for="(exp, index) in geminiExperience" :key="index" class="mb-3 last:mb-0">
                <p class="font-medium text-gray-800">{{ exp.role }}</p>
                <p class="text-sm text-gray-600">{{ exp.company }}</p>
                <p v-if="exp.duration" class="text-xs text-gray-400">{{ exp.duration }}</p>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm">No hay experiencia registrada</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Acciones</h2>
          <div class="flex flex-wrap gap-4">
            <router-link
              to="/mis-recomendaciones"
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700"
              :class="{ 'opacity-50 cursor-not-allowed': !profile.is_complete }"
            >
              <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              Ver Recomendaciones
            </router-link>

            <button
              @click="showDeleteConfirm = true"
              class="inline-flex items-center px-4 py-2 border border-red-300 rounded-md text-sm font-medium text-red-700 bg-white hover:bg-red-50"
            >
              <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Limpiar Perfil
            </button>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteConfirm" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 max-w-md mx-4">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Confirmar limpieza de perfil</h3>
          <p class="text-gray-600 mb-6">
            Esto eliminara todos los datos de tu CV y competencias. Tendras que subir tu CV nuevamente.
            Esta accion no se puede deshacer.
          </p>
          <div class="flex justify-end gap-3">
            <button
              @click="showDeleteConfirm = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              @click="deleteProfile"
              :disabled="deleting"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
            >
              {{ deleting ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMyProfile, getProfileCompleteness, deleteMyProfile } from '../services/api'

const profile = ref({
  hard_skills: [],
  soft_skills: [],
  languages: [],
  education_level: null,
  experience_years: 0,
  is_complete: false,
  completeness_score: 0,
  cv_filename: null,
  cv_uploaded_at: null,
  gemini_extraction: {}
})
const completeness = ref(null)
const loading = ref(true)
const error = ref(null)
const showDeleteConfirm = ref(false)
const deleting = ref(false)

const geminiEducation = computed(() => {
  return profile.value.gemini_extraction?.education || []
})

const geminiExperience = computed(() => {
  return profile.value.gemini_extraction?.experience || []
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

const loadProfile = async () => {
  loading.value = true
  error.value = null

  try {
    const [profileData, completenessData] = await Promise.all([
      getMyProfile(),
      getProfileCompleteness()
    ])

    profile.value = profileData
    completeness.value = completenessData
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error cargando el perfil'
  } finally {
    loading.value = false
  }
}

const deleteProfile = async () => {
  deleting.value = true

  try {
    await deleteMyProfile()
    showDeleteConfirm.value = false
    await loadProfile()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error eliminando el perfil'
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>
