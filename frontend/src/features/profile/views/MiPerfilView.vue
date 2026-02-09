<template>
  <AppLayout>
    <div class="flex">
      <!-- Secondary Sidebar -->
      <ProfileSidebar
        :profile="profile"
        v-model:isOpen="isSecondarySidebarOpen"
        @refresh="loadProfile"
      />

      <!-- Main Content -->
      <div
        class="flex-1 transition-[margin] duration-300 ease-in-out min-h-screen"
        :style="{ marginLeft: isSecondarySidebarOpen ? '280px' : '60px' }"
      >
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- Header -->
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-emi-navy-500">Digitalización de Perfiles</h1>
            <p class="mt-2 text-gray-600">
              Sube tu CV para extraer automáticamente tus competencias y experiencia profesional
            </p>
          </div>

          <!-- CV Upload/Update Section -->
          <CVUploadSection
            :profile="profile"
            :formatDate="formatDate"
            @showUpload="showUploadModal = true"
            @showDelete="showDeleteConfirm = true"
          />

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-12">
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
          <div v-else class="space-y-6">
            <!-- Mobile Score Card -->
            <Card class="lg:hidden">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-lg font-semibold text-gray-900">Estado del Perfil</h2>
                  <Badge :variant="profile.is_complete ? 'gold' : 'danger'" class="mt-2">
                    {{ profile.is_complete ? 'Completo' : 'Incompleto' }}
                  </Badge>
                </div>
                <GaugeChart
                  :value="Math.round(profile.completeness_score * 100)"
                  size="sm"
                />
              </div>
              <div class="mt-4">
                <ProgressBar
                  :value="profile.completeness_score * 100"
                  label="Completitud del perfil"
                />
              </div>
              <button
                @click="showUploadModal = true"
                class="mt-4 w-full flex items-center justify-center gap-2 btn-emi-primary"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                {{ profile.cv_filename ? 'Actualizar CV' : 'Subir CV' }}
              </button>
            </Card>

            <!-- Missing Fields -->
            <Card v-if="completeness && completeness.missing_fields.length > 0" class="border-emi-gold-200 bg-emi-gold-50">
              <div class="flex items-start gap-3">
                <div class="p-2 bg-emi-gold-100 rounded-full">
                  <svg class="w-5 h-5 text-emi-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-emi-gold-800">Para mejorar tu perfil:</h3>
                  <ul class="mt-2 list-disc list-inside text-sm text-emi-gold-700 space-y-1">
                    <li v-for="rec in completeness.recommendations" :key="rec">{{ rec }}</li>
                  </ul>
                </div>
              </div>
            </Card>

            <!-- CV Info Card -->
            <Card v-if="profile.cv_filename" title="Documento CV">
              <div class="flex items-center text-gray-600">
                <div class="p-2 bg-emi-navy-100 rounded-lg mr-3">
                  <svg class="h-6 w-6 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ profile.cv_filename }}</p>
                  <p class="text-sm text-gray-500">Subido {{ formatDate(profile.cv_uploaded_at) }}</p>
                </div>
              </div>
            </Card>

            <!-- Digitalization Summary -->
            <DigitalizationSummary
              :profile="profile"
              :geminiPersonalInfo="geminiPersonalInfo"
              :geminiEducation="geminiEducation"
              :geminiExperience="geminiExperience"
              :hasGeminiData="hasGeminiData"
            />

            <!-- No CV Message -->
            <Card v-if="!profile.cv_filename" class="border-emi-gold-200 bg-emi-gold-50">
              <div class="flex items-start gap-4">
                <div class="p-3 bg-emi-gold-100 rounded-full">
                  <svg class="h-6 w-6 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-emi-gold-800">Sube tu CV para comenzar</h3>
                  <p class="mt-1 text-emi-gold-700">
                    Nuestro sistema extraera automaticamente tus competencias, formacion y experiencia.
                  </p>
                  <button @click="showUploadModal = true" class="mt-4 btn-emi-primary">
                    Subir CV ahora
                  </button>
                </div>
              </div>
            </Card>

            <!-- Competencias -->
            <CompetenciasCard :profile="profile" @edit="openEditModal" />

            <!-- Education & Experience -->
            <EducationExperienceGrid
              :profile="profile"
              :geminiEducation="geminiEducation"
              :geminiExperience="geminiExperience"
              @edit="openEditModal"
            />

            <!-- Actions Card -->
            <Card title="Acciones">
              <div class="flex flex-wrap gap-4">
                <router-link
                  to="/mis-recomendaciones"
                  class="inline-flex items-center gap-2 btn-emi-secondary"
                  :class="{ 'opacity-50 cursor-not-allowed': !profile.is_complete }"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                  Ver Recomendaciones
                </router-link>
                <button
                  @click="showDeleteConfirm = true"
                  class="inline-flex items-center gap-2 px-4 py-2 border border-red-300 rounded-lg text-red-700 bg-white hover:bg-red-50 transition-colors"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Limpiar Perfil
                </button>
              </div>
            </Card>
          </div>
        </div>

        <!-- Modals -->
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
          @close="closeEditModal"
          @save="saveChanges"
          @addSkill="addSkill"
          @removeSkill="removeSkill"
          @updateField="(field, val) => editForm[field] = val"
          @update:newHardSkill="v => newHardSkill = v"
          @update:newSoftSkill="v => newSoftSkill = v"
          @update:newLanguage="v => newLanguage = v"
        />

        <DeleteConfirmModal
          :show="showDeleteConfirm"
          :deleting="deleting"
          @cancel="showDeleteConfirm = false"
          @confirm="deleteProfile"
        />
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import GaugeChart from '@/shared/components/ui/GaugeChart.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'
import ProfileSidebar from '../components/ProfileSidebar.vue'
import CVUploadSection from '../components/CVUploadSection.vue'
import CVUploadModal from '../components/CVUploadModal.vue'
import CompetenciasCard from '../components/CompetenciasCard.vue'
import EducationExperienceGrid from '../components/EducationExperienceGrid.vue'
import EditProfileModal from '../components/EditProfileModal.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'
import DigitalizationSummary from '../components/DigitalizationSummary.vue'
import { useProfileEditor } from '../composables/useProfileEditor'

const isSecondarySidebarOpen = ref(true)

const {
  profile,
  completeness,
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
  geminiEducation,
  geminiExperience,
  geminiPersonalInfo,
  hasGeminiData,
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
  saveChanges
} = useProfileEditor()
</script>
