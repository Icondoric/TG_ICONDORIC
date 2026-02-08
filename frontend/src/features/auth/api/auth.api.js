import api from '@/shared/api/client'

export const loginUser = async (email, password) => {
    const response = await api.post('/api/auth/login', { email, password })
    return response.data
}

export const registerUser = async (email, password, rol, nombre_completo) => {
    const response = await api.post('/api/auth/register', { email, password, rol, nombre_completo })
    return response.data
}
