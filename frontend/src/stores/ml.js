/**
 * ML Store - Fase 7
 * Store Pinia para gestion de estado ML
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
    evaluateCV,
    getRecommendations,
    getUserEvaluations,
    getModelInfo,
    listProfiles,
    getProfile,
    createProfile,
    updateProfile,
    deleteProfile,
    activateProfile,
    listSectors
} from '../services/api'

export const useMLStore = defineStore('ml', () => {
    // ============================================
    // State
    // ============================================

    // Estado de evaluacion actual
    const currentEvaluation = ref(null)
    const isEvaluating = ref(false)
    const evaluationError = ref(null)

    // Estado de recomendaciones
    const recommendations = ref([])
    const isLoadingRecommendations = ref(false)
    const recommendationsError = ref(null)

    // Historial de evaluaciones
    const evaluationHistory = ref([])
    const historyTotal = ref(0)
    const isLoadingHistory = ref(false)
    const historyError = ref(null)

    // Perfiles institucionales
    const profiles = ref([])
    const currentProfile = ref(null)
    const isLoadingProfiles = ref(false)
    const profilesError = ref(null)

    // Sectores
    const sectors = ref([])

    // Informacion del modelo
    const modelInfo = ref(null)

    // ============================================
    // Computed
    // ============================================

    const hasActiveProfiles = computed(() => {
        return profiles.value.some(p => p.is_active)
    })

    const activeProfiles = computed(() => {
        return profiles.value.filter(p => p.is_active)
    })

    const isModelReady = computed(() => {
        return modelInfo.value?.is_ready === true || modelInfo.value?.status === 'loaded'
    })

    // ============================================
    // Actions - Evaluaciones
    // ============================================

    /**
     * Evalua un CV contra un perfil institucional
     */
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

    /**
     * Obtiene recomendaciones de instituciones
     */
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

    /**
     * Carga el historial de evaluaciones del usuario
     */
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

    // ============================================
    // Actions - Perfiles (Admin)
    // ============================================

    /**
     * Carga todos los perfiles institucionales
     */
    async function loadProfiles(includeInactive = false, sector = null) {
        isLoadingProfiles.value = true
        profilesError.value = null

        try {
            const result = await listProfiles(includeInactive, sector)
            profiles.value = result.profiles || []
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al cargar perfiles'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    /**
     * Carga un perfil especifico
     */
    async function loadProfile(profileId) {
        isLoadingProfiles.value = true
        profilesError.value = null

        try {
            const result = await getProfile(profileId)
            currentProfile.value = result
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al cargar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    /**
     * Crea un nuevo perfil institucional
     */
    async function createProfileAction(profileData) {
        isLoadingProfiles.value = true
        profilesError.value = null

        try {
            const result = await createProfile(profileData)
            // Agregar a la lista local
            profiles.value.unshift(result)
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al crear perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    /**
     * Actualiza un perfil institucional
     */
    async function updateProfileAction(profileId, profileData) {
        isLoadingProfiles.value = true
        profilesError.value = null

        try {
            const result = await updateProfile(profileId, profileData)
            // Actualizar en la lista local
            const index = profiles.value.findIndex(p => p.id === profileId)
            if (index !== -1) {
                profiles.value[index] = result
            }
            if (currentProfile.value?.id === profileId) {
                currentProfile.value = result
            }
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al actualizar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    /**
     * Elimina (desactiva) un perfil institucional
     */
    async function deleteProfileAction(profileId) {
        isLoadingProfiles.value = true
        profilesError.value = null

        try {
            await deleteProfile(profileId)
            // Actualizar estado local
            const index = profiles.value.findIndex(p => p.id === profileId)
            if (index !== -1) {
                profiles.value[index].is_active = false
            }
            return true
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al eliminar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    /**
     * Reactiva un perfil institucional
     */
    async function activateProfileAction(profileId) {
        isLoadingProfiles.value = true
        profilesError.value = null

        try {
            await activateProfile(profileId)
            // Actualizar estado local
            const index = profiles.value.findIndex(p => p.id === profileId)
            if (index !== -1) {
                profiles.value[index].is_active = true
            }
            return true
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al activar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    /**
     * Carga sectores disponibles
     */
    async function loadSectors() {
        try {
            const result = await listSectors()
            sectors.value = result.sectors || []
            return result
        } catch (error) {
            console.error('Error cargando sectores:', error)
            return { sectors: [] }
        }
    }

    // ============================================
    // Actions - Modelo
    // ============================================

    /**
     * Carga informacion del modelo ML
     */
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

    // ============================================
    // Actions - Reset
    // ============================================

    /**
     * Resetea el estado de evaluacion
     */
    function resetEvaluation() {
        currentEvaluation.value = null
        evaluationError.value = null
    }

    /**
     * Resetea el estado de recomendaciones
     */
    function resetRecommendations() {
        recommendations.value = []
        recommendationsError.value = null
    }

    /**
     * Resetea todo el estado
     */
    function resetAll() {
        currentEvaluation.value = null
        isEvaluating.value = false
        evaluationError.value = null
        recommendations.value = []
        isLoadingRecommendations.value = false
        recommendationsError.value = null
        evaluationHistory.value = []
        historyTotal.value = 0
        currentProfile.value = null
    }

    return {
        // State
        currentEvaluation,
        isEvaluating,
        evaluationError,
        recommendations,
        isLoadingRecommendations,
        recommendationsError,
        evaluationHistory,
        historyTotal,
        isLoadingHistory,
        historyError,
        profiles,
        currentProfile,
        isLoadingProfiles,
        profilesError,
        sectors,
        modelInfo,

        // Computed
        hasActiveProfiles,
        activeProfiles,
        isModelReady,

        // Actions - Evaluaciones
        evaluateCVAction,
        getRecommendationsAction,
        loadEvaluationHistory,

        // Actions - Perfiles
        loadProfiles,
        loadProfile,
        createProfileAction,
        updateProfileAction,
        deleteProfileAction,
        activateProfileAction,
        loadSectors,

        // Actions - Modelo
        loadModelInfo,

        // Actions - Reset
        resetEvaluation,
        resetRecommendations,
        resetAll
    }
})
