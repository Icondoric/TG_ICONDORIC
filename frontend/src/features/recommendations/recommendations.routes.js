const MisRecomendacionesView = () => import('@/features/recommendations/views/MisRecomendacionesView.vue')
const PostulacionesView = () => import('@/features/recommendations/views/PostulacionesView.vue')
const HistorialPostulacionesView = () => import('@/features/recommendations/views/HistorialPostulacionesView.vue')

export default [
    {
        path: '/mis-recomendaciones',
        name: 'mis-recomendaciones',
        component: MisRecomendacionesView,
        meta: { requiresAuth: true }
    },
    {
        path: '/correspondencia-perfiles',
        name: 'correspondencia-perfiles',
        component: PostulacionesView,
        meta: { requiresAuth: true, hideNavbar: true }
    },
    {
        path: '/historial-postulaciones',
        name: 'historial-postulaciones',
        component: HistorialPostulacionesView,
        meta: { requiresAuth: true, hideNavbar: true }
    },
    {
        path: '/recommendations',
        redirect: '/mis-recomendaciones'
    }
]
