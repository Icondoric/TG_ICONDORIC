import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { evaluateCV, getRecommendations, getUserEvaluations, getModelInfo } from '@/features/evaluation/api/evaluation.api'

export const useEvaluationStore = defineStore('evaluation', () => {
    const currentEvaluation = ref(null)
    const isEvaluating = ref(false)
    const evaluationError = ref(null)

    const recommendations = ref([])
    const isLoadingRecommendations = ref(false)
    const recommendationsError = ref(null)

    const evaluationHistory = ref([])
    const historyTotal = ref(0)
    const isLoadingHistory = ref(false)
    const historyError = ref(null)

    const modelInfo = ref(null)

    const isModelReady = computed(() => {
        return modelInfo.value?.is_ready === true || modelInfo.value?.status === 'loaded'
    })

    async function evaluateCVAction(file, profileId) {
        isEvaluating.value = true
        evaluationError.value = null
        currentEvaluation.value = null
        try {
            const result = await evaluateCV(file, profileId)
            currentEvaluation.value = result
            return result
        } catch (error) {
            evaluationError.value = error.response?.data?.detail || 'Error al evaluar CV'
            throw error
        } finally {
            isEvaluating.value = false
        }
    }

    async function getRecommendationsAction(file, topN = 5) {
        isLoadingRecommendations.value = true
        recommendationsError.value = null
        recommendations.value = []
        try {
            const result = await getRecommendations(file, topN)
            recommendations.value = result.recommendations || []
            return result
        } catch (error) {
            recommendationsError.value = error.response?.data?.detail || 'Error al obtener recomendaciones'
            throw error
        } finally {
            isLoadingRecommendations.value = false
        }
    }

    async function loadEvaluationHistory(limit = 10, offset = 0) {
        isLoadingHistory.value = true
        historyError.value = null
        try {
            const result = await getUserEvaluations(limit, offset)
            evaluationHistory.value = result.evaluations || []
            historyTotal.value = result.total || 0
            return result
        } catch (error) {
            historyError.value = error.response?.data?.detail || 'Error al cargar historial'
            throw error
        } finally {
            isLoadingHistory.value = false
        }
    }

    async function loadModelInfo() {
        try {
            const result = await getModelInfo()
            modelInfo.value = result
            return result
        } catch (error) {
            console.error('Error cargando info del modelo:', error)
            return null
        }
    }

    function resetEvaluation() {
        currentEvaluation.value = null
        evaluationError.value = null
    }

    function resetRecommendations() {
        recommendations.value = []
        recommendationsError.value = null
    }

    function resetAll() {
        currentEvaluation.value = null
        isEvaluating.value = false
        evaluationError.value = null
        recommendations.value = []
        isLoadingRecommendations.value = false
        recommendationsError.value = null
        evaluationHistory.value = []
        historyTotal.value = 0
    }

    return {
        currentEvaluation, isEvaluating, evaluationError,
        recommendations, isLoadingRecommendations, recommendationsError,
        evaluationHistory, historyTotal, isLoadingHistory, historyError,
        modelInfo, isModelReady,
        evaluateCVAction, getRecommendationsAction, loadEvaluationHistory,
        loadModelInfo, resetEvaluation, resetRecommendations, resetAll
    }
})
