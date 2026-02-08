const MisRecomendacionesView = () => import('@/features/recommendations/views/MisRecomendacionesView.vue')

export default [
    {
        path: '/mis-recomendaciones',
        name: 'mis-recomendaciones',
        component: MisRecomendacionesView,
        meta: { requiresAuth: true }
    },
    {
        path: '/recommendations',
        redirect: '/mis-recomendaciones'
    }
]
