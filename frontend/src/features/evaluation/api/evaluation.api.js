import api from '@/shared/api/client'
import { fileToBase64 } from '@/shared/api/client'

export const evaluateCV = async (file, profileId) => {
    const base64 = await fileToBase64(file)
    const response = await api.post('/api/ml/evaluate-cv', {
        cv_file: base64,
        institutional_profile_id: profileId
    })
    return response.data
}

export const getRecommendations = async (file, topN = 5) => {
    const base64 = await fileToBase64(file)
    const response = await api.post('/api/ml/get-recommendations', {
        cv_file: base64,
        top_n: topN
    })
    return response.data
}

export const getModelInfo = async () => {
    const response = await api.get('/api/ml/model-info')
    return response.data
}

export const getUserEvaluations = async (limit = 10, offset = 0) => {
    const response = await api.get('/api/ml/user-evaluations', {
        params: { limit, offset }
    })
    return response.data
}
