
<template>
  <AppLayout>
    <div class="min-h-screen bg-gray-50 py-8">
      <!-- Aumentamos el ancho máximo para aprovechar pantallas grandes -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <!-- Header Principal -->
        <div class="mb-8 text-center lg:text-left lg:flex lg:items-end lg:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-emi-navy-500">Subir CV</h1>
            <p class="mt-2 text-gray-600">
              Sube tu curriculum vitae para extraer tus competencias automáticamente
            </p>
          </div>
          <!-- Opcional: Podrías poner un botón de ayuda aquí en el futuro -->
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <!-- COLUMNA IZQUIERDA: Contenido Principal (Upload/Results) -->
          <div class="lg:col-span-8">
            <div class="bg-white rounded-xl shadow-lg p-8 min-h-[500px] flex flex-col">
              
              <!-- Step Indicator -->
              <div class="mb-10">
                <div class="flex justify-center items-start">
                  <!-- Paso 1 -->
                  <div class="flex flex-col items-center w-20">
                    <div :class="[
                      'w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold transition-all duration-300',
                      step >= 1 ? 'bg-emi-navy-500 ring-4 ring-emi-navy-100' : 'bg-gray-300'
                    ]">1</div>
                    <span class="mt-2 text-xs font-medium text-center leading-tight"
                          :class="step === 1 ? 'text-emi-navy-600' : 'text-gray-400'">
                      Subida
                    </span>
                  </div>

                  <!-- Línea 1-2 -->
                  <div class="flex-1 mt-5 mx-1">
                    <div :class="['h-1 rounded-full transition-all duration-500', step >= 2 ? 'bg-emi-navy-500' : 'bg-gray-200']"></div>
                  </div>

                  <!-- Paso 2 -->
                  <div class="flex flex-col items-center w-20">
                    <div :class="[
                      'w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold transition-all duration-300',
                      step >= 2 ? 'bg-emi-navy-500 ring-4 ring-emi-navy-100' : 'bg-gray-300'
                    ]">2</div>
                    <span class="mt-2 text-xs font-medium text-center leading-tight"
                          :class="step === 2 ? 'text-emi-navy-600' : 'text-gray-400'">
                      Proceso
                    </span>
                  </div>

                  <!-- Línea 2-3 -->
                  <div class="flex-1 mt-5 mx-1">
                    <div :class="['h-1 rounded-full transition-all duration-500', step >= 3 ? 'bg-green-500' : 'bg-gray-200']"></div>
                  </div>

                  <!-- Paso 3 -->
                  <div class="flex flex-col items-center w-20">
                    <div :class="[
                      'w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold transition-all duration-300',
                      step >= 3 ? 'bg-green-600 ring-4 ring-green-100' : 'bg-gray-300'
                    ]">3</div>
                    <span class="mt-2 text-xs font-medium text-center leading-tight"
                          :class="step === 3 ? 'text-green-600' : 'text-gray-400'">
                      Resultado
                    </span>
                  </div>
                </div>

                <!-- Banner de etapa activa -->
                <div class="mt-5">
                  <transition name="step-badge" mode="out-in">
                    <div
                      :key="step"
                      class="rounded-lg px-4 py-3 flex items-center gap-3 border-l-4"
                      :class="stepInfo.bannerClass"
                    >
                      <!-- Ícono -->
                      <div class="flex-shrink-0">
                        <svg v-if="step === 1" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                        </svg>
                        <svg v-else-if="step === 2" class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <!-- Texto -->
                      <div>
                        <p class="text-xs font-semibold uppercase tracking-widest opacity-70">Paso {{ step }} de 3</p>
                        <p class="text-sm font-bold leading-tight">{{ stepInfo.label }}</p>
                      </div>
                    </div>
                  </transition>
                </div>
              </div>

              <!-- Content Area -->
              <div class="flex-grow">
                <!-- Step 1: Upload -->
                <div v-if="step === 1" class="transition-all duration-300">
                  <div
                    @dragover.prevent="isDragging = true"
                    @dragleave.prevent="isDragging = false"
                    @drop.prevent="handleDrop"
                    :class="[
                      'border-2 border-dashed rounded-xl p-12 text-center cursor-pointer group',
                      isDragging
                        ? 'border-blue-500 bg-blue-50 scale-[1.01]'
                        : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50/40 dropzone-idle'
                    ]"
                    style="transition: border-color 0.25s ease, background-color 0.25s ease, transform 0.2s ease;"
                  >
                    <svg
                      class="mx-auto h-16 w-16 transition-transform duration-300 group-hover:scale-110"
                      :class="isDragging ? 'text-blue-500' : 'text-gray-400'"
                      fill="none" viewBox="0 0 24 24" stroke="currentColor"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p class="mt-4 text-base text-gray-500">
                      Arrastra tu CV aquí o
                    </p>
                    <label class="mt-2 cursor-pointer inline-block">
                      <span class="text-blue-600 hover:text-blue-700 font-medium text-base underline decoration-dashed underline-offset-2 transition-colors">selecciona un archivo</span>
                      <input
                        type="file"
                        class="hidden"
                        accept=".pdf"
                        @change="handleFileSelect"
                      />
                    </label>
                    <p class="mt-2 text-sm text-gray-500">Solo archivos PDF (máx. 10MB)</p>
                  </div>

                  <!-- Selected File -->
                  <div v-if="selectedFile" class="mt-6 p-4 bg-gray-50 border border-gray-200 rounded-lg animate-fade-in">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <svg class="h-8 w-8 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                        </svg>
                        <div class="ml-3">
                          <p class="font-medium text-gray-900 truncate max-w-xs">{{ selectedFile.name }}</p>
                          <p class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
                        </div>
                      </div>
                      <button @click="selectedFile = null" class="text-gray-400 hover:text-gray-600 p-2">
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>

                    <button
                      @click="uploadFile"
                      :disabled="uploading"
                      class="mt-4 w-full btn-emi-primary py-3 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                      {{ uploading ? 'Procesando documento...' : 'Procesar CV' }}
                    </button>
                  </div>
                </div>

                <!-- Step 2: Processing -->
                <div v-if="step === 2" class="text-center py-20">
                  <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-emi-navy-500 mx-auto"></div>
                  <p class="mt-6 text-lg font-medium text-gray-800">Extrayendo información de tu CV...</p>
                  <p class="mt-2 text-sm text-gray-500">Esto puede tomar unos segundos. Gracias por la espera.</p>
                </div>

                <!-- Step 3: Results -->
                <div v-if="step === 3" class="animate-fade-in">
                  <!-- Success Message -->
                  <div class="text-center mb-8">
                    <div class="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                      <svg class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <h2 class="text-2xl font-bold text-gray-900">CV procesado exitosamente</h2>
                    <p class="mt-2 text-gray-600">Hemos extraído la siguiente información de tu perfil</p>
                  </div>

                  <!-- Extraction Summary Grid -->
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div class="bg-blue-50 border border-blue-100 rounded-xl p-4 text-center transform transition-transform hover:scale-105">
                      <p class="text-3xl font-bold text-emi-navy-500">{{ extractionSummary.hard_skills_count }}</p>
                      <p class="text-xs font-medium text-gray-600 uppercase tracking-wide mt-1">Hab. Técnicas</p>
                    </div>
                    <div class="bg-purple-50 border border-purple-100 rounded-xl p-4 text-center transform transition-transform hover:scale-105">
                      <p class="text-3xl font-bold text-purple-600">{{ extractionSummary.soft_skills_count }}</p>
                      <p class="text-xs font-medium text-gray-600 uppercase tracking-wide mt-1">Hab. Blandas</p>
                    </div>
                    <div class="bg-green-50 border border-green-100 rounded-xl p-4 text-center transform transition-transform hover:scale-105">
                      <p class="text-3xl font-bold text-green-600">{{ extractionSummary.education_items }}</p>
                      <p class="text-xs font-medium text-gray-600 uppercase tracking-wide mt-1">Educación</p>
                    </div>
                    <div class="bg-orange-50 border border-orange-100 rounded-xl p-4 text-center transform transition-transform hover:scale-105">
                      <p class="text-3xl font-bold text-orange-600">{{ extractionSummary.experience_items }}</p>
                      <p class="text-xs font-medium text-gray-600 uppercase tracking-wide mt-1">Experiencia</p>
                    </div>
                  </div>

                  <!-- Extracted Skills Preview -->
                  <div class="mb-6 bg-white border border-gray-100 shadow-sm rounded-lg p-5">
                    <h3 class="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                      Habilidades Técnicas Detectadas
                    </h3>
                    <div class="flex flex-wrap gap-2">
                      <span
                        v-for="skill in resultProfile?.hard_skills?.slice(0, 10)"
                        :key="skill"
                        class="px-3 py-1.5 bg-blue-50 border border-blue-200 text-blue-800 rounded-full text-sm font-medium"
                      >
                        {{ skill }}
                      </span>
                      <span v-if="resultProfile?.hard_skills?.length > 10" class="px-3 py-1.5 bg-gray-100 text-gray-600 rounded-full text-sm font-medium">
                        +{{ resultProfile.hard_skills.length - 10 }} más
                      </span>
                    </div>
                  </div>

                  <!-- Languages -->
                  <div v-if="extractionSummary.languages_detected?.length > 0" class="mb-8 bg-white border border-gray-100 shadow-sm rounded-lg p-5">
                    <h3 class="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path></svg>
                      Idiomas Detectados
                    </h3>
                    <div class="flex flex-wrap gap-2">
                      <span
                        v-for="lang in extractionSummary.languages_detected"
                        :key="lang"
                        class="px-3 py-1.5 bg-green-50 border border-green-200 text-green-800 rounded-full text-sm font-medium"
                      >
                        {{ lang }}
                      </span>
                    </div>
                  </div>

                  <!-- Actions -->
                  <div class="flex flex-col sm:flex-row justify-center gap-4 mt-8 pt-6 border-t border-gray-100">
                    <router-link
                      to="/digitalizacion/mi-perfil"
                      class="px-6 py-3 border-2 border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50 hover:border-gray-300 font-semibold text-center transition-colors"
                    >
                      Ver Perfil Completo
                    </router-link>
                    <router-link
                      to="/mis-recomendaciones"
                      class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold shadow-md hover:shadow-lg text-center transition-all"
                    >
                      Ver Recomendaciones
                    </router-link>
                  </div>
                </div>

                <!-- Error State -->
                <div v-if="error" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg animate-fade-in">
                  <div class="flex items-start">
                    <svg class="h-5 w-5 text-red-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-red-800">Hubo un problema</h3>
                      <p class="text-sm text-red-700 mt-1">{{ error }}</p>
                      <button @click="resetUpload" class="mt-2 text-sm font-medium text-red-600 hover:text-red-800 underline">
                        Intentar de nuevo
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- COLUMNA DERECHA: Sidebar Informativo (Sticky) -->
          <div class="lg:col-span-4">
            <div class="bg-emi-navy-50 border border-emi-navy-100 rounded-xl p-6 shadow-sm sticky top-8">
              <h3 class="text-lg font-semibold text-emi-navy-900 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-emi-navy-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                ¿Cómo funciona?
              </h3>
              <ul class="text-sm text-emi-navy-800 space-y-4">
                <li class="flex items-start">
                  <span class="flex-shrink-0 w-6 h-6 bg-emi-navy-200 rounded-full flex items-center justify-center text-xs font-bold text-emi-navy-900 mr-3 mt-0.5">1</span>
                  <span class="leading-relaxed">Sube tu CV actualizado en formato <strong>PDF</strong>.</span>
                </li>
                <li class="flex items-start">
                  <span class="flex-shrink-0 w-6 h-6 bg-emi-navy-200 rounded-full flex items-center justify-center text-xs font-bold text-emi-navy-900 mr-3 mt-0.5">2</span>
                  <span class="leading-relaxed">Nuestro sistema procesa el documento y <strong>extrae tus competencias</strong> automáticamente.</span>
                </li>
                <li class="flex items-start">
                  <span class="flex-shrink-0 w-6 h-6 bg-emi-navy-200 rounded-full flex items-center justify-center text-xs font-bold text-emi-navy-900 mr-3 mt-0.5">3</span>
                  <span class="leading-relaxed">Recibe <strong>recomendaciones personalizadas</strong> de pasantías o empleos basados en tu perfil.</span>
                </li>
              </ul>
              
              <div class="mt-6 pt-6 border-t border-emi-navy-100/60">
                <p class="text-xs text-emi-navy-600 text-center">
                  Tus datos están seguros y solo se usarán para mejorar tus recomendaciones laborales.
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import { uploadCV } from '@/features/profile/api/profile.api'
import { formatApiError } from '@/shared/utils/apiError'

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

