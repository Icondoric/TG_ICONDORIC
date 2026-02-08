const LoginView = () => import('@/features/auth/views/LoginView.vue')
const RegisterView = () => import('@/features/auth/views/RegisterView.vue')

export default [
    {
        path: '/login',
        name: 'login',
        component: LoginView
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterView
    }
]
