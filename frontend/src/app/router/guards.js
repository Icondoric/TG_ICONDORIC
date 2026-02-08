import { useAuthStore } from '@/features/auth/store/auth.store'

export function setupGuards(router) {
    router.beforeEach((to, from, next) => {
        const authStore = useAuthStore()

        // Verificar autenticacion
        if (to.meta.requiresAuth && !authStore.isAuthenticated) {
            next({ name: 'login', query: { redirect: to.fullPath } })
            return
        }

        // Verificar rol de admin o operador
        if (to.meta.requiresAdmin && !authStore.isOperator) {
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
