/**
 * Router - Fase 7
 * Configuracion de rutas incluyendo vistas ML y Admin
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Views existentes
import DashboardView from '../views/DashboardView.vue'
import LandingPage from '../views/LandingPage.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

// Views ML - Fase 7
import EvaluationView from '../views/EvaluationView.vue'
import RecommendationsView from '../views/RecommendationsView.vue'
import HistoryView from '../views/HistoryView.vue'

// Views Admin - Fase 7
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'
import ProfilesAdminView from '../views/admin/ProfilesAdminView.vue'
import ProfileFormView from '../views/admin/ProfileFormView.vue'

// Views v2 - Sistema de Recomendaciones
import MiPerfilView from '../views/MiPerfilView.vue'
import SubirCVView from '../views/SubirCVView.vue'
import MisRecomendacionesView from '../views/MisRecomendacionesView.vue'
import OfertasAdminView from '../views/admin/OfertasAdminView.vue'
import OfertaFormView from '../views/admin/OfertaFormView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        // Rutas publicas
        {
            path: '/',
            name: 'landing',
            component: LandingPage,
            meta: { hideNavbar: false }
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterView
        },

        // Rutas de usuario autenticado
        {
            path: '/dashboard',
            name: 'dashboard',
            component: DashboardView,
            meta: { requiresAuth: true }
        },

        // Rutas ML - Fase 7
        {
            path: '/evaluation',
            name: 'evaluation',
            component: EvaluationView,
            meta: { requiresAuth: false } // Opcional, funciona sin auth
        },
        {
            path: '/recommendations',
            name: 'recommendations',
            component: RecommendationsView,
            meta: { requiresAuth: false }
        },
        {
            path: '/history',
            name: 'history',
            component: HistoryView,
            meta: { requiresAuth: true }
        },

        // Rutas Admin - Fase 7
        {
            path: '/admin',
            name: 'admin',
            component: AdminDashboardView,
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/admin/profiles',
            name: 'admin-profiles',
            component: ProfilesAdminView,
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/admin/profiles/new',
            name: 'admin-profiles-new',
            component: ProfileFormView,
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/admin/profiles/:id/edit',
            name: 'admin-profiles-edit',
            component: ProfileFormView,
            meta: { requiresAuth: true, requiresAdmin: true }
        },

        // Rutas v2 - Usuario
        {
            path: '/mi-perfil',
            name: 'mi-perfil',
            component: MiPerfilView,
            meta: { requiresAuth: true }
        },
        {
            path: '/subir-cv',
            name: 'subir-cv',
            component: SubirCVView,
            meta: { requiresAuth: true }
        },
        {
            path: '/mis-recomendaciones',
            name: 'mis-recomendaciones',
            component: MisRecomendacionesView,
            meta: { requiresAuth: true }
        },

        // Rutas v2 - Admin Ofertas
        {
            path: '/admin/ofertas',
            name: 'admin-ofertas',
            component: OfertasAdminView,
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/admin/ofertas/new',
            name: 'admin-ofertas-new',
            component: OfertaFormView,
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/admin/ofertas/edit/:id',
            name: 'admin-ofertas-edit',
            component: OfertaFormView,
            meta: { requiresAuth: true, requiresAdmin: true }
        },

        // Catch-all redirect
        {
            path: '/:pathMatch(.*)*',
            redirect: '/'
        }
    ]
})

// Navigation guards
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Verificar autenticacion
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } })
        return
    }

    // Verificar rol de admin
    if (to.meta.requiresAdmin && !authStore.isAdmin) {
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

export default router
