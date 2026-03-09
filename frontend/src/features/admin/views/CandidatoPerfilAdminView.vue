<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- Breadcrumb + título -->
      <div class="mb-6">
        <button
          @click="router.back()"
          class="inline-flex items-center gap-1.5 text-xs text-emi-navy-400 hover:text-emi-navy-600 font-medium transition-colors mb-2"
        >
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Volver
        </button>
        <h1 class="text-2xl font-bold text-emi-navy-500">Perfil del Candidato</h1>
        <p class="mt-1 text-sm text-gray-500">CV digitalizado y competencias extraídas automáticamente.</p>
      </div>

      <!-- Cargando -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-white rounded-xl border border-red-200 text-center py-12 px-6">
        <svg class="w-10 h-10 text-red-400 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="text-red-600 font-semibold">{{ error }}</p>
      </div>

      <!-- Perfil cargado -->
      <div v-else-if="perfil" class="space-y-4">

        <!-- CV info bar -->
        <div v-if="perfil.cv_filename"
          class="flex items-center gap-3 px-4 py-3 bg-emi-navy-50 border border-emi-navy-100 rounded-lg text-sm"
        >
          <svg class="h-5 w-5 text-emi-navy-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span class="font-medium text-emi-navy-700">{{ perfil.cv_filename }}</span>
          <span class="text-emi-navy-400">·</span>
          <span class="text-emi-navy-500">Subido {{ formatDate(perfil.cv_uploaded_at) }}</span>
        </div>

        <!-- Documento CV — estilo igual a Mi Perfil Digitalizado -->
        <div class="bg-white rounded-xl shadow-md border border-gray-100 px-8 py-8 space-y-8">

          <!-- Nombre + contacto + línea navy -->
          <PersonalInfoCard :profile="perfil" :readOnly="true" />

          <!-- Perfil Profesional (summary de Gemini) -->
          <div v-if="geminiPersonalInfo?.summary">
            <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
              Perfil Profesional
            </h3>
            <div class="mt-1 h-px bg-emi-navy-300"></div>
            <p class="mt-3 text-sm text-gray-700 leading-relaxed">
              {{ geminiPersonalInfo.summary }}
            </p>
          </div>

          <!-- Formación Académica + Experiencia Laboral -->
          <EducationExperienceGrid
            :profile="perfil"
            :geminiEducation="educacion"
            :geminiExperience="experiencia"
            :readOnly="true"
          />

          <!-- Habilidades Técnicas + Blandas + Idiomas -->
          <CompetenciasCard :profile="perfil" :readOnly="true" />

        </div>
      </div>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/shared/components/AppLayout.vue'
import PersonalInfoCard from '@/features/profile/components/PersonalInfoCard.vue'
import EducationExperienceGrid from '@/features/profile/components/EducationExperienceGrid.vue'
import CompetenciasCard from '@/features/profile/components/CompetenciasCard.vue'
import { fetchUserProfile } from '../api/users.api'

const route = useRoute()
const router = useRouter()

const userId = route.params.userId
const perfil = ref(null)
const loading = ref(true)
const error = ref(null)

const educacion = computed(() => {
  const ge = perfil.value?.gemini_extraction || {}
  return ge.education || ge.educacion || ge.formacion || []
})

const experiencia = computed(() => {
  const ge = perfil.value?.gemini_extraction || {}
  return ge.experience || ge.experiencia || ge.work_experience || []
})

const geminiPersonalInfo = computed(() => {
  const ge = perfil.value?.gemini_extraction || {}
  return ge.personal_info || ge.personal || null
})

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    perfil.value = await fetchUserProfile(userId)
  } catch (e) {
    error.value = e.response?.status === 404
      ? 'Este usuario no tiene perfil digitalizado.'
      : 'Error al cargar el perfil.'
  } finally {
    loading.value = false
  }
})
</script>
