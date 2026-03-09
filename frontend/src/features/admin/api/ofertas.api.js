import api from '@/shared/api/client'

export const listOfertas = async (params = {}) => {
    const response = await api.get('/api/admin/convocatorias', { params })
    return response.data
}

export const getOferta = async (ofertaId) => {
    const response = await api.get(`/api/admin/convocatorias/${ofertaId}`)
    return response.data
}

export const createOferta = async (data) => {
    const response = await api.post('/api/admin/convocatorias', data)
    return response.data
}

export const updateOferta = async (ofertaId, data) => {
    const response = await api.put(`/api/admin/convocatorias/${ofertaId}`, data)
    return response.data
}

export const deleteOferta = async (ofertaId) => {
    const response = await api.delete(`/api/admin/convocatorias/${ofertaId}`)
    return response.data
}

export const permanentDeleteOferta = async (ofertaId) => {
    const response = await api.delete(`/api/admin/convocatorias/${ofertaId}/permanent`)
    return response.data
}

export const activateOferta = async (ofertaId) => {
    const response = await api.post(`/api/admin/convocatorias/${ofertaId}/activate`)
    return response.data
}

export const getOfertasStats = async () => {
    const response = await api.get('/api/admin/convocatorias/stats/summary')
    return response.data
}

export const getContactSuggestions = async (institutionId) => {
    const response = await api.get('/api/admin/convocatorias/contact-suggestions', {
        params: { institution_id: institutionId }
    })
    return response.data
}

export const analyzeOfertaPdf = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/admin/convocatorias/analyze-pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
}
