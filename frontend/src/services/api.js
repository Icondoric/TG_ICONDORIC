/**
 * API Service - Fase 7
 * Servicio centralizado para comunicacion con el backend
 */

import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import router from '../router'

// Base URL del backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Crear instancia de axios
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000, // 60 segundos para operaciones ML
    headers: {
        'Content-Type': 'application/json'
    }
})

// Interceptor de request - agregar token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Interceptor de response - manejar errores
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            // Error del servidor
            if (error.response.status === 401) {
                // Token expirado o invalido
                const authStore = useAuthStore()
                authStore.logout()
                router.push('/login')
            } else if (error.response.status === 403) {
                // Sin permisos
                router.push('/dashboard')
            }
        }
        return Promise.reject(error)
    }
)

// ============================================
// ML Endpoints
// ============================================

/**
 * Evalua un CV contra un perfil institucional
 * @param {File} file - Archivo PDF del CV
 * @param {string} profileId - UUID del perfil institucional
 */
export const evaluateCV = async (file, profileId) => {
    // Convertir archivo a base64
    const base64 = await fileToBase64(file)

    const response = await api.post('/api/ml/evaluate-cv', {
        cv_file: base64,
        institutional_profile_id: profileId
    })
    return response.data
}

/**
 * Obtiene recomendaciones de instituciones para un CV
 * @param {File} file - Archivo PDF del CV
 * @param {number} topN - Numero de recomendaciones (default: 5)
 */
export const getRecommendations = async (file, topN = 5) => {
    const base64 = await fileToBase64(file)

    const response = await api.post('/api/ml/get-recommendations', {
        cv_file: base64,
        top_n: topN
    })
    return response.data
}

/**
 * Obtiene informacion del modelo ML
 */
export const getModelInfo = async () => {
    const response = await api.get('/api/ml/model-info')
    return response.data
}

/**
 * Obtiene historial de evaluaciones del usuario
 * @param {number} limit - Limite de resultados
 * @param {number} offset - Offset para paginacion
 */
export const getUserEvaluations = async (limit = 10, offset = 0) => {
    const response = await api.get('/api/ml/user-evaluations', {
        params: { limit, offset }
    })
    return response.data
}

// ============================================
// Admin - Perfiles Institucionales
// ============================================

/**
 * Lista todos los perfiles institucionales
 * @param {boolean} includeInactive - Incluir perfiles inactivos
 * @param {string} sector - Filtrar por sector
 */
export const listProfiles = async (includeInactive = false, sector = null) => {
    const params = { include_inactive: includeInactive }
    if (sector) params.sector = sector

    const response = await api.get('/api/admin/institutional-profiles', { params })
    return response.data
}

/**
 * Obtiene un perfil institucional por ID
 * @param {string} profileId - UUID del perfil
 */
export const getProfile = async (profileId) => {
    const response = await api.get(`/api/admin/institutional-profiles/${profileId}`)
    return response.data
}

/**
 * Crea un nuevo perfil institucional
 * @param {Object} profileData - Datos del perfil
 */
export const createProfile = async (profileData) => {
    const response = await api.post('/api/admin/institutional-profiles', profileData)
    return response.data
}

/**
 * Actualiza un perfil institucional
 * @param {string} profileId - UUID del perfil
 * @param {Object} profileData - Datos a actualizar
 */
export const updateProfile = async (profileId, profileData) => {
    const response = await api.put(`/api/admin/institutional-profiles/${profileId}`, profileData)
    return response.data
}

/**
 * Elimina (soft delete) un perfil institucional
 * @param {string} profileId - UUID del perfil
 */
export const deleteProfile = async (profileId) => {
    const response = await api.delete(`/api/admin/institutional-profiles/${profileId}`)
    return response.data
}

/**
 * Reactiva un perfil institucional
 * @param {string} profileId - UUID del perfil
 */
export const activateProfile = async (profileId) => {
    const response = await api.post(`/api/admin/institutional-profiles/${profileId}/activate`)
    return response.data
}

/**
 * Lista sectores disponibles
 */
export const listSectors = async () => {
    const response = await api.get('/api/admin/sectors')
    return response.data
}

// ============================================
// Utilidades
// ============================================

/**
 * Convierte un archivo a base64
 * @param {File} file - Archivo a convertir
 */
const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => {
            // Extraer solo la parte base64 (sin el prefijo data:...)
            const base64 = reader.result.split(',')[1]
            resolve(base64)
        }
        reader.onerror = (error) => reject(error)
    })
}

/**
 * Health check del API
 */
export const healthCheck = async () => {
    const response = await api.get('/health')
    return response.data
}

// ============================================
// Perfil del Usuario (v2)
// ============================================

/**
 * Obtiene el perfil profesional del usuario autenticado
 */
export const getMyProfile = async () => {
    const response = await api.get('/api/profile/me')
    return response.data
}

