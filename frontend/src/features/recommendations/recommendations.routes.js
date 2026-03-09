const MisRecomendacionesView = () => import('@/features/recommendations/views/MisRecomendacionesView.vue')
const HistorialPostulacionesView = () => import('@/features/recommendations/views/HistorialPostulacionesView.vue')

export default [
    {
        path: '/mis-recomendaciones',
        name: 'mis-recomendaciones',
        component: MisRecomendacionesView,
        meta: { requiresAuth: true, moduleId: 'evaluacion_perfiles', submoduleId: 'correspondencia' }
    },
    {
        path: '/correspondencia-perfiles',
        redirect: '/mis-recomendaciones'
    },
    {
        path: '/historial-postulaciones',
        name: 'historial-postulaciones',
        component: HistorialPostulacionesView,
        meta: { requiresAuth: true, hideNavbar: true, moduleId: 'evaluacion_perfiles', submoduleId: 'historial' }
    },
    {
        path: '/recommendations',
        redirect: '/mis-recomendaciones'
    }
]
