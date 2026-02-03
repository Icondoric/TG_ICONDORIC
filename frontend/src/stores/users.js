import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useUsersStore = defineStore('users', {
    state: () => ({
        users: [],
        totalUsers: 0,
        currentUser: null,
        currentUserProfile: null,
        loading: false,
        error: null
    }),

    actions: {
        async fetchUsers({ page = 1, pageSize = 20, role = null, search = null } = {}) {
            this.loading = true
            this.error = null

            try {
                const authStore = useAuthStore()
                const params = { page, page_size: pageSize }
                if (role) params.role = role
                if (search) params.search = search

                const response = await axios.get(`${API_URL}/api/users/`, {
                    params,
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })

                this.users = response.data.usuarios
                this.totalUsers = response.data.total
                return response.data
            } catch (error) {
                console.error('Error fetching users:', error)
                this.error = error.response?.data?.detail || 'Error al cargar usuarios'
                throw error
            } finally {
                this.loading = false
            }
        },

        async fetchUser(userId) {
            this.loading = true
            this.error = null
            this.currentUser = null
            this.currentUserProfile = null

            try {
                const authStore = useAuthStore()

                // Fetch user basic info
                const userResponse = await axios.get(`${API_URL}/api/users/${userId}`, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
                this.currentUser = userResponse.data

                // If user has profile, fetch full profile details (including skills)
                if (this.currentUser.tiene_perfil) {
                    try {
                        const profileResponse = await axios.get(`${API_URL}/api/users/${userId}/profile`, {
                            headers: { Authorization: `Bearer ${authStore.token}` }
                        })
                        this.currentUserProfile = profileResponse.data
                    } catch (err) {
                        console.warn('Could not fetch full profile details', err)
                    }
                }

                return this.currentUser
            } catch (error) {
                console.error('Error fetching user details:', error)
                this.error = error.response?.data?.detail || 'Error al cargar detalle de usuario'
                throw error
            } finally {
                this.loading = false
            }
        },

        async updateUser(userId, userData) {
            this.loading = true
            this.error = null

            try {
                const authStore = useAuthStore()
                const response = await axios.put(`${API_URL}/api/users/${userId}`, userData, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })

                // Update local state if it's the current user being viewed
                if (this.currentUser && this.currentUser.id === userId) {
                    this.currentUser = { ...this.currentUser, ...response.data.user }
                }

                return response.data
            } catch (error) {
                console.error('Error updating user:', error)
                this.error = error.response?.data?.detail || 'Error al actualizar usuario'
                throw error
            } finally {
                this.loading = false
            }
        },

        async deleteUser(userId) {
            this.loading = true
            this.error = null

            try {
                const authStore = useAuthStore()
                await axios.delete(`${API_URL}/api/users/${userId}`, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })

                // Remove from local list
                this.users = this.users.filter(u => u.id !== userId)
                this.totalUsers--

                return true
            } catch (error) {
                console.error('Error deleting user:', error)
                this.error = error.response?.data?.detail || 'Error al eliminar usuario'
                throw error
            } finally {
                this.loading = false
            }
        }
    }
})
