import { useAuthStore } from '@/features/auth/store/auth.store'

export function setupGuards(router) {
    router.beforeEach((to, from, next) => {
        const authStore = useAuthStore()

        // Verificar autenticacion
        if (to.meta.requiresAuth && !authStore.isAuthenticated) {
            next({ name: 'login', query: { redirect: to.fullPath } })
            return
        }

        // Verificar rol de admin solamente (ej: dashboard admin)
        if (to.meta.requiresAdminOnly && !authStore.isAdmin) {
            next({ name: 'admin-users' })
            return
        }

        // Verificar rol de admin o operador
        if (to.meta.requiresAdmin && !authStore.isAdminOrOperator) {
            next({ name: 'dashboard' })
            return
        }

        // Redirigir usuarios autenticados fuera de login/register
        if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
            next({ name: 'dashboard' })
            return
        }

        next()
    })
}
