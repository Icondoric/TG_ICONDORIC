import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginUser, registerUser } from '@/features/auth/api/auth.api'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token'))
    const user = ref(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null)

    const isAuthenticated = computed(() => !!token.value)
    const isAdmin = computed(() => user.value?.rol === 'admin' || user.value?.rol === 'administrador')
    const isOperator = computed(() => user.value?.rol === 'operador' || user.value?.rol === 'administrador')

    async function login(email, password) {
        try {
            const data = await loginUser(email, password)
            setSession(data.access_token, {
                user_id: data.user_id,
                rol: data.rol,
                email: data.email,
                nombre_completo: data.nombre_completo
            })
            return true
        } catch (error) {
            throw error.response?.data?.detail || "Error al iniciar sesión"
        }
    }

    async function register(email, password, rol, nombre_completo) {
        try {
            const data = await registerUser(email, password, rol, nombre_completo)
            setSession(data.access_token, {
                user_id: data.user_id,
                rol: data.rol,
                email: data.email,
                nombre_completo: data.nombre_completo
            })
            return true
        } catch (error) {
            throw error.response?.data?.detail || "Error al registrarse"
        }
    }

    function setSession(newToken, userData) {
        token.value = newToken
        user.value = userData
        localStorage.setItem('token', newToken)
        localStorage.setItem('user', JSON.stringify(userData))
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    }

    return { token, user, isAuthenticated, isAdmin, isOperator, login, register, logout }
})
