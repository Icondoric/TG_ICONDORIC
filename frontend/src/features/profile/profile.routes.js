const SubirCVView = () => import('@/features/profile/views/SubirCVView.vue')
const MiPerfilView = () => import('@/features/profile/views/MiPerfilView.vue')
const EditarPerfilView = () => import('@/features/profile/views/EditarPerfilView.vue')
const BuscarPerfilesView = () => import('@/features/profile/views/BuscarPerfilesView.vue')

export default [
    {
        path: '/digitalizacion/subir-cv',
        name: 'subir-cv',
        component: SubirCVView,
        meta: { requiresAuth: true, moduleId: 'digitalizacion_perfiles', submoduleId: 'subir_cv' }
    },
    {
        path: '/digitalizacion/mi-perfil',
        name: 'mi-perfil',
        component: MiPerfilView,
        meta: { requiresAuth: true, moduleId: 'digitalizacion_perfiles', submoduleId: 'mi_perfil' }
    },
    {
        path: '/digitalizacion/editar',
        name: 'editar-perfil',
        component: EditarPerfilView,
        meta: { requiresAuth: true, moduleId: 'digitalizacion_perfiles', submoduleId: 'editar_perfil' }
    },
    {
        path: '/digitalizacion/buscar-perfiles',
        name: 'buscar-perfiles',
        component: BuscarPerfilesView,
        meta: { requiresAuth: true, requiresAdmin: true, moduleId: 'digitalizacion_perfiles', submoduleId: 'buscar_perfiles' }
    },
    // Redirects for old routes
    {
        path: '/mi-perfil',
        redirect: '/digitalizacion/mi-perfil'
    },
    {
        path: '/subir-cv',
        redirect: '/digitalizacion/subir-cv'
    }
]
