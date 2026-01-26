import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { jwtDecode } from 'jwt-decode'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token'))
    const user = ref(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null)

    const isAuthenticated = computed(() => !!token.value)
    const isAdmin = computed(() => user.value?.rol === 'admin' || user.value?.rol === 'administrador')

    async function login(email, password) {
        try {
            const response = await axios.post('http://localhost:8000/api/auth/login', {
                email,
                password
            })

            const data = response.data
            // Store all relevant user info returned by backend
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
            const response = await axios.post('http://localhost:8000/api/auth/register', {
                email,
                password,
                rol,
                nombre_completo
            })
            const data = response.data
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

        // Configurar header por defecto para futuras peticiones (si tuviéramos instancia global de axios)
        // axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
    }

    return { token, user, isAuthenticated, isAdmin, login, register, logout }
})
