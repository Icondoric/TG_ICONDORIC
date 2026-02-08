import api from '@/shared/api/client'

export const listProfiles = async (includeInactive = false, sector = null) => {
    const params = { include_inactive: includeInactive }
    if (sector) params.sector = sector
    const response = await api.get('/api/admin/institutional-profiles', { params })
    return response.data
}

export const getProfile = async (profileId) => {
    const response = await api.get(`/api/admin/institutional-profiles/${profileId}`)
    return response.data
}

export const createProfile = async (profileData) => {
    const response = await api.post('/api/admin/institutional-profiles', profileData)
    return response.data
}

export const updateProfile = async (profileId, profileData) => {
    const response = await api.put(`/api/admin/institutional-profiles/${profileId}`, profileData)
    return response.data
}

export const deleteProfile = async (profileId) => {
    const response = await api.delete(`/api/admin/institutional-profiles/${profileId}`)
    return response.data
}

export const activateProfile = async (profileId) => {
    const response = await api.post(`/api/admin/institutional-profiles/${profileId}/activate`)
    return response.data
}

export const listSectors = async () => {
    const response = await api.get('/api/admin/sectors')
    return response.data
}
