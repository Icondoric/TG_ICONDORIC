<script setup>
import { ref } from 'vue'
import axios from 'axios'
import ProfileEditor from './ProfileEditor.vue'

const fileInput = ref(null)
const selectedFile = ref(null)
const isUploading = ref(false)
const error = ref(null)
const profileData = ref(null)
const rawPreview = ref("")

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0]
  error.value = null
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  isUploading.value = true
  error.value = null
  
  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    // Assuming backend is running on localhost:8000
    const response = await axios.post('http://localhost:8000/api/upload-cv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    profileData.value = response.data.data
    rawPreview.value = response.data.raw_text_preview
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.detail || "Error al subir el archivo. Asegúrate de que el backend esté corriendo."
  } finally {
    isUploading.value = false
  }
}

const reset = () => {
  profileData.value = null
  selectedFile.value = null
  if(fileInput.value) fileInput.value.value = ""
}
</script>

<template>
  <div class="space-y-8">
    <!-- Upload Section -->
    <div v-if="!profileData" class="bg-white p-8 rounded-xl shadow-lg border border-slate-100 transition-all hover:shadow-xl">
      <h2 class="text-2xl font-bold text-slate-800 mb-6">Subir CV (PDF)</h2>
      
      <div class="flex items-center justify-center w-full">
        <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-64 border-2 border-slate-300 border-dashed rounded-lg cursor-pointer bg-slate-50 hover:bg-slate-100 transition-colors">
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
                <svg class="w-10 h-10 mb-4 text-slate-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                </svg>
                <p class="mb-2 text-sm text-slate-500"><span class="font-semibold">Haz clic para subir</span> o arrastra y suelta</p>
                <p class="text-xs text-slate-500">Solo archivos PDF</p>
            </div>
            <input id="dropzone-file" type="file" ref="fileInput" @change="handleFileChange" accept="application/pdf" class="hidden" />
        </label>
      </div> 

      <div v-if="selectedFile" class="mt-4 flex items-center justify-between p-4 bg-blue-50 text-blue-700 rounded-lg">
        <span class="font-medium truncate">{{ selectedFile.name }}</span>
        <button @click="uploadFile" :disabled="isUploading" class="ml-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
          {{ isUploading ? 'Analizando...' : 'Analizar CV' }}
        </button>
      </div>

      <div v-if="error" class="mt-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">
        {{ error }}
      </div>
    </div>

    <div v-else>
      <!-- Editor Section -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-slate-800">Validación de Perfil</h2>
        <button @click="reset" class="text-sm text-slate-500 hover:text-slate-700 underline">Subir otro archivo</button>
      </div>
      
      <ProfileEditor :initial-data="profileData" />
    </div>
  </div>
</template>
