<script setup>
/**
 * HistoryView - Fase 7
 * Vista para ver el historial de evaluaciones del usuario
 */

import { ref, onMounted, computed } from 'vue'
import { useEvaluationStore } from '@/features/evaluation/store/evaluation.store'
import { useAuthStore } from '@/features/auth/store/auth.store'

const mlStore = useEvaluationStore()
const authStore = useAuthStore()

// Estado local
const currentPage = ref(1)
const itemsPerPage = ref(10)
const selectedEvaluation = ref(null)

// Cargar historial al montar
onMounted(async () => {
    if (authStore.isAuthenticated) {
        await loadHistory()
    }
})

// Computed
const totalPages = computed(() => {
    return Math.ceil(mlStore.historyTotal / itemsPerPage.value)
})

const paginatedHistory = computed(() => {
    return mlStore.evaluationHistory
})

// Methods
const loadHistory = async () => {
    const offset = (currentPage.value - 1) * itemsPerPage.value
    try {
        await mlStore.loadEvaluationHistory(itemsPerPage.value, offset)
    } catch (error) {
        console.error('Error cargando historial:', error)
    }
}

const changePage = async (page) => {
    currentPage.value = page
    await loadHistory()
}

const viewDetails = (evaluation) => {
    selectedEvaluation.value = evaluation
}

const closeDetails = () => {
    selectedEvaluation.value = null
}

