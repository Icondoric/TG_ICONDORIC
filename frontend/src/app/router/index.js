import { createRouter, createWebHistory } from 'vue-router'
import { setupGuards } from './guards'

// Import feature routes
import landingRoutes from '@/features/landing/landing.routes'
import authRoutes from '@/features/auth/auth.routes'
import dashboardRoutes from '@/features/dashboard/dashboard.routes'
import profileRoutes from '@/features/profile/profile.routes'
import evaluationRoutes from '@/features/evaluation/evaluation.routes'
import recommendationsRoutes from '@/features/recommendations/recommendations.routes'
import accountRoutes from '@/features/account/account.routes'
import adminRoutes from '@/features/admin/admin.routes'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        ...landingRoutes,
        ...authRoutes,
        ...dashboardRoutes,
        ...profileRoutes,
        ...evaluationRoutes,
        ...recommendationsRoutes,
        ...accountRoutes,
        ...adminRoutes,

        // Catch-all redirect
        {
            path: '/:pathMatch(.*)*',
            redirect: '/'
        }
    ]
})

setupGuards(router)

export default router
