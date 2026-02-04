<script setup>
/**
 * NavBar - Corregido
 * Barra de navegacion con identidad corporativa EMI (Azul Marino + Dorado)
 * - Usuarios NO autenticados: Landing + Evaluar CV + Login/Register
 * - Usuarios autenticados: Mi Perfil + Mis Recomendaciones
 */

import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

// Detectar si estamos en una pagina de dashboard (no landing)
const isDashboardPage = computed(() => {
    const dashboardRoutes = ['/mi-perfil', '/mis-recomendaciones', '/admin', '/subir-cv', '/dashboard']
    return dashboardRoutes.some(r => route.path.startsWith(r))
})

const handleNavigation = (path) => {
    router.push(path)
    isMobileMenuOpen.value = false
}

const scrollToSection = (id) => {
    if (route.path !== '/') {
        router.push('/')
        setTimeout(() => {
            const element = document.getElementById(id)
            if (element) element.scrollIntoView({ behavior: 'smooth' })
        }, 100)
    } else {
        const element = document.getElementById(id)
        if (element) element.scrollIntoView({ behavior: 'smooth' })
    }
    isMobileMenuOpen.value = false
}

const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
}

onMounted(() => {
    window.addEventListener('scroll', () => {
        isScrolled.value = window.scrollY > 50
    })
})
</script>

