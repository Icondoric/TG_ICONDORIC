/**
 * Router - Optimized with Lazy Loading
 * All routes use dynamic imports for code splitting
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Eager load only critical routes (Landing Page for fast initial render)
import LandingPage from '../views/LandingPage.vue'

// Lazy load all other views for better performance
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const DashboardView = () => import('../views/DashboardView.vue')

// ML Views - Lazy loaded
const EvaluationView = () => import('../views/EvaluationView.vue')
const RecommendationsView = () => import('../views/RecommendationsView.vue')
const HistoryView = () => import('../views/HistoryView.vue')

// Admin Views - Lazy loaded
const AdminDashboardView = () => import('../views/admin/AdminDashboardView.vue')
const ProfilesAdminView = () => import('../views/admin/ProfilesAdminView.vue')
const ProfileFormView = () => import('../views/admin/ProfileFormView.vue')
const UsersAdminView = () => import('../views/admin/UsersAdminView.vue')
const UserDetailView = () => import('../views/admin/UserDetailView.vue')
const ReportsView = () => import('../views/admin/ReportsView.vue')

// Student Views - Lazy loaded
const MiPerfilView = () => import('../views/MiPerfilView.vue')
const SubirCVView = () => import('../views/SubirCVView.vue')
const MisRecomendacionesView = () => import('../views/MisRecomendacionesView.vue')
const AccountSettingsView = () => import('../views/AccountSettingsView.vue')

// Admin Ofertas - Lazy loaded
const OfertasAdminView = () => import('../views/admin/OfertasAdminView.vue')
const OfertaFormView = () => import('../views/admin/OfertaFormView.vue')

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
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },
        {
            path: '/admin/profiles',
            name: 'admin-profiles',
            component: ProfilesAdminView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },
        {
            path: '/admin/profiles/new',
            name: 'admin-profiles-new',
            component: ProfileFormView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },
        {
            path: '/admin/profiles/:id/edit',
            name: 'admin-profiles-edit',
            component: ProfileFormView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },


        // Rutas Admin Users - Fase 7+
        {
            path: '/admin/users',
            name: 'admin-users',
            component: UsersAdminView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },
        {
            path: '/admin/users/:id',
            name: 'admin-users-detail',
            component: UserDetailView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },
        {
            path: '/admin/reports',
            name: 'admin-reports',
            component: ReportsView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
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
        {
            path: '/configuracion-cuenta',
            name: 'configuracion-cuenta',
            component: AccountSettingsView,
            meta: { requiresAuth: true, hideNavbar: true }
        },

        // Rutas v2 - Admin Ofertas
        {
            path: '/admin/ofertas',
            name: 'admin-ofertas',
            component: OfertasAdminView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },
        {
            path: '/admin/ofertas/new',
            name: 'admin-ofertas-new',
            component: OfertaFormView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
        },
        {
            path: '/admin/ofertas/edit/:id',
            name: 'admin-ofertas-edit',
            component: OfertaFormView,
            meta: { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
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

export default router
