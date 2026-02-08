const DashboardView = () => import('@/features/dashboard/views/DashboardView.vue')

export default [
    {
        path: '/dashboard',
        name: 'dashboard',
        component: DashboardView,
        meta: { requiresAuth: true }
    }
]
