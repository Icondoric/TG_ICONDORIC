import api from '@/shared/api/client'

export const getAccountInfo = async () => {
    const response = await api.get('/api/users/me/account')
    return response.data
}

export const updateAccount = async (data) => {
    const response = await api.put('/api/users/me', data)
    return response.data
}

export const changePassword = async (currentPassword, newPassword) => {
    const response = await api.put('/api/users/me/password', {
        current_password: currentPassword,
        new_password: newPassword
    })
    return response.data
}
