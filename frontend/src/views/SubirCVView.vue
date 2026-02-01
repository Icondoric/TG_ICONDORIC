<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-gray-900">Subir CV</h1>
        <p class="mt-2 text-gray-600">
          Sube tu curriculum vitae para extraer tus competencias automaticamente
        </p>
      </div>

      <!-- Upload Card -->
      <div class="bg-white rounded-lg shadow-lg p-8">
        <!-- Step Indicator -->
        <div class="flex justify-center mb-8">
          <div class="flex items-center">
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold',
              step >= 1 ? 'bg-blue-600' : 'bg-gray-300'
            ]">1</div>
            <div :class="['w-16 h-1', step >= 2 ? 'bg-blue-600' : 'bg-gray-300']"></div>
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold',
              step >= 2 ? 'bg-blue-600' : 'bg-gray-300'
            ]">2</div>
            <div :class="['w-16 h-1', step >= 3 ? 'bg-blue-600' : 'bg-gray-300']"></div>
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold',
              step >= 3 ? 'bg-green-600' : 'bg-gray-300'
            ]">3</div>
          </div>
        </div>

        <!-- Step 1: Upload -->
        <div v-if="step === 1">
          <div
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            :class="[
              'border-2 border-dashed rounded-lg p-12 text-center transition-colors',
              isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
            ]"
          >
            <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p class="mt-4 text-lg text-gray-600">
              Arrastra tu CV aqui o
            </p>
            <label class="mt-2 cursor-pointer">
              <span class="text-blue-600 hover:text-blue-700 font-medium">selecciona un archivo</span>
              <input
                type="file"
                class="hidden"
                accept=".pdf"
                @change="handleFileSelect"
              />
            </label>
            <p class="mt-2 text-sm text-gray-500">Solo archivos PDF (max. 10MB)</p>
          </div>

          <!-- Selected File -->
          <div v-if="selectedFile" class="mt-6 p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <svg class="h-8 w-8 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                </svg>
                <div class="ml-3">
                  <p class="font-medium text-gray-900">{{ selectedFile.name }}</p>
                  <p class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
                </div>
              </div>
              <button @click="selectedFile = null" class="text-gray-400 hover:text-gray-600">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <button
              @click="uploadFile"
              :disabled="uploading"
              class="mt-4 w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {{ uploading ? 'Procesando...' : 'Procesar CV' }}
            </button>
          </div>
        </div>

        <!-- Step 2: Processing -->
        <div v-if="step === 2" class="text-center py-12">
          <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-6 text-lg text-gray-600">Extrayendo informacion de tu CV...</p>
          <p class="mt-2 text-sm text-gray-500">Esto puede tomar unos segundos</p>
        </div>

        <!-- Step 3: Results -->
        <div v-if="step === 3">
          <!-- Success Message -->
          <div class="text-center mb-8">
            <div class="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 class="mt-4 text-xl font-semibold text-gray-900">CV procesado exitosamente</h2>
            <p class="mt-2 text-gray-600">Hemos extraido la siguiente informacion de tu CV</p>
          </div>

          <!-- Extraction Summary -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-blue-50 rounded-lg p-4 text-center">
              <p class="text-2xl font-bold text-blue-600">{{ extractionSummary.hard_skills_count }}</p>
              <p class="text-sm text-gray-600">Habilidades Tecnicas</p>
            </div>
            <div class="bg-purple-50 rounded-lg p-4 text-center">
              <p class="text-2xl font-bold text-purple-600">{{ extractionSummary.soft_skills_count }}</p>
              <p class="text-sm text-gray-600">Habilidades Blandas</p>
            </div>
            <div class="bg-green-50 rounded-lg p-4 text-center">
              <p class="text-2xl font-bold text-green-600">{{ extractionSummary.education_items }}</p>
              <p class="text-sm text-gray-600">Items Educacion</p>
            </div>
            <div class="bg-orange-50 rounded-lg p-4 text-center">
              <p class="text-2xl font-bold text-orange-600">{{ extractionSummary.experience_items }}</p>
              <p class="text-sm text-gray-600">Items Experiencia</p>
            </div>
          </div>

          <!-- Extracted Skills Preview -->
          <div class="mb-6">
            <h3 class="font-medium text-gray-900 mb-3">Habilidades Tecnicas Detectadas</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="skill in resultProfile?.hard_skills?.slice(0, 10)"
                :key="skill"
                class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
              >
                {{ skill }}
              </span>
              <span v-if="resultProfile?.hard_skills?.length > 10" class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm">
                +{{ resultProfile.hard_skills.length - 10 }} mas
              </span>
            </div>
          </div>

          <!-- Languages -->
          <div v-if="extractionSummary.languages_detected?.length > 0" class="mb-6">
            <h3 class="font-medium text-gray-900 mb-3">Idiomas Detectados</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="lang in extractionSummary.languages_detected"
                :key="lang"
                class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
              >
                {{ lang }}
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-center gap-4 mt-8">
            <router-link
              to="/mi-perfil"
              class="px-6 py-3 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 font-medium"
            >
              Ver Perfil Completo
            </router-link>
            <router-link
              to="/mis-recomendaciones"
              class="px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"
            >
              Ver Recomendaciones
            </router-link>
          </div>
        </div>

        <!-- Error State -->
        <div v-if="error" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex">
            <svg class="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="ml-3">
              <p class="text-sm text-red-700">{{ error }}</p>
              <button @click="resetUpload" class="mt-2 text-sm text-red-600 hover:text-red-800 underline">
                Intentar de nuevo
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Info Card -->
      <div class="mt-6 bg-blue-50 rounded-lg p-6">
        <h3 class="font-medium text-blue-900 mb-2">Como funciona</h3>
        <ul class="text-sm text-blue-800 space-y-2">
          <li class="flex items-start">
            <span class="flex-shrink-0 w-5 h-5 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium text-blue-800 mr-2">1</span>
            Sube tu CV en formato PDF
          </li>
          <li class="flex items-start">
            <span class="flex-shrink-0 w-5 h-5 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium text-blue-800 mr-2">2</span>
            Nuestro sistema (Gemini AI) extrae tus competencias automaticamente
          </li>
          <li class="flex items-start">
            <span class="flex-shrink-0 w-5 h-5 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium text-blue-800 mr-2">3</span>
            Recibe recomendaciones de pasantias o empleos personalizadas
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadCV } from '../services/api'