/**
 * Actualiza el perfil profesional manualmente
 * @param {Object} updates - Campos a actualizar
 */
export const updateMyProfile = async (updates) => {
    const response = await api.put('/api/profile/me', updates)
    return response.data
}

/**
 * Obtiene el score de completitud del perfil
 */
export const getProfileCompleteness = async () => {
    const response = await api.get('/api/profile/completeness')
    return response.data
}

/**
 * Sube un CV y actualiza el perfil con los datos extraidos
 * @param {File} file - Archivo PDF del CV
 */
export const uploadCV = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/profile/upload-cv', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    return response.data
}

/**
 * Elimina/limpia los datos del perfil
 */
export const deleteMyProfile = async () => {
    const response = await api.delete('/api/profile/me')
    return response.data
}

/**
 * Obtiene vista previa del perfil para recomendaciones
 */
export const getProfilePreview = async () => {
    const response = await api.get('/api/profile/preview')
    return response.data
}

// ============================================
// Ofertas Laborales (Admin)
// ============================================

/**
 * Lista todas las ofertas laborales
 * @param {Object} params - Parametros de filtro
 */
export const listOfertas = async (params = {}) => {
    const response = await api.get('/api/admin/ofertas', { params })
    return response.data
}

/**
 * Obtiene una oferta por ID
 * @param {string} ofertaId - UUID de la oferta
 */
export const getOferta = async (ofertaId) => {
    const response = await api.get(`/api/admin/ofertas/${ofertaId}`)
    return response.data
}

/**
 * Crea una nueva oferta laboral
 * @param {Object} data - Datos de la oferta
 */
export const createOferta = async (data) => {
    const response = await api.post('/api/admin/ofertas', data)
    return response.data
}

/**
 * Actualiza una oferta existente
 * @param {string} ofertaId - UUID de la oferta
 * @param {Object} data - Datos a actualizar
 */
export const updateOferta = async (ofertaId, data) => {
    const response = await api.put(`/api/admin/ofertas/${ofertaId}`, data)
    return response.data
}

/**
 * Desactiva una oferta (soft delete)
 * @param {string} ofertaId - UUID de la oferta
 */
export const deleteOferta = async (ofertaId) => {
    const response = await api.delete(`/api/admin/ofertas/${ofertaId}`)
    return response.data
}

/**
 * Reactiva una oferta
 * @param {string} ofertaId - UUID de la oferta
 */
export const activateOferta = async (ofertaId) => {
    const response = await api.post(`/api/admin/ofertas/${ofertaId}/activate`)
    return response.data
}

/**
 * Obtiene estadisticas de ofertas
 */
export const getOfertasStats = async () => {
    const response = await api.get('/api/admin/ofertas/stats/summary')
    return response.data
}

// ============================================
// Recomendaciones (v2)
// ============================================

/**
 * Obtiene recomendaciones basadas en el perfil guardado
 * @param {Object} params - Parametros de filtro
 */
export const getMyRecommendations = async (params = {}) => {
    const response = await api.get('/api/recommendations', { params })
    return response.data
}

/**
 * Obtiene historial de recomendaciones
 * @param {number} limit - Limite de resultados
 * @param {number} offset - Offset para paginacion
 */
export const getRecommendationHistory = async (limit = 20, offset = 0) => {
    const response = await api.get('/api/recommendations/history', {
        params: { limit, offset }
    })
    return response.data
}

/**
 * Marca una recomendacion como vista
 * @param {string} recommendationId - UUID de la recomendacion
 */
export const markRecommendationViewed = async (recommendationId) => {
    const response = await api.post(`/api/recommendations/${recommendationId}/viewed`)
    return response.data
}

/**
 * Verifica si el usuario puede recibir recomendaciones
 */
export const checkRecommendationEligibility = async () => {
    const response = await api.get('/api/recommendations/check-eligibility')
    return response.data
}

/**
 * Obtiene estadisticas de recomendaciones del usuario
 */
export const getMyRecommendationStats = async () => {
    const response = await api.get('/api/recommendations/stats')
    return response.data
}

// ============================================
// Account Management
// ============================================

/**
 * Obtiene información de la cuenta del usuario actual
 */
export const getAccountInfo = async () => {
    const response = await api.get('/api/users/me/account')
    return response.data
}

/**
 * Actualiza información de la cuenta (nombre, email)
 * @param {Object} data - Datos a actualizar
 */
export const updateAccount = async (data) => {
    const response = await api.put('/api/users/me', data)
    return response.data
}

/**
 * Cambia la contraseña del usuario
 * @param {string} currentPassword - Contraseña actual
 * @param {string} newPassword - Nueva contraseña
 */
export const changePassword = async (currentPassword, newPassword) => {
    const response = await api.put('/api/users/me/password', {
        current_password: currentPassword,
        new_password: newPassword
    })
    return response.data
}

// Exportar instancia para uso directo si es necesario
export default api
