import api from '@/shared/api/client'

export const getMyProfile = async () => {
    const response = await api.get('/api/profile/me')
    return response.data
}

export const updateMyProfile = async (updates) => {
    const response = await api.put('/api/profile/me', updates)
    return response.data
}

export const getProfileCompleteness = async () => {
    const response = await api.get('/api/profile/completeness')
    return response.data
}

export const uploadCV = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/profile/upload-cv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
}

export const deleteMyProfile = async () => {
    const response = await api.delete('/api/profile/me')
    return response.data
}

export const getProfilePreview = async () => {
    const response = await api.get('/api/profile/preview')
    return response.data
}
