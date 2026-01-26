<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isScrolled = ref(false)

const handleNavigation = (path) => {
    router.push(path)
}

const scrollToSection = (id) => {
    if (route.path !== '/') {
        router.push('/')
        // Wait for navigation then scroll (simple approach)
        setTimeout(() => {
            const element = document.getElementById(id)
            if (element) element.scrollIntoView({ behavior: 'smooth' })
        }, 100)
    } else {
        const element = document.getElementById(id)
        if (element) element.scrollIntoView({ behavior: 'smooth' })
    }
}

// Scroll effect logic
onMounted(() => {
    window.addEventListener('scroll', () => {
        isScrolled.value = window.scrollY > 50
    })
})
</script>

<template>
    <nav class="landing-nav" :class="{ 'scrolled': isScrolled }">
        <div class="nav-container">
            <!-- Logo with redirect to Home -->
            <div class="logo" @click="handleNavigation('/')" style="cursor: pointer;">
                <img src="@/assets/icons/logoEmi.png" alt="Logo EMI" class="emi-logo-img" />
            </div>
            
            <div class="nav-links">
                <a @click.prevent="scrollToSection('features')">Características</a>
                <a @click.prevent="scrollToSection('how-it-works')">¿Cómo funciona?</a>
                <a @click.prevent="scrollToSection('about')">Acerca de</a>
                
                <template v-if="!authStore.isAuthenticated">
                    <button @click="handleNavigation('/login')" class="btn-login">Iniciar Sesión</button>
                    <button @click="handleNavigation('/register')" class="btn-register">Registrarse</button>
                </template>
                <template v-else>
                    <div class="user-info">
                        <!-- Nombre removido por solicitud del usuario -->
                        <div class="auth-buttons">
                            <button @click="handleNavigation('/dashboard')" class="btn-dashboard">Mi Panel</button>
                            <button @click="authStore.logout()" class="btn-logout">Cerrar Sesión</button>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </nav>
</template>

<style scoped>
/* Copied and adapted from landing.css */
.landing-nav {
    position: fixed;
    width: 100%;
    top: 0;
    left: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    padding: 0.5rem 0; /* Reduced padding slightly */
    transition: box-shadow 0.3s ease;
}

.landing-nav.scrolled {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.nav-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 0 4rem; /* Increased padding for aesthetics on large screens */
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
}

.emi-logo-img {
    height: 40px; /* Adjust as needed */
    width: auto;
    /* object-fit: contain; handled by auto width */
}

.nav-links {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-links a {
    text-decoration: none;
    color: #1f2937; /* var(--text-dark) */
    font-weight: 500;
    transition: color 0.3s;
    cursor: pointer;
}

.nav-links a:hover {
    color: #2563eb; /* var(--primary) */
}

/* Button styles repeated here or we rely on global css. 
   Ideally these should be unique or properly scoped. */
.btn-login {
    color: #1f2937;
    padding: 0.6rem 1.2rem;
    text-decoration: none;
    font-weight: 500;
    margin-right: 0.5rem;
    transition: color 0.3s;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}

.btn-login:hover {
    color: #2563eb;
}

.btn-register {
    background: #2563eb;
    color: white !important;
    padding: 0.6rem 1.5rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 1rem;
}

.btn-register:hover {
    background: #1e40af;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-dashboard {
    background: #10b981;
    color: white !important;
    padding: 0.6rem 1.5rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-weight: 500;
    font-size: 1rem;
}

.btn-dashboard:hover {
    background: #059669;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

@media (max-width: 768px) {
    .nav-links {
        display: none; /* Mobile menu needed eventually, but keeping simple for now */
    }
}

/* User Info Styles */
.user-info {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.user-name {
    color: #1f2937;
    font-weight: 600;
    font-size: 0.95rem;
}

.auth-buttons {
    display: flex;
    gap: 0.8rem;
    align-items: center;
}

.btn-logout {
    color: #ef4444; /* Red color */
    padding: 0.6rem 1rem;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s;
    background: transparent;
    border: 1px solid #ef4444;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
}

.btn-logout:hover {
    background: #fef2f2;
    transform: translateY(-1px);
}
</style>