<template>
    <nav
        v-if="route.path === '/' || route.path === '/login' || route.path === '/register' || route.path === '/evaluation' || (!route.path.startsWith('/mi-perfil') && !route.path.startsWith('/mis-recomendaciones') && !route.path.startsWith('/admin'))"
        class="fixed w-full top-0 left-0 z-50 transition-all duration-300"
        :class="[
            isDashboardPage
                ? 'bg-emi-navy-500 shadow-lg'
                : isScrolled
                    ? 'bg-white/95 backdrop-blur-md shadow-md'
                    : 'bg-white/95 backdrop-blur-md shadow-sm'
        ]"
    >
        <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <div
                    @click="handleNavigation('/')"
                    class="flex items-center cursor-pointer"
                >
                    <img src="@/assets/icons/logoEmi.png" alt="Logo EMI" class="h-10 w-auto" />
                </div>

                <!-- Desktop Navigation -->
                <div class="hidden lg:flex items-center gap-6">
                    <!-- Links publicos y Estudiantes (Menu Común) -->
                    <template v-if="!authStore.isAdmin">
                        <!-- Link Inicio EXPLICITO -->
                        <a
                            @click.prevent="handleNavigation('/')"
                            class="text-gray-700 hover:text-emi-gold-500 font-medium text-sm cursor-pointer transition-colors"
                        >
                            Inicio
                        </a>

                        <a
                            @click.prevent="scrollToSection('features')"
                            class="text-gray-700 hover:text-emi-gold-500 font-medium text-sm cursor-pointer transition-colors"
                        >
                            Caracteristicas
                        </a>
                        <a
                            @click.prevent="scrollToSection('how-it-works')"
                            class="text-gray-700 hover:text-emi-gold-500 font-medium text-sm cursor-pointer transition-colors"
                        >
                            Como funciona
                        </a>
                        <a
                            @click.prevent="scrollToSection('about')"
                            class="text-gray-700 hover:text-emi-gold-500 font-medium text-sm cursor-pointer transition-colors"
                        >
                            Acerca de
                        </a>
                        <!-- Link Evaluar CV -->
                        <a
                            @click.prevent="handleNavigation('/evaluation')"
                            :class="[
                                'font-semibold text-sm cursor-pointer transition-colors',
                                isDashboardPage
                                    ? 'text-emi-gold-400 hover:text-emi-gold-300'
                                    : 'text-emi-navy-500 hover:text-emi-gold-500'
                            ]"
                        >
                            Evaluar CV
                        </a>
                    </template>

                    <!-- Usuario no autenticado -->
                    <template v-if="!authStore.isAuthenticated">
                        <button
                            @click="handleNavigation('/login')"
                            :class="[
                                'font-medium text-sm transition-colors',
                                isDashboardPage
                                    ? 'text-white hover:text-emi-gold-300'
                                    : 'text-gray-700 hover:text-emi-navy-500'
                            ]"
                        >
                            Iniciar Sesion
                        </button>
                        <button
                            @click="handleNavigation('/register')"
                            class="bg-emi-gold-500 text-emi-navy-800 px-4 py-2 rounded-lg font-medium text-sm hover:bg-emi-gold-400 transition-all hover:-translate-y-0.5 shadow-sm hover:shadow-md"
                        >
                            Registrarse
                        </button>
                    </template>

                    <!-- Usuario autenticado (estudiante/titulado) -->
                    <template v-else-if="!authStore.isAdmin">
                        <button
                            @click="handleNavigation('/mi-perfil')"
                            :class="[
                                'px-4 py-2 rounded-lg font-medium text-sm transition-all',
                                isDashboardPage && route.path.startsWith('/mi-perfil')
                                    ? 'bg-white text-emi-navy-500'
                                    : isDashboardPage
                                        ? 'bg-emi-navy-400 text-white hover:bg-emi-navy-300'
                                        : 'bg-emi-navy-500 text-white hover:bg-emi-navy-600'
                            ]"
                        >
                            Mi Perfil
                        </button>
                        <button
                            @click="authStore.logout()"
                            :class="[
                                'px-3 py-2 rounded-lg font-medium text-sm border transition-all',
                                isDashboardPage
                                    ? 'border-red-400 text-red-400 hover:bg-red-400/10'
                                    : 'border-red-500 text-red-500 hover:bg-red-50'
                            ]"
                        >
                            Cerrar Sesión
                        </button>
                    </template>

                    <!-- Usuario admin -->
                    <template v-else>
                        <!-- Link Inicio para Admin -->
                        <a
                            @click.prevent="handleNavigation('/')"
                            :class="[
                                'font-medium text-sm cursor-pointer transition-colors',
                                isDashboardPage
                                    ? 'text-white hover:text-emi-gold-300'
                                    : 'text-gray-700 hover:text-emi-gold-500'
                            ]"
                        >
                            Inicio
                        </a>

                        <button
                            @click="handleNavigation('/admin')"
                            :class="[
                                'px-4 py-2 rounded-lg font-medium text-sm transition-all',
                                isDashboardPage && route.path === '/admin'
                                    ? 'bg-white text-emi-gold-600'
                                    : 'bg-emi-gold-500 text-emi-navy-800 hover:bg-emi-gold-400'
                            ]"
                        >
                            Dashboard
                        </button>
                        <button
                            @click="handleNavigation('/admin/ofertas')"
                            :class="[
                                'px-4 py-2 rounded-lg font-medium text-sm transition-all',
                                isDashboardPage && route.path.startsWith('/admin/ofertas')
                                    ? 'bg-white text-emi-navy-500'
                                    : isDashboardPage
                                        ? 'bg-emi-navy-400 text-white hover:bg-emi-navy-300'
                                        : 'bg-emi-navy-500 text-white hover:bg-emi-navy-600'
                            ]"
                        >
                            Ofertas
                        </button>
                        <button
                            @click="handleNavigation('/admin/profiles')"
                            :class="[
                                'px-4 py-2 rounded-lg font-medium text-sm transition-all',
                                isDashboardPage && route.path.startsWith('/admin/profiles')
                                    ? 'bg-white text-emi-navy-500'
                                    : isDashboardPage
                                        ? 'bg-emi-navy-400 text-white hover:bg-emi-navy-300'
                                        : 'bg-emi-navy-500 text-white hover:bg-emi-navy-600'
                            ]"
                        >
                            Perfiles
                        </button>
                        <button
                            @click="authStore.logout()"
                            :class="[
                                'px-3 py-2 rounded-lg font-medium text-sm border transition-all',
                                isDashboardPage
                                    ? 'border-red-400 text-red-400 hover:bg-red-400/10'
                                    : 'border-red-500 text-red-500 hover:bg-red-50'
                            ]"
                        >
                            Salir
                        </button>
                    </template>
                </div>

                <!-- Mobile Menu Button -->
                <button
                    @click="toggleMobileMenu"
                    class="lg:hidden p-2 rounded-lg transition-colors"
                    :class="isDashboardPage ? 'text-white hover:bg-emi-navy-400' : 'text-gray-700 hover:bg-gray-100'"
                >
                    <svg v-if="!isMobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                    <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div
            v-if="isMobileMenuOpen"
            class="lg:hidden absolute top-full left-0 right-0 bg-white shadow-lg border-t border-gray-100"
        >
            <div class="px-4 py-4 space-y-2">
                <!-- Links publicos (solo NO autenticado) -->
                <template v-if="!authStore.isAuthenticated">
                    <a
                        @click.prevent="scrollToSection('features')"
                        class="block px-4 py-3 text-gray-700 hover:bg-emi-navy-50 hover:text-emi-navy-500 rounded-lg font-medium cursor-pointer transition-colors"
                    >
                        Caracteristicas
                    </a>
                    <a
                        @click.prevent="scrollToSection('how-it-works')"
                        class="block px-4 py-3 text-gray-700 hover:bg-emi-navy-50 hover:text-emi-navy-500 rounded-lg font-medium cursor-pointer transition-colors"
                    >
                        Como funciona
                    </a>
                    <a
                        @click.prevent="scrollToSection('about')"
                        class="block px-4 py-3 text-gray-700 hover:bg-emi-navy-50 hover:text-emi-navy-500 rounded-lg font-medium cursor-pointer transition-colors"
                    >
                        Acerca de
                    </a>

                    <hr class="border-gray-200 my-2" />

                    <a
                        @click.prevent="handleNavigation('/evaluation')"
                        class="block px-4 py-3 text-emi-navy-500 hover:bg-emi-gold-50 hover:text-emi-gold-600 rounded-lg font-semibold cursor-pointer transition-colors"
                    >
                        Evaluar CV
                    </a>

                    <hr class="border-gray-200 my-2" />

                    <a
                        @click.prevent="handleNavigation('/login')"
                        class="block px-4 py-3 text-gray-700 hover:bg-gray-100 rounded-lg font-medium cursor-pointer transition-colors"
                    >
                        Iniciar Sesion
                    </a>
                    <a
                        @click.prevent="handleNavigation('/register')"
                        class="block px-4 py-3 bg-emi-gold-500 text-emi-navy-800 hover:bg-emi-gold-400 rounded-lg font-medium text-center cursor-pointer transition-colors"
                    >
                        Registrarse
                    </a>
                </template>

                <!-- Menu para usuario autenticado (estudiante/titulado) -->
                <template v-else-if="!authStore.isAdmin">
                    <a
                        @click.prevent="handleNavigation('/mi-perfil')"
                        :class="[
                            'block px-4 py-3 rounded-lg font-medium cursor-pointer transition-colors',
                            route.path.startsWith('/mi-perfil')
                                ? 'bg-emi-navy-500 text-white'
                                : 'text-gray-700 hover:bg-emi-navy-50 hover:text-emi-navy-500'
                        ]"
                    >
                        Mi Perfil
                    </a>
                    <a
                        @click.prevent="handleNavigation('/mis-recomendaciones')"
                        :class="[
                            'block px-4 py-3 rounded-lg font-medium cursor-pointer transition-colors',
                            route.path.startsWith('/mis-recomendaciones')
                                ? 'bg-emi-gold-500 text-emi-navy-800'
                                : 'text-gray-700 hover:bg-emi-gold-50 hover:text-emi-gold-600'
                        ]"
                    >
                        Mis Recomendaciones
                    </a>

                    <hr class="border-gray-200 my-2" />

                    <a
                        @click.prevent="authStore.logout()"
                        class="block px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg font-medium cursor-pointer transition-colors"
                    >
                        Cerrar Sesion
                    </a>
                </template>

                <!-- Menu para admin -->
                <template v-else>
                    <a
                        @click.prevent="handleNavigation('/admin')"
                        :class="[
                            'block px-4 py-3 rounded-lg font-medium cursor-pointer transition-colors',
                            route.path === '/admin'
                                ? 'bg-emi-gold-500 text-emi-navy-800'
                                : 'text-emi-gold-600 hover:bg-emi-gold-50'
                        ]"
                    >
                        Dashboard Admin
                    </a>
                    <a
                        @click.prevent="handleNavigation('/admin/ofertas')"
                        :class="[
                            'block px-4 py-3 rounded-lg font-medium cursor-pointer transition-colors',
                            route.path.startsWith('/admin/ofertas')
                                ? 'bg-emi-navy-500 text-white'
                                : 'text-gray-700 hover:bg-gray-100'
                        ]"
                    >
                        Ofertas
                    </a>
                    <a
                        @click.prevent="handleNavigation('/admin/profiles')"
                        :class="[
                            'block px-4 py-3 rounded-lg font-medium cursor-pointer transition-colors',
                            route.path.startsWith('/admin/profiles')
                                ? 'bg-emi-navy-500 text-white'
                                : 'text-gray-700 hover:bg-gray-100'
                        ]"
                    >
                        Perfiles Institucionales
                    </a>

                    <hr class="border-gray-200 my-2" />

                    <a
                        @click.prevent="authStore.logout()"
                        class="block px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg font-medium cursor-pointer transition-colors"
                    >
                        Cerrar Sesion
                    </a>
                </template>
            </div>
        </div>
    </nav>
</template>