const stepInfo = computed(() => {
  const steps = {
    1: {
      label: 'Selección de archivo',
      bannerClass: 'bg-emi-navy-50 border-emi-navy-500 text-emi-navy-800'
    },
    2: {
      label: 'Procesando tu CV...',
      bannerClass: 'bg-blue-50 border-blue-500 text-blue-800'
    },
    3: {
      label: '¡Extracción completada!',
      bannerClass: 'bg-green-50 border-green-500 text-green-800'
    },
  }
  return steps[step.value] || steps[1]
})

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

  if (!file.name.toLowerCase().endsWith('.pdf')) {
    error.value = 'Solo se permiten archivos PDF'
    return
  }

  if (file.size > 10 * 1024 * 1024) {
    error.value = 'El archivo excede el tamaño máximo de 10MB'
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
    error.value = formatApiError(e, 'Error procesando el CV. Intenta de nuevo.')
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

<style scoped>

.step-badge-enter-active,
.step-badge-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.step-badge-enter-from {
  opacity: 0;
  transform: translateY(6px) scale(0.95);
}
.step-badge-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.95);
}

/* Animación suave en reposo del área de subida */
@keyframes dropzone-pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(96, 165, 250, 0);
    border-color: #d1d5db; /* gray-300 */
  }
  50% {
    box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.15);
    border-color: #93c5fd; /* blue-300 */
  }
}
.dropzone-idle {
  animation: dropzone-pulse 3s ease-in-out infinite;
}
</style>
