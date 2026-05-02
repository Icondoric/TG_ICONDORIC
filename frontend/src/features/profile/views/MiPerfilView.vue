<template>
  <AppLayout>
    <div class="flex min-h-screen">
      <!-- Main Content -->
      <div class="flex-1 min-w-0">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

          <!-- Header -->
          <div class="mb-4">
            <h1 class="text-2xl sm:text-3xl font-bold text-emi-navy-500">Mi Perfil Digitalizado</h1>
            <p class="mt-1 text-gray-500 text-sm">
              Resumen de tus competencias y experiencia extraídas de tu CV
            </p>
          </div>

          <!-- Acciones -->
          <div class="grid grid-cols-2 sm:flex sm:flex-wrap sm:justify-end gap-2 mb-6">
            <!-- Actualizar CV -->
            <router-link
              to="/digitalizacion/subir-cv"
              class="inline-flex items-center justify-center gap-1.5 px-3 py-2 sm:px-4 rounded-lg font-medium text-xs sm:text-sm bg-emi-gold-500 text-emi-navy-800 hover:bg-emi-gold-400 transition-colors w-full sm:w-auto"
            >
              <svg class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              {{ profile.cv_filename ? 'Actualizar CV' : 'Subir CV' }}
            </router-link>

            <!-- Ver Recomendaciones -->
            <router-link
              to="/mis-recomendaciones"
              class="inline-flex items-center justify-center gap-1.5 px-3 py-2 sm:px-4 rounded-lg font-medium text-xs sm:text-sm bg-emi-gold-500 text-emi-navy-800 hover:bg-emi-gold-400 transition-colors w-full sm:w-auto"
            >
              <svg class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <span class="sm:hidden">Recomendaciones</span>
              <span class="hidden sm:inline">Ver Recomendaciones</span>
            </router-link>

            <!-- Editar Perfil -->
            <router-link
              to="/digitalizacion/editar"
              class="inline-flex items-center justify-center gap-1.5 px-3 py-2 sm:px-4 rounded-lg font-medium text-xs sm:text-sm bg-emi-gold-500 text-emi-navy-800 hover:bg-emi-gold-400 transition-colors w-full sm:w-auto"
            >
              <svg class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              Editar Perfil
            </router-link>

            <!-- Generar CV PDF -->
            <button
              @click="generateCVPdf"
              :disabled="generatingPdf || loading"
              class="inline-flex items-center justify-center gap-1.5 px-3 py-2 sm:px-4 rounded-lg font-medium text-xs sm:text-sm bg-emi-navy-500 text-white hover:bg-emi-navy-600 transition-colors w-full sm:w-auto disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <svg v-if="!generatingPdf" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <svg v-else class="animate-spin h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <span class="sm:hidden">{{ generatingPdf ? 'Generando...' : 'Generar PDF' }}</span>
              <span class="hidden sm:inline">{{ generatingPdf ? 'Generando...' : 'Generar CV PDF' }}</span>
            </button>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
          </div>

          <!-- Error -->
          <Card v-else-if="error" class="border-red-200 bg-red-50">
            <p class="text-red-700">{{ error }}</p>
            <button @click="loadProfile" class="mt-2 text-red-600 hover:text-red-800 underline">
              Reintentar
            </button>
          </Card>

          <!-- Content + Mobile Stats -->
          <div v-else>
            <!-- Mobile Stats Bar (visible solo en < lg, reemplaza el sidebar oculto) -->
            <div class="lg:hidden mb-4 grid grid-cols-4 gap-2 p-3 bg-white rounded-xl border border-gray-200 shadow-sm">
              <div class="flex flex-col items-center">
                <span class="text-lg font-bold text-emi-navy-600">{{ Math.round(profile.completeness_score * 100) }}%</span>
                <span class="text-[11px] text-gray-500 text-center">Perfil</span>
              </div>
              <div class="flex flex-col items-center">
                <span class="text-lg font-bold text-emi-navy-600">{{ profile.hard_skills?.length ?? 0 }}</span>
                <span class="text-[11px] text-gray-500 text-center">Técnicas</span>
              </div>
              <div class="flex flex-col items-center">
                <span class="text-lg font-bold text-emi-gold-600">{{ profile.soft_skills?.length ?? 0 }}</span>
                <span class="text-[11px] text-gray-500 text-center">Blandas</span>
              </div>
              <div class="flex flex-col items-center">
                <span class="text-lg font-bold text-purple-600">{{ profile.experience_years ?? 0 }}</span>
                <span class="text-[11px] text-gray-500 text-center">Años exp.</span>
              </div>
            </div>

            <div class="space-y-4">

            <!-- Aviso sin CV -->
            <Card v-if="!profile.cv_filename" class="border-emi-gold-200 bg-emi-gold-50">
              <div class="flex items-start gap-4">
                <div class="p-3 bg-emi-gold-100 rounded-full flex-shrink-0">
                  <svg class="h-6 w-6 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-base font-semibold text-emi-gold-800">Sube tu CV para completar tu perfil</h3>
                  <p class="mt-1 text-sm text-emi-gold-700">
                    El sistema extraerá automáticamente tus competencias, formación y experiencia.
                  </p>
                  <router-link to="/digitalizacion/subir-cv" class="mt-3 inline-block btn-emi-primary text-sm">
                    Subir CV ahora
                  </router-link>
                </div>
              </div>
            </Card>

            <!-- Aviso de campos faltantes -->
            <Card v-if="completeness && completeness.missing_fields.length > 0"
              class="border-emi-gold-200 bg-emi-gold-50">
              <div class="flex items-start gap-3">
                <div class="p-2 bg-emi-gold-100 rounded-full flex-shrink-0">
                  <svg class="w-5 h-5 text-emi-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-emi-gold-800 text-sm">Para mejorar tu perfil:</h3>
                  <ul class="mt-1.5 list-disc list-inside text-sm text-emi-gold-700 space-y-0.5">
                    <li v-for="rec in completeness.recommendations" :key="rec">{{ rec }}</li>
                  </ul>
                  <router-link to="/digitalizacion/editar"
                    class="mt-2 inline-block text-sm font-medium text-emi-navy-500 hover:underline">
                    Completar perfil &rarr;
                  </router-link>
                </div>
              </div>
            </Card>

            <!-- CV info -->
            <div v-if="profile.cv_filename"
              class="flex items-center gap-3 px-4 py-3 bg-emi-navy-50 border border-emi-navy-100 rounded-lg text-sm">
              <svg class="h-5 w-5 text-emi-navy-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span class="font-medium text-emi-navy-700">{{ profile.cv_filename }}</span>
              <span class="text-emi-navy-400">·</span>
              <span class="text-emi-navy-500">Subido {{ formatDate(profile.cv_uploaded_at) }}</span>
            </div>

            <!-- ╔══════════════════════════════════╗
                 ║   DOCUMENTO CV — estilo Harvard  ║
                 ╚══════════════════════════════════╝ -->
            <div class="bg-white rounded-xl shadow-md border border-gray-100 px-8 py-8 space-y-8">

              <!-- CABECERA: Nombre + contacto + línea navy (sin botón editar) -->
              <PersonalInfoCard
                :profile="profile"
                :readOnly="true"
              />

              <!-- PERFIL PROFESIONAL (solo si hay summary de Gemini) -->
              <div v-if="geminiPersonalInfo?.summary">
                <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
                  Perfil Profesional
                </h3>
                <div class="mt-1 h-px bg-emi-navy-300"></div>
                <p class="mt-3 text-sm text-gray-700 leading-relaxed">
                  {{ geminiPersonalInfo.summary }}
                </p>
              </div>

              <!-- FORMACIÓN ACADÉMICA + EXPERIENCIA PROFESIONAL -->
              <EducationExperienceGrid
                :profile="profile"
                :geminiEducation="geminiEducation"
                :geminiExperience="geminiExperience"
                :readOnly="true"
              />

              <!-- HABILIDADES TÉCNICAS + BLANDAS + IDIOMAS -->
              <CompetenciasCard :profile="profile" :readOnly="true" />

            </div>
            <!-- fin CV document -->

            </div><!-- fin space-y-4 -->
          </div><!-- fin v-else -->
        </div>
      </div>

      <!-- Panel lateral derecho -->
      <ProfileSidebar
        :profile="profile"
        v-model:isOpen="isSecondarySidebarOpen"
        @refresh="loadProfile"
      />
    </div>

    <!-- Modal de edición (desde el sidebar o botón Editar Perfil) -->
    <EditProfileModal
      :editModal="editModal"
      :editForm="editForm"
      :saving="saving"
      :newHardSkill="newHardSkill"
      :newSoftSkill="newSoftSkill"
      :newLanguage="newLanguage"
      :newEducationEntry="newEducationEntry"
      :newExperienceEntry="newExperienceEntry"
      @close="closeEditModal"
      @save="saveChanges"
      @addSkill="addSkill"
      @removeSkill="removeSkill"
      @updateField="(field, val) => editForm[field] = val"
      @update:newHardSkill="newHardSkill = $event"
      @update:newSoftSkill="newSoftSkill = $event"
      @update:newLanguage="newLanguage = $event"
      @update:newEducationEntry="v => newEducationEntry = v"
      @update:newExperienceEntry="v => newExperienceEntry = v"
      @addEducationEntry="addEducationEntry"
      @removeEducationEntry="removeEducationEntry"
      @addExperienceEntry="addExperienceEntry"
      @removeExperienceEntry="removeExperienceEntry"
    />

    <!-- Overlay mientras se genera el PDF -->
    <Teleport to="body">
      <div
        v-if="generatingPdf"
        style="position:fixed;inset:0;background:rgba(255,255,255,0.85);z-index:9998;display:flex;align-items:center;justify-content:center;"
      >
        <div style="display:flex;flex-direction:column;align-items:center;gap:12px;">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
          <p class="text-sm text-emi-navy-700 font-medium">Generando CV en PDF...</p>
        </div>
      </div>
    </Teleport>

  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import Card from '@/shared/components/ui/Card.vue'
