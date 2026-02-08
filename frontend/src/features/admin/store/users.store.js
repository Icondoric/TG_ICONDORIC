import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchUsers, fetchUser, fetchUserProfile, updateUser, deleteUser } from '@/features/admin/api/users.api'

export const useUsersStore = defineStore('users', () => {
    const users = ref([])
    const totalUsers = ref(0)
    const currentUser = ref(null)
    const currentUserProfile = ref(null)
    const loading = ref(false)
    const error = ref(null)

    async function loadUsers({ page = 1, pageSize = 20, role = null, search = null } = {}) {
        loading.value = true
        error.value = null
        try {
            const data = await fetchUsers({ page, pageSize, role, search })
            users.value = data.usuarios
            totalUsers.value = data.total
            return data
        } catch (err) {
            console.error('Error fetching users:', err)
            error.value = err.response?.data?.detail || 'Error al cargar usuarios'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function loadUser(userId) {
        loading.value = true
        error.value = null
        currentUser.value = null
        currentUserProfile.value = null
        try {
            const userData = await fetchUser(userId)
            currentUser.value = userData
            if (userData.tiene_perfil) {
                try {
                    const profileData = await fetchUserProfile(userId)
                    currentUserProfile.value = profileData
                } catch (err) {
                    console.warn('Could not fetch full profile details', err)
                }
            }
            return currentUser.value
        } catch (err) {
            console.error('Error fetching user details:', err)
            error.value = err.response?.data?.detail || 'Error al cargar detalle de usuario'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateUserAction(userId, userData) {
        loading.value = true
        error.value = null
        try {
            const data = await updateUser(userId, userData)
            if (currentUser.value && currentUser.value.id === userId) {
                currentUser.value = { ...currentUser.value, ...data.user }
            }
            return data
        } catch (err) {
            console.error('Error updating user:', err)
            error.value = err.response?.data?.detail || 'Error al actualizar usuario'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function deleteUserAction(userId) {
        loading.value = true
        error.value = null
        try {
            await deleteUser(userId)
            users.value = users.value.filter(u => u.id !== userId)
            totalUsers.value--
            return true
        } catch (err) {
            console.error('Error deleting user:', err)
            error.value = err.response?.data?.detail || 'Error al eliminar usuario'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        users, totalUsers, currentUser, currentUserProfile, loading, error,
        loadUsers, loadUser, updateUserAction, deleteUserAction
    }
})
