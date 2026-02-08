const AdminDashboardView = () => import('@/features/admin/views/AdminDashboardView.vue')
const ProfilesAdminView = () => import('@/features/admin/views/ProfilesAdminView.vue')
const ProfileFormView = () => import('@/features/admin/views/ProfileFormView.vue')
const UsersAdminView = () => import('@/features/admin/views/UsersAdminView.vue')
const UserDetailView = () => import('@/features/admin/views/UserDetailView.vue')
const ReportsView = () => import('@/features/admin/views/ReportsView.vue')
const OfertasAdminView = () => import('@/features/admin/views/OfertasAdminView.vue')
const OfertaFormView = () => import('@/features/admin/views/OfertaFormView.vue')

const adminMeta = { requiresAuth: true, requiresAdmin: true, hideNavbar: true }

export default [
    {
        path: '/admin',
        name: 'admin',
        component: AdminDashboardView,
        meta: adminMeta
    },
    {
        path: '/admin/profiles',
        name: 'admin-profiles',
        component: ProfilesAdminView,
        meta: adminMeta
    },
    {
        path: '/admin/profiles/new',
        name: 'admin-profiles-new',
        component: ProfileFormView,
        meta: adminMeta
    },
    {
        path: '/admin/profiles/:id/edit',
        name: 'admin-profiles-edit',
        component: ProfileFormView,
        meta: adminMeta
    },
    {
        path: '/admin/users',
        name: 'admin-users',
        component: UsersAdminView,
        meta: adminMeta
    },
    {
        path: '/admin/users/:id',
        name: 'admin-users-detail',
        component: UserDetailView,
        meta: adminMeta
    },
    {
        path: '/admin/reports',
        name: 'admin-reports',
        component: ReportsView,
        meta: adminMeta
    },
    {
        path: '/admin/ofertas',
        name: 'admin-ofertas',
        component: OfertasAdminView,
        meta: adminMeta
    },
    {
        path: '/admin/ofertas/new',
        name: 'admin-ofertas-new',
        component: OfertaFormView,
        meta: adminMeta
    },
    {
        path: '/admin/ofertas/edit/:id',
        name: 'admin-ofertas-edit',
        component: OfertaFormView,
        meta: adminMeta
    }
]