import ProfileSidebar from '../components/ProfileSidebar.vue'
import CompetenciasCard from '../components/CompetenciasCard.vue'
import EducationExperienceGrid from '../components/EducationExperienceGrid.vue'
import PersonalInfoCard from '../components/PersonalInfoCard.vue'
import EditProfileModal from '../components/EditProfileModal.vue'
import { useProfileEditor } from '../composables/useProfileEditor'
import { downloadCVPdf } from '../api/profile.api'

const isSecondarySidebarOpen = ref(true)
const generatingPdf = ref(false)

const {
  profile,
  completeness,
  loading,
  error,
  editModal,
  editForm,
  saving,
  newHardSkill,
  newSoftSkill,
  newLanguage,
  newEducationEntry,
  newExperienceEntry,
  geminiEducation,
  geminiExperience,
  geminiPersonalInfo,
  formatDate,
  loadProfile,
  openEditModal,
  closeEditModal,
  addSkill,
  removeSkill,
  addEducationEntry,
  removeEducationEntry,
  addExperienceEntry,
  removeExperienceEntry,
  saveChanges
} = useProfileEditor()

const generateCVPdf = async () => {
  if (generatingPdf.value) return
  generatingPdf.value = true

  try {
    const blob = await downloadCVPdf()
    const url = URL.createObjectURL(blob)
    const nombre = (profile.value.nombre_completo || 'curriculum')
      .toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
    const a = document.createElement('a')
    a.href = url
    a.download = `CV-${nombre}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Error generando CV PDF:', err)
  } finally {
    generatingPdf.value = false
  }
}
</script>
