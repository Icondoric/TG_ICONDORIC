import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginUser, registerUser } from '@/features/auth/api/auth.api'
import { FIXED_ROLE_MODULES } from '@/shared/constants/modules'

const FIXED_ROLES = Object.keys(FIXED_ROLE_MODULES)

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token'))
    const user = ref(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null)
    // allowedModules: { moduleId: [submoduleId, ...] } | null  (null = usar FIXED_ROLE_MODULES)
    const allowedModules = ref(localStorage.getItem('allowedModules') ? JSON.parse(localStorage.getItem('allowedModules')) : null)

    const isAuthenticated = computed(() => !!token.value)
    const isAdmin = computed(() => user.value?.rol === 'admin' || user.value?.rol === 'administrador')
    const isOperator = computed(() => user.value?.rol === 'operador')
    const isAdminOrOperator = computed(() => isAdmin.value || isOperator.value)

    /**
     * Verifica si el usuario tiene acceso a un módulo y opcionalmente a un sub-módulo.
     * @param {string} moduleId
     * @param {string|null} submoduleId
     */
    function hasModuleAccess(moduleId, submoduleId = null) {
        const rol = user.value?.rol
        if (!rol) return false

        // Obtener el mapa de permisos { moduleId: [submoduleId, ...] }
        const perms = FIXED_ROLES.includes(rol) ? FIXED_ROLE_MODULES[rol] : allowedModules.value

        if (!perms) return false

        // Compatibilidad con formato antiguo (array plano de IDs de módulo)
        if (Array.isArray(perms)) return perms.includes(moduleId)

        // Formato nuevo: { moduleId: [submoduleId, ...] }
        if (!(moduleId in perms)) return false
        if (!submoduleId) return true

        return Array.isArray(perms[moduleId]) && perms[moduleId].includes(submoduleId)
    }

    async function login(email, password) {
        try {
            const data = await loginUser(email, password)
            await setSession(data.access_token, {
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
            await setSession(data.access_token, {
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

    async function setSession(newToken, userData) {
        token.value = newToken
        user.value = userData
        localStorage.setItem('token', newToken)
        localStorage.setItem('user', JSON.stringify(userData))

        // Si es rol personalizado, cargar sus permisos desde el backend
        if (!FIXED_ROLES.includes(userData.rol)) {
            await _loadCustomRolePerms(userData.rol)
        } else {
            allowedModules.value = null
            localStorage.removeItem('allowedModules')
        }
    }

    async function _loadCustomRolePerms(rolName) {
        try {
            const { fetchRoleByName } = await import('@/features/system/api/roles.api')
            const result = await fetchRoleByName(rolName)
            allowedModules.value = result.modulos_permitidos
            localStorage.setItem('allowedModules', JSON.stringify(result.modulos_permitidos))
            console.log('[Auth] Permisos cargados para rol personalizado:', rolName, result.modulos_permitidos)
        } catch (err) {
            console.error('[Auth] Error cargando permisos del rol personalizado:', rolName, err?.response?.data || err?.message || err)
            allowedModules.value = {}
            localStorage.setItem('allowedModules', '{}')
        }
    }

    function logout() {
        token.value = null
        user.value = null
        allowedModules.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('allowedModules')
    }

    async function reloadPermissions() {
        const rol = user.value?.rol
        if (!rol || FIXED_ROLES.includes(rol)) return
        await _loadCustomRolePerms(rol)
    }

    return { token, user, allowedModules, isAuthenticated, isAdmin, isOperator, isAdminOrOperator, hasModuleAccess, login, register, logout, reloadPermissions }
})
