<script setup>
/**
 * EvaluationView - Fase 7
 * Vista para evaluar un CV contra un perfil institucional
 */

import { ref, onMounted, computed } from 'vue'
import { useEvaluationStore } from '@/features/evaluation/store/evaluation.store'
import { useAuthStore } from '@/features/auth/store/auth.store'
import ScoreChart from '@/features/evaluation/components/ScoreChart.vue'
import EvaluationResult from '@/features/evaluation/components/EvaluationResult.vue'

const mlStore = useEvaluationStore()
const authStore = useAuthStore()

// Estado local
const fileInput = ref(null)
const selectedFile = ref(null)
const selectedProfileId = ref('')
const step = ref(1) // 1: Seleccionar, 2: Resultado

// Cargar perfiles activos al montar
onMounted(async () => {
    try {
        await mlStore.loadProfiles(false) // Solo activos
    } catch (error) {
        console.error('Error cargando perfiles:', error)
    }
})

// Computed
const canEvaluate = computed(() => {
    return selectedFile.value && selectedProfileId.value && !mlStore.isEvaluating
})

const selectedProfile = computed(() => {
    return mlStore.activeProfiles.find(p => p.id === selectedProfileId.value)
})

// Methods
const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file && file.type === 'application/pdf') {
        selectedFile.value = file
    } else {
        alert('Por favor selecciona un archivo PDF valido')
        event.target.value = ''
    }
}

const handleDrop = (event) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file && file.type === 'application/pdf') {
        selectedFile.value = file
    }
}

const handleDragOver = (event) => {
    event.preventDefault()
}

const evaluate = async () => {
    if (!canEvaluate.value) return

    try {
        await mlStore.evaluateCVAction(selectedFile.value, selectedProfileId.value)
        step.value = 2
    } catch (error) {
        console.error('Error en evaluacion:', error)
    }
}

const reset = () => {
    mlStore.resetEvaluation()
    selectedFile.value = null
    selectedProfileId.value = ''
    step.value = 1
    if (fileInput.value) fileInput.value.value = ''
}
</script>

<template>
    <div class="max-w-5xl mx-auto py-8 px-4">
        <!-- Header -->
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-slate-800">Evaluacion de CV</h1>
            <p class="mt-2 text-slate-600">
                Evalua tu CV contra los requisitos de una institucion especifica
            </p>
        </header>

        <!-- Step 1: Seleccion -->
        <div v-if="step === 1" class="space-y-6">
            <!-- Seleccionar Perfil -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <h2 class="text-xl font-semibold text-slate-800 mb-4">
                    1. Selecciona una Institucion
                </h2>

                <div v-if="mlStore.isLoadingProfiles" class="text-center py-8">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                    <p class="mt-2 text-slate-500">Cargando instituciones...</p>
                </div>

                <div v-else-if="mlStore.activeProfiles.length === 0" class="text-center py-8">
                    <p class="text-slate-500">No hay perfiles institucionales disponibles</p>
                </div>

                <div v-else class="grid gap-4 md:grid-cols-2">
                    <label
                        v-for="profile in mlStore.activeProfiles"
                        :key="profile.id"
                        :class="[
                            'relative flex cursor-pointer rounded-lg border p-4 transition-all hover:border-blue-400',
                            selectedProfileId === profile.id
                                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                                : 'border-slate-200 bg-white'
                        ]"
                    >
                        <input
                            type="radio"
                            v-model="selectedProfileId"
                            :value="profile.id"
                            class="sr-only"
                        />
                        <div class="flex-1">
                            <p class="font-semibold text-slate-800">{{ profile.institution_name }}</p>
                            <p class="text-sm text-slate-500 mt-1">{{ profile.sector }}</p>
                            <p v-if="profile.description" class="text-sm text-slate-400 mt-2 line-clamp-2">
                                {{ profile.description }}
                            </p>
                        </div>
                        <div
                            v-if="selectedProfileId === profile.id"
                            class="absolute top-3 right-3 text-blue-500"
                        >
                            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                            </svg>
                        </div>
                    </label>
                </div>
            </div>

            <!-- Subir CV -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <h2 class="text-xl font-semibold text-slate-800 mb-4">
                    2. Sube tu CV
                </h2>

                <div
                    @drop="handleDrop"
                    @dragover="handleDragOver"
                    :class="[
                        'flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-lg cursor-pointer transition-colors',
                        selectedFile ? 'border-green-400 bg-green-50' : 'border-slate-300 bg-slate-50 hover:bg-slate-100'
                    ]"
                    @click="$refs.fileInput.click()"
                >
                    <template v-if="!selectedFile">
                        <svg class="w-10 h-10 mb-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        <p class="text-sm text-slate-500">
                            <span class="font-semibold">Haz clic</span> o arrastra tu CV
                        </p>
                        <p class="text-xs text-slate-400 mt-1">Solo archivos PDF</p>
                    </template>
                    <template v-else>
                        <svg class="w-10 h-10 mb-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p class="text-sm font-medium text-green-700">{{ selectedFile.name }}</p>
                        <p class="text-xs text-green-600 mt-1">
                            {{ (selectedFile.size / 1024).toFixed(1) }} KB
                        </p>
                    </template>
                </div>
                <input
                    ref="fileInput"
                    type="file"
                    accept="application/pdf"
                    @change="handleFileChange"
                    class="hidden"
                />
            </div>

            <!-- Error -->
            <div v-if="mlStore.evaluationError" class="bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-red-700">{{ mlStore.evaluationError }}</p>
            </div>

            <!-- Boton Evaluar -->
            <div class="flex justify-end">
                <button
                    @click="evaluate"
                    :disabled="!canEvaluate"
                    :class="[
                        'px-8 py-3 rounded-lg font-semibold text-white transition-all',
                        canEvaluate
                            ? 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
                            : 'bg-slate-300 cursor-not-allowed'
                    ]"
                >
                    <span v-if="mlStore.isEvaluating" class="flex items-center">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Analizando...
                    </span>
                    <span v-else>Evaluar CV</span>
                </button>
            </div>
        </div>

        <!-- Step 2: Resultado -->
        <div v-else-if="step === 2 && mlStore.currentEvaluation">
            <EvaluationResult
                :evaluation="mlStore.currentEvaluation"
                :profile="selectedProfile"
                @reset="reset"
            />
        </div>
    </div>
</template>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>
