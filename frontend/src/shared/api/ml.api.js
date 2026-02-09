import api from '@/shared/api/client'

export const getModelInfo = async () => {
    const { data } = await api.get('/api/ml/model-info')
    return data
}
