<template>
  <AppLayout>
    <div class="flex min-h-screen">
      <!-- Main Content -->
      <div class="flex-1 min-w-0">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

          <!-- Header -->
          <div class="mb-6 flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-emi-navy-500">Editar Perfil</h1>
              <p class="mt-1 text-gray-500 text-sm">
                Modifica tus competencias, formación y experiencia profesional
              </p>
            </div>
            <router-link
              to="/digitalizacion/mi-perfil"
              class="inline-flex items-center gap-2 btn-emi-secondary"
            >
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Ver Perfil
            </router-link>
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

          <!-- Content -->
          <div v-else class="space-y-4">

            <!-- Sección CV upload -->
            <CVUploadSection
              :profile="profile"
              :formatDate="formatDate"
              @showUpload="showUploadModal = true"
              @showDelete="showDeleteConfirm = true"
            />

            <!-- ╔══════════════════════════════════╗
                 ║   DOCUMENTO CV — estilo Harvard  ║
                 ╚══════════════════════════════════╝ -->
            <div class="bg-white rounded-xl shadow-md border border-gray-100 px-8 py-8 space-y-8">

              <!-- CABECERA: Nombre + contacto + línea navy -->
              <PersonalInfoCard
                :profile="profile"
                @edit="openEditModal('personal_info')"
              />

              <!-- PERFIL PROFESIONAL (solo lectura, viene de Gemini) -->
              <div v-if="geminiPersonalInfo?.summary">
                <h3 class="text-xs font-bold text-emi-navy-500 uppercase tracking-widest">
                  Perfil Profesional
                </h3>
                <div class="mt-1 h-px bg-emi-navy-300"></div>
                <p class="mt-3 text-sm text-gray-700 leading-relaxed">
                  {{ geminiPersonalInfo.summary }}
                </p>
              </div>

              <!-- FORMACIÓN ACADÉMICA + EXPERIENCIA PROFESIONAL (editable) -->
              <EducationExperienceGrid
                :profile="profile"
                :geminiEducation="geminiEducation"
                :geminiExperience="geminiExperience"
                @edit="openEditModal"
              />

              <!-- HABILIDADES TÉCNICAS + BLANDAS + IDIOMAS (editable) -->
              <CompetenciasCard :profile="profile" @edit="openEditModal" />

            </div>
            <!-- fin CV document -->

            <!-- Zona de peligro -->
            <Card class="border-red-200">
              <h2 class="text-base font-semibold text-red-700 mb-3">Zona de peligro</h2>
              <p class="text-sm text-gray-600 mb-3">
                Elimina todos los datos de tu perfil digitalizado. Esta acción no se puede deshacer.
              </p>
              <button
                @click="showDeleteConfirm = true"
                class="inline-flex items-center gap-2 px-4 py-2 border border-red-300 rounded-lg text-red-700 bg-white hover:bg-red-50 transition-colors text-sm"
              >
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Limpiar Perfil
              </button>
            </Card>

          </div>
        </div>

        <!-- Modales -->
        <CVUploadModal
          :show="showUploadModal"
          :uploadFile="uploadFile"
          :uploading="uploading"
          :isDragging="isDragging"
          :formatFileSize="formatFileSize"
          @close="showUploadModal = false; uploadFile = null"
          @dragOver="isDragging = true"
          @dragLeave="isDragging = false"
          @drop="handleDrop"
          @fileSelect="handleFileSelect"
          @process="processCV"
        />

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
          @update:newHardSkill="v => newHardSkill = v"
          @update:newSoftSkill="v => newSoftSkill = v"
          @update:newLanguage="v => newLanguage = v"
          @update:newEducationEntry="v => newEducationEntry = v"
          @update:newExperienceEntry="v => newExperienceEntry = v"
          @addEducationEntry="addEducationEntry"
          @removeEducationEntry="removeEducationEntry"
          @addExperienceEntry="addExperienceEntry"
          @removeExperienceEntry="removeExperienceEntry"
        />

        <DeleteConfirmModal
          :show="showDeleteConfirm"
          :deleting="deleting"
          @cancel="showDeleteConfirm = false"
          @confirm="deleteProfile"
        />
      </div>

      <!-- Panel lateral derecho -->
      <ProfileSidebar
        :profile="profile"
        v-model:isOpen="isSecondarySidebarOpen"
        @refresh="loadProfile"
      />
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import Card from '@/shared/components/ui/Card.vue'
import ProfileSidebar from '../components/ProfileSidebar.vue'
import CVUploadSection from '../components/CVUploadSection.vue'
import CVUploadModal from '../components/CVUploadModal.vue'
import PersonalInfoCard from '../components/PersonalInfoCard.vue'
import CompetenciasCard from '../components/CompetenciasCard.vue'
import EducationExperienceGrid from '../components/EducationExperienceGrid.vue'
import EditProfileModal from '../components/EditProfileModal.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'
import { useProfileEditor } from '../composables/useProfileEditor'

const isSecondarySidebarOpen = ref(true)

const {
  profile,
  loading,
  error,
  showDeleteConfirm,
  deleting,
  showUploadModal,
  uploadFile,
  uploading,
  isDragging,
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
  formatFileSize,
  loadProfile,
  deleteProfile,
  handleFileSelect,
  handleDrop,
  processCV,
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
</script>