const step = ref(1)
const selectedFile = ref(null)
const isDragging = ref(false)
const uploading = ref(false)
const error = ref(null)
const resultProfile = ref(null)
const extractionSummary = ref({
  hard_skills_count: 0,
  soft_skills_count: 0,
  education_items: 0,
  experience_items: 0,
  languages_detected: []
})

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  validateAndSetFile(file)
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  validateAndSetFile(file)
}

const validateAndSetFile = (file) => {
  error.value = null

  if (!file) return

  // Validate file type
  if (!file.name.toLowerCase().endsWith('.pdf')) {
    error.value = 'Solo se permiten archivos PDF'
    return
  }

  // Validate file size (10MB max)
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'El archivo excede el tamano maximo de 10MB'
    return
  }

  selectedFile.value = file
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  uploading.value = true
  error.value = null
  step.value = 2

  try {
    const result = await uploadCV(selectedFile.value)

    resultProfile.value = result.perfil
    extractionSummary.value = result.extraction_summary
    step.value = 3

  } catch (e) {
    error.value = e.response?.data?.detail || 'Error procesando el CV. Intenta de nuevo.'
    step.value = 1
  } finally {
    uploading.value = false
  }
}

const resetUpload = () => {
  step.value = 1
  selectedFile.value = null
  error.value = null
  resultProfile.value = null
}
</script>
