<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useUiStore } from '../../stores/ui'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()

const isActive = (path) => route.path === path || route.path.startsWith(path + '/')

const menuItems = [
    {
        label: 'Gestión de Usuarios',
        path: '/admin/users',
        icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
    },
    {
        label: 'Gestión de Oferta Institución',
        path: '/admin/ofertas',
        icon: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    },
    {
        label: 'Evaluación de Correspondencia (ML)',
        path: '/admin',
        icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    },
    {
        label: 'Informes y Reportes',
        path: '/admin/reports',
        icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    }
]

const handleLogout = () => {
    authStore.logout()
    router.push('/login')
}
</script>

<template>
    <aside 
        class="hidden lg:flex flex-col fixed inset-y-0 left-0 bg-emi-navy-900 text-white transition-all duration-300 transform z-50 shadow-lg"
        :class="uiStore.isSidebarOpen ? 'w-64' : 'w-20'"
    >
        <!-- Header -->
        <div class="flex items-center justify-between h-16 border-b border-emi-navy-700 bg-emi-navy-800 px-4">
            <h1 v-if="uiStore.isSidebarOpen" class="text-xl font-bold tracking-wider uppercase truncate">Admin</h1>
            <button @click="uiStore.toggleSidebar" class="text-white hover:text-gray-300 focus:outline-none ml-auto">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>
        </div>

        <!-- Menu Items -->
        <div class="flex-1 overflow-y-auto py-4">
            <nav class="space-y-1 px-2">
                <router-link
                    v-for="item in menuItems"
                    :key="item.path"
                    :to="item.path"
                    :title="!uiStore.isSidebarOpen ? item.label : ''"
                    :class="[
                        'group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors duration-150',
                        isActive(item.path) 
                            ? 'bg-emi-navy-700 text-white' 
                            : 'text-gray-300 hover:bg-emi-navy-700 hover:text-white',
                        !uiStore.isSidebarOpen ? 'justify-center' : ''
                    ]"
                >
                    <svg 
                        class="h-6 w-6 flex-shrink-0" 
                        :class="[
                            isActive(item.path) ? 'text-white' : 'text-gray-400 group-hover:text-white',
                            uiStore.isSidebarOpen ? 'mr-3' : ''
                        ]"
                        fill="none" 
                        stroke="currentColor" 
                        viewBox="0 0 24 24"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                    </svg>
                    <span v-if="uiStore.isSidebarOpen" class="truncate">{{ item.label }}</span>
                </router-link>
            </nav>
        </div>

        <!-- Footer / Logout -->
        <div class="p-4 border-t border-emi-navy-700 bg-emi-navy-800">
            <button 
                @click="handleLogout"
                class="w-full flex items-center px-3 py-2 text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 transition-colors duration-150 shadow-sm"
                :class="!uiStore.isSidebarOpen ? 'justify-center' : ''"
                :title="!uiStore.isSidebarOpen ? 'Cerrar Sesión' : ''"
            >
                <svg class="h-5 w-5" :class="uiStore.isSidebarOpen ? 'mr-2' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span v-if="uiStore.isSidebarOpen">Cerrar Sesión</span>
            </button>
        </div>
    </aside>
</template>
