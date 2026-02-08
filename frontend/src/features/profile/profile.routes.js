const MiPerfilView = () => import('@/features/profile/views/MiPerfilView.vue')
const SubirCVView = () => import('@/features/profile/views/SubirCVView.vue')

export default [
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
    }
]