// Helpers
const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

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
            <h1 class="text-3xl font-bold text-slate-800">Historial de Evaluaciones</h1>
            <p class="mt-2 text-slate-600">
                Revisa todas tus evaluaciones de CV anteriores
            </p>
        </header>

        <!-- No autenticado -->
        <div v-if="!authStore.isAuthenticated" class="bg-white rounded-xl shadow-md p-8 text-center">
            <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <h3 class="text-lg font-medium text-slate-600">Inicia sesion para ver tu historial</h3>
            <p class="text-sm text-slate-400 mt-2 mb-4">
                Necesitas estar autenticado para acceder a tu historial de evaluaciones
            </p>
            <router-link
                to="/login"
                class="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
                Iniciar Sesion
            </router-link>
        </div>

        <!-- Loading -->
        <div v-else-if="mlStore.isLoadingHistory" class="bg-white rounded-xl shadow-md p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-4 text-slate-500">Cargando historial...</p>
        </div>

        <!-- Error -->
        <div v-else-if="mlStore.historyError" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-700">{{ mlStore.historyError }}</p>
            <button
                @click="loadHistory"
                class="mt-2 text-sm text-red-600 underline hover:text-red-800"
            >
                Reintentar
            </button>
        </div>

        <!-- Contenido -->
        <div v-else>
            <!-- Sin historial -->
            <div v-if="paginatedHistory.length === 0" class="bg-white rounded-xl shadow-md p-8 text-center">
                <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 class="text-lg font-medium text-slate-600">No tienes evaluaciones aun</h3>
                <p class="text-sm text-slate-400 mt-2 mb-4">
                    Evalua tu CV contra perfiles institucionales para ver tu historial aqui
                </p>
                <router-link
                    to="/evaluation"
                    class="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    Evaluar mi CV
                </router-link>
            </div>

            <!-- Lista de Evaluaciones -->
            <div v-else class="space-y-4">
                <!-- Stats -->
                <div class="bg-white rounded-xl shadow-md p-4 flex items-center justify-between">
                    <span class="text-slate-600">
                        Total: <span class="font-semibold">{{ mlStore.historyTotal }}</span> evaluaciones
                    </span>
                    <span class="text-sm text-slate-500">
                        Pagina {{ currentPage }} de {{ totalPages }}
                    </span>
                </div>

                <!-- Cards -->
                <div
                    v-for="evaluation in paginatedHistory"
                    :key="evaluation.id"
                    class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                    @click="viewDetails(evaluation)"
                >
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-lg font-semibold text-slate-800">
                                {{ evaluation.institution_name || 'Institucion' }}
                            </h3>
                            <p class="text-sm text-slate-500 mt-1">
                                {{ formatDate(evaluation.evaluated_at) }}
                            </p>
                        </div>
                        <div class="text-right">
                            <span :class="['px-3 py-1 rounded-full text-sm font-medium', getClassificationBadge(evaluation.classification)]">
                                {{ evaluation.classification?.replace('_', ' ') || 'N/A' }}
                            </span>
                            <p class="mt-2 text-2xl font-bold" :class="{
                                'text-green-600': evaluation.match_score >= 0.7,
                                'text-yellow-600': evaluation.match_score >= 0.5 && evaluation.match_score < 0.7,
                                'text-red-600': evaluation.match_score < 0.5
                            }">
                                {{ formatScore(evaluation.match_score) }}%
                            </p>
                        </div>
                    </div>

                    <!-- Barra de progreso -->
                    <div class="mt-4">
                        <div class="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                            <div
                                class="h-full rounded-full"
                                :class="{
                                    'bg-green-500': evaluation.match_score >= 0.7,
                                    'bg-yellow-500': evaluation.match_score >= 0.5 && evaluation.match_score < 0.7,
                                    'bg-red-500': evaluation.match_score < 0.5
                                }"
                                :style="{ width: `${formatScore(evaluation.match_score)}%` }"
                            ></div>
                        </div>
                    </div>
                </div>

                <!-- Paginacion -->
                <div v-if="totalPages > 1" class="flex justify-center space-x-2 mt-6">
                    <button
                        @click="changePage(currentPage - 1)"
                        :disabled="currentPage === 1"
                        class="px-4 py-2 rounded-lg border border-slate-200 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
                    >
                        Anterior
                    </button>

                    <template v-for="page in totalPages" :key="page">
                        <button
                            v-if="page === 1 || page === totalPages || (page >= currentPage - 1 && page <= currentPage + 1)"
                            @click="changePage(page)"
                            :class="[
                                'px-4 py-2 rounded-lg border',
                                currentPage === page
                                    ? 'bg-blue-600 text-white border-blue-600'
                                    : 'border-slate-200 hover:bg-slate-50'
                            ]"
                        >
                            {{ page }}
                        </button>
                        <span
                            v-else-if="page === 2 || page === totalPages - 1"
                            class="px-2 py-2 text-slate-400"
                        >
                            ...
                        </span>
                    </template>

                    <button
                        @click="changePage(currentPage + 1)"
                        :disabled="currentPage === totalPages"
                        class="px-4 py-2 rounded-lg border border-slate-200 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
                    >
                        Siguiente
                    </button>
                </div>
            </div>
        </div>

        <!-- Modal de Detalles -->
        <Teleport to="body">
            <div
                v-if="selectedEvaluation"
                class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
                @click.self="closeDetails"
            >
                <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                    <!-- Header -->
                    <div class="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
                        <h3 class="text-xl font-semibold text-slate-800">
                            Detalles de Evaluacion
                        </h3>
                        <button
                            @click="closeDetails"
                            class="text-slate-400 hover:text-slate-600"
                        >
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Contenido -->
                    <div class="p-6 space-y-6">
                        <!-- Info General -->
                        <div>
                            <p class="text-sm text-slate-500">Institucion</p>
                            <p class="text-lg font-semibold text-slate-800">
                                {{ selectedEvaluation.institution_name || 'N/A' }}
                            </p>
                            <p class="text-sm text-slate-400 mt-1">
                                {{ formatDate(selectedEvaluation.evaluated_at) }}
                            </p>
                        </div>

                        <!-- Score Principal -->
                        <div class="text-center py-4">
                            <span :class="['px-4 py-2 rounded-full text-lg font-bold', getClassificationBadge(selectedEvaluation.classification)]">
                                {{ selectedEvaluation.classification?.replace('_', ' ') }}
                            </span>
                            <p class="text-5xl font-bold mt-4" :class="{
                                'text-green-600': selectedEvaluation.match_score >= 0.7,
                                'text-yellow-600': selectedEvaluation.match_score >= 0.5 && selectedEvaluation.match_score < 0.7,
                                'text-red-600': selectedEvaluation.match_score < 0.5
                            }">
                                {{ formatScore(selectedEvaluation.match_score) }}%
                            </p>
                            <p class="text-slate-500">Match Score</p>
                        </div>

                        <!-- Scores por Dimension -->
                        <div v-if="selectedEvaluation.cv_scores">
                            <h4 class="font-medium text-slate-700 mb-3">Puntuacion por Dimension</h4>
                            <div class="space-y-3">
                                <div
                                    v-for="(score, dimension) in selectedEvaluation.cv_scores"
                                    :key="dimension"
                                    class="space-y-1"
                                >
                                    <div class="flex justify-between text-sm">
                                        <span class="text-slate-600 capitalize">{{ dimension.replace('_', ' ') }}</span>
                                        <span class="font-medium">{{ formatScore(score) }}%</span>
                                    </div>
                                    <div class="w-full bg-slate-200 rounded-full h-2">
                                        <div
                                            class="h-full rounded-full bg-blue-500"
                                            :style="{ width: `${formatScore(score)}%` }"
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Teleport>
    </div>
</template>
