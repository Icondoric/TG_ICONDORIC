const RolesView = () => import('@/features/system/views/RolesView.vue')
const RoleFormView = () => import('@/features/system/views/RoleFormView.vue')

const systemMeta = { requiresAuth: true, requiresAdminOnly: true, hideNavbar: true }

export default [
    {
        path: '/admin/system/roles',
        name: 'system-roles',
        component: RolesView,
        meta: systemMeta
    },
    {
        path: '/admin/system/roles/new',
        name: 'system-roles-new',
        component: RoleFormView,
        meta: systemMeta
    },
    {
        path: '/admin/system/roles/:id/edit',
        name: 'system-roles-edit',
        component: RoleFormView,
        meta: systemMeta
    },
]
