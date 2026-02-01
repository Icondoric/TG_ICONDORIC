<script setup>
/**
 * NavBar - Fase 7
 * Barra de navegacion actualizada con enlaces ML y Admin
 */

import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

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
    <nav class="landing-nav" :class="{ 'scrolled': isScrolled }">
        <div class="nav-container">
            <!-- Logo -->
            <div class="logo" @click="handleNavigation('/')" style="cursor: pointer;">
                <img src="@/assets/icons/logoEmi.png" alt="Logo EMI" class="emi-logo-img" />
            </div>

            <!-- Desktop Navigation -->
            <div class="nav-links">
                <!-- Links publicos -->
                <a @click.prevent="scrollToSection('features')">Caracteristicas</a>
                <a @click.prevent="scrollToSection('how-it-works')">Como funciona</a>
                <a @click.prevent="scrollToSection('about')">Acerca de</a>

                <!-- Links ML (visibles para todos) -->
                <a @click.prevent="handleNavigation('/evaluation')" class="nav-ml-link">Evaluar CV</a>
                <a @click.prevent="handleNavigation('/recommendations')" class="nav-ml-link">Recomendaciones</a>

                <!-- Usuario no autenticado -->
                <template v-if="!authStore.isAuthenticated">
                    <button @click="handleNavigation('/login')" class="btn-login">Iniciar Sesion</button>
                    <button @click="handleNavigation('/register')" class="btn-register">Registrarse</button>
                </template>

                <!-- Usuario autenticado -->
                <template v-else>
                    <div class="user-info">
                        <div class="auth-buttons">
                            <!-- Botones para estudiante/titulado -->
                            <template v-if="!authStore.isAdmin">
                                <button @click="handleNavigation('/mi-perfil')" class="btn-profile">Mi Perfil</button>
                                <button @click="handleNavigation('/mis-recomendaciones')" class="btn-recommendations">Recomendaciones</button>
                            </template>
                            <!-- Admin button -->
                            <button
                                v-if="authStore.isAdmin"
                                @click="handleNavigation('/admin')"
                                class="btn-admin"
                            >
                                Admin
                            </button>
                            <button @click="authStore.logout()" class="btn-logout">Salir</button>
                        </div>
                    </div>
                </template>
            </div>

            <!-- Mobile Menu Button -->
            <button @click="toggleMobileMenu" class="mobile-menu-btn">
                <svg v-if="!isMobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
                <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>

        <!-- Mobile Menu -->
        <div v-if="isMobileMenuOpen" class="mobile-menu">
            <a @click.prevent="scrollToSection('features')">Caracteristicas</a>
            <a @click.prevent="scrollToSection('how-it-works')">Como funciona</a>
            <a @click.prevent="scrollToSection('about')">Acerca de</a>
            <hr />
            <a @click.prevent="handleNavigation('/evaluation')">Evaluar CV</a>
            <a @click.prevent="handleNavigation('/recommendations')">Recomendaciones</a>

            <template v-if="!authStore.isAuthenticated">
                <hr />
                <a @click.prevent="handleNavigation('/login')">Iniciar Sesion</a>
                <a @click.prevent="handleNavigation('/register')">Registrarse</a>
            </template>
            <template v-else>
                <hr />
                <template v-if="!authStore.isAdmin">
                    <a @click.prevent="handleNavigation('/mi-perfil')">Mi Perfil</a>
                    <a @click.prevent="handleNavigation('/subir-cv')">Subir CV</a>
                    <a @click.prevent="handleNavigation('/mis-recomendaciones')">Mis Recomendaciones</a>
                </template>
                <a v-if="authStore.isAdmin" @click.prevent="handleNavigation('/admin')">Dashboard Admin</a>
                <a v-if="authStore.isAdmin" @click.prevent="handleNavigation('/admin/ofertas')">Ofertas</a>
                <a v-if="authStore.isAdmin" @click.prevent="handleNavigation('/admin/profiles')">Perfiles Inst.</a>
                <a @click.prevent="authStore.logout()" class="text-red-600">Cerrar Sesion</a>
            </template>
        </div>
    </nav>
</template>

<style scoped>
.landing-nav {
    position: fixed;
    width: 100%;
    top: 0;
    left: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    padding: 0.5rem 0;
    transition: box-shadow 0.3s ease;
}

.landing-nav.scrolled {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.nav-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
}

.emi-logo-img {
    height: 40px;
    width: auto;
}

.nav-links {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.nav-links a {
    text-decoration: none;
    color: #1f2937;
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 0.3s;
    cursor: pointer;
}

.nav-links a:hover {
    color: #2563eb;
}

.nav-ml-link {
    color: #2563eb !important;
    font-weight: 600 !important;
}

.btn-login {
    color: #1f2937;
    padding: 0.5rem 1rem;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 0.9rem;
}

.btn-login:hover {
    color: #2563eb;
}

.btn-register {
    background: #2563eb;
    color: white !important;
    padding: 0.5rem 1.2rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.9rem;
}

.btn-register:hover {
    background: #1e40af;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-dashboard {
    background: #10b981;
    color: white !important;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.85rem;
}

.btn-dashboard:hover {
    background: #059669;
    transform: translateY(-1px);
}

.btn-history {
    background: #6366f1;
    color: white !important;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.85rem;
}

.btn-history:hover {
    background: #4f46e5;
    transform: translateY(-1px);
}

.btn-admin {
    background: #f59e0b;
    color: white !important;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.85rem;
}

.btn-admin:hover {
    background: #d97706;
    transform: translateY(-1px);
}

.btn-profile {
    background: #8b5cf6;
    color: white !important;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.85rem;
}

.btn-profile:hover {
    background: #7c3aed;
    transform: translateY(-1px);
}

.btn-recommendations {
    background: #10b981;
    color: white !important;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.85rem;
}

.btn-recommendations:hover {
    background: #059669;
    transform: translateY(-1px);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.auth-buttons {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.btn-logout {
    color: #ef4444;
    padding: 0.5rem 0.8rem;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s;
    background: transparent;
    border: 1px solid #ef4444;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85rem;
}

.btn-logout:hover {
    background: #fef2f2;
}

/* Mobile Menu Button */
.mobile-menu-btn {
    display: none;
    padding: 0.5rem;
    background: transparent;
    border: none;
    cursor: pointer;
    color: #1f2937;
}

/* Mobile Menu */
.mobile-menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    flex-direction: column;
    gap: 0.75rem;
}

.mobile-menu a {
    padding: 0.75rem 1rem;
    color: #1f2937;
    text-decoration: none;
    font-weight: 500;
    border-radius: 8px;
    transition: background 0.2s;
}

.mobile-menu a:hover {
    background: #f1f5f9;
}

.mobile-menu hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 0.5rem 0;
}

/* Responsive */
@media (max-width: 1024px) {
    .nav-links {
        display: none;
    }

    .mobile-menu-btn {
        display: block;
    }

    .mobile-menu {
        display: flex;
    }
}

@media (min-width: 1025px) {
    .mobile-menu {
        display: none !important;
    }
}
</style>
