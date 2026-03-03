import { useAuthStore } from '@/features/auth/store/auth.store'

export function setupGuards(router) {
    router.beforeEach((to, from, next) => {
        const authStore = useAuthStore()

        // Verificar autenticacion
        if (to.meta.requiresAuth && !authStore.isAuthenticated) {
            next({ name: 'login', query: { redirect: to.fullPath } })
            return
        }

        // Helper: ¿el usuario tiene acceso a la ruta por módulo/submódulo (para roles personalizados)?
        const hasRouteModuleAccess = () => {
            const { moduleId, submoduleId } = to.meta
            if (!moduleId) return false
            return authStore.hasModuleAccess(moduleId, submoduleId)
        }

        // Verificar rol de admin solamente — o rol personalizado con acceso al módulo
        if (to.meta.requiresAdminOnly) {
            if (!authStore.isAdmin && !hasRouteModuleAccess()) {
                next({ name: 'admin-users' })
                return
            }
        }

        // Verificar rol de admin o operador — o rol personalizado con acceso al módulo
        if (to.meta.requiresAdmin) {
            if (!authStore.isAdminOrOperator && !hasRouteModuleAccess()) {
                next({ name: 'dashboard' })
                return
            }
        }

        // Redirigir usuarios autenticados fuera de login/register
        if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
            next({ name: 'dashboard' })
            return
        }

        next()
    })
}
