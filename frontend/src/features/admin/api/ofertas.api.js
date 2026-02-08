import api from '@/shared/api/client'

export const listOfertas = async (params = {}) => {
    const response = await api.get('/api/admin/ofertas', { params })
    return response.data
}

export const getOferta = async (ofertaId) => {
    const response = await api.get(`/api/admin/ofertas/${ofertaId}`)
    return response.data
}

export const createOferta = async (data) => {
    const response = await api.post('/api/admin/ofertas', data)
    return response.data
}

export const updateOferta = async (ofertaId, data) => {
    const response = await api.put(`/api/admin/ofertas/${ofertaId}`, data)
    return response.data
}

export const deleteOferta = async (ofertaId) => {
    const response = await api.delete(`/api/admin/ofertas/${ofertaId}`)
    return response.data
}

export const activateOferta = async (ofertaId) => {
    const response = await api.post(`/api/admin/ofertas/${ofertaId}/activate`)
    return response.data
}

export const getOfertasStats = async () => {
    const response = await api.get('/api/admin/ofertas/stats/summary')
    return response.data
}
