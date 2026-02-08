import api from '@/shared/api/client'

export const fetchUsers = async ({ page = 1, pageSize = 20, role = null, search = null } = {}) => {
    const params = { page, page_size: pageSize }
    if (role) params.role = role
    if (search) params.search = search
    const response = await api.get('/api/users/', { params })
    return response.data
}

export const fetchUser = async (userId) => {
    const response = await api.get(`/api/users/${userId}`)
    return response.data
}

export const fetchUserProfile = async (userId) => {
    const response = await api.get(`/api/users/${userId}/profile`)
    return response.data
}

export const updateUser = async (userId, userData) => {
    const response = await api.put(`/api/users/${userId}`, userData)
    return response.data
}

export const deleteUser = async (userId) => {
    await api.delete(`/api/users/${userId}`)
}
