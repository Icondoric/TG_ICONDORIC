import api from '@/shared/api/client'

export const getMyRecommendations = async (params = {}) => {
    const response = await api.get('/api/recommendations', { params })
    return response.data
}

export const getRecommendationHistory = async (limit = 20, offset = 0) => {
    const response = await api.get('/api/recommendations/history', {
        params: { limit, offset }
    })
    return response.data
}

export const markRecommendationViewed = async (recommendationId) => {
    const response = await api.post(`/api/recommendations/${recommendationId}/viewed`)
    return response.data
}

export const checkRecommendationEligibility = async () => {
    const response = await api.get('/api/recommendations/check-eligibility')
    return response.data
}

export const getMyRecommendationStats = async () => {
    const response = await api.get('/api/recommendations/stats')
    return response.data
}
