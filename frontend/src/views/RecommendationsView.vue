<script setup>
/**
 * RecommendationsView - Fase 7
 * Vista para obtener recomendaciones de instituciones basadas en un CV
 */

import { ref, computed } from 'vue'
import { useMLStore } from '../stores/ml'
import { useRouter } from 'vue-router'

const mlStore = useMLStore()
const router = useRouter()

// Estado local
const fileInput = ref(null)
const selectedFile = ref(null)
const topN = ref(5)
const hasResults = ref(false)

// Computed
const canGetRecommendations = computed(() => {
    return selectedFile.value && !mlStore.isLoadingRecommendations
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

const getRecommendations = async () => {
    if (!canGetRecommendations.value) return

    try {
        await mlStore.getRecommendationsAction(selectedFile.value, topN.value)
        hasResults.value = true
    } catch (error) {
        console.error('Error obteniendo recomendaciones:', error)
    }
}

const reset = () => {
    mlStore.resetRecommendations()
    selectedFile.value = null
    hasResults.value = false
    if (fileInput.value) fileInput.value.value = ''
}

const goToEvaluation = (profileId) => {
    router.push({
        name: 'evaluation',
        query: { profile: profileId }
    })
}

// Helpers
const getClassificationBadge = (classification) => {
    const badges = {
        'APTO': 'bg-green-100 text-green-700',
        'CONSIDERADO': 'bg-yellow-100 text-yellow-700',
        'NO_APTO': 'bg-red-100 text-red-700'
    }
    return badges[classification] || badges['NO_APTO']
}

const formatScore = (score) => {
    return Math.round((score || 0) * 100)
}
</script>

<template>
    <div class="max-w-5xl mx-auto py-8 px-4">
        <!-- Header -->
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-slate-800">Recomendaciones</h1>
            <p class="mt-2 text-slate-600">
                Descubre las instituciones que mejor se ajustan a tu perfil
            </p>
        </header>

        <!-- Formulario de Upload -->
        <div v-if="!hasResults" class="space-y-6">
            <div class="bg-white rounded-xl shadow-md p-6">
                <h2 class="text-xl font-semibold text-slate-800 mb-4">
                    Sube tu CV para obtener recomendaciones
                </h2>

                <!-- Dropzone -->
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

                <!-- Opciones -->
                <div class="mt-6 flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <label class="text-sm text-slate-600">Mostrar top:</label>
                        <select
                            v-model="topN"
                            class="px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option :value="3">3 instituciones</option>
                            <option :value="5">5 instituciones</option>
                            <option :value="10">10 instituciones</option>
                        </select>
                    </div>

                    <button
                        @click="getRecommendations"
                        :disabled="!canGetRecommendations"
                        :class="[
                            'px-6 py-3 rounded-lg font-semibold text-white transition-all',
                            canGetRecommendations
                                ? 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
                                : 'bg-slate-300 cursor-not-allowed'
                        ]"
                    >
                        <span v-if="mlStore.isLoadingRecommendations" class="flex items-center">
                            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Analizando...
                        </span>
                        <span v-else>Obtener Recomendaciones</span>
                    </button>
                </div>
            </div>

            <!-- Error -->
            <div v-if="mlStore.recommendationsError" class="bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-red-700">{{ mlStore.recommendationsError }}</p>
            </div>
        </div>

        <!-- Resultados -->
        <div v-else class="space-y-6">
            <!-- Header de Resultados -->
            <div class="flex justify-between items-center">
                <div>
                    <h2 class="text-xl font-semibold text-slate-800">
                        {{ mlStore.recommendations.length }} Instituciones Recomendadas
                    </h2>
                    <p class="text-sm text-slate-500 mt-1">
                        Ordenadas por compatibilidad con tu perfil
                    </p>
                </div>
                <button
                    @click="reset"
                    class="px-4 py-2 text-slate-600 hover:text-slate-800 font-medium transition-colors"
                >
                    Nueva Busqueda
                </button>
            </div>

            <!-- Lista de Recomendaciones -->
            <div class="space-y-4">
                <div
                    v-for="rec in mlStore.recommendations"
                    :key="rec.profile_id"
                    class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
                >
                    <div class="flex items-start justify-between">
                        <!-- Info Principal -->
                        <div class="flex items-start space-x-4">
                            <!-- Ranking -->
                            <div class="flex-shrink-0 w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                                <span class="text-xl font-bold text-blue-600">#{{ rec.rank }}</span>
                            </div>

                            <div>
                                <h3 class="text-lg font-semibold text-slate-800">
                                    {{ rec.institution_name }}
                                </h3>
                                <p class="text-sm text-slate-500">{{ rec.sector }}</p>

                                <!-- Badges -->
                                <div class="flex items-center space-x-3 mt-2">
                                    <span :class="['px-3 py-1 rounded-full text-sm font-medium', getClassificationBadge(rec.classification)]">
                                        {{ rec.classification.replace('_', ' ') }}
                                    </span>
                                    <span class="text-sm text-slate-500">
                                        {{ formatScore(rec.match_score) }}% match
                                    </span>
                                </div>

                                <!-- Fortaleza Principal -->
                                <p v-if="rec.main_strength" class="mt-3 text-sm text-slate-600">
                                    <span class="text-green-600 font-medium">Fortaleza:</span>
                                    {{ rec.main_strength }}
                                </p>
                            </div>
                        </div>

                        <!-- Score Visual -->
                        <div class="text-right">
                            <div class="text-3xl font-bold" :class="{
                                'text-green-600': rec.match_score >= 0.7,
                                'text-yellow-600': rec.match_score >= 0.5 && rec.match_score < 0.7,
                                'text-red-600': rec.match_score < 0.5
                            }">
                                {{ formatScore(rec.match_score) }}%
                            </div>
                            <button
                                @click="goToEvaluation(rec.profile_id)"
                                class="mt-3 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-medium rounded-lg transition-colors"
                            >
                                Ver Detalles
                            </button>
                        </div>
                    </div>

                    <!-- Barra de Progreso -->
                    <div class="mt-4">
                        <div class="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                            <div
                                class="h-full rounded-full transition-all duration-500"
                                :class="{
                                    'bg-green-500': rec.match_score >= 0.7,
                                    'bg-yellow-500': rec.match_score >= 0.5 && rec.match_score < 0.7,
                                    'bg-red-500': rec.match_score < 0.5
                                }"
                                :style="{ width: `${formatScore(rec.match_score)}%` }"
                            ></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sin resultados -->
            <div v-if="mlStore.recommendations.length === 0" class="bg-white rounded-xl shadow-md p-8 text-center">
                <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 class="text-lg font-medium text-slate-600">No se encontraron recomendaciones</h3>
                <p class="text-sm text-slate-400 mt-2">
                    Intenta subir un CV diferente o verifica que existan perfiles institucionales activos
                </p>
            </div>
        </div>
    </div>
</template>
