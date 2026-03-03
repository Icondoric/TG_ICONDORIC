import api from '@/shared/api/client'

export const fetchRoles = async () => {
    const response = await api.get('/api/roles/')
    return response.data
}

export const fetchRole = async (id) => {
    const response = await api.get(`/api/roles/${id}`)
    return response.data
}

export const fetchRoleByName = async (name) => {
    const response = await api.get(`/api/roles/by-name/${encodeURIComponent(name)}`)
    return response.data
}

export const createRole = async (data) => {
    const response = await api.post('/api/roles/', data)
    return response.data
}

export const updateRole = async (id, data) => {
    const response = await api.put(`/api/roles/${id}`, data)
    return response.data
}

export const deleteRole = async (id) => {
    await api.delete(`/api/roles/${id}`)
}
