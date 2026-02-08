const EvaluationView = () => import('@/features/evaluation/views/EvaluationView.vue')
const HistoryView = () => import('@/features/evaluation/views/HistoryView.vue')

export default [
    {
        path: '/evaluation',
        name: 'evaluation',
        component: EvaluationView,
        meta: { requiresAuth: false }
    },
    {
        path: '/history',
        name: 'history',
        component: HistoryView,
        meta: { requiresAuth: true }
    }
]
