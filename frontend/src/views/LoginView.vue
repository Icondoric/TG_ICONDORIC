<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import '../assets/css/auth.css'

const email = ref('')
const password = ref('')
const captchaInput = ref('')
const captchaText = ref('')
const error = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const authStore = useAuthStore()
const router = useRouter()

// Captcha Logic
const generateCaptcha = () => {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    let captcha = ''
    for (let i = 0; i < 4; i++) {
        captcha += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    captchaText.value = captcha
}

const refreshCaptcha = () => {
    generateCaptcha()
    captchaInput.value = ''
}

// Navigation
const goToRegister = () => {
    router.push('/register')
}

const handleLogin = async () => {
    error.value = ''
    successMessage.value = ''
    
    // Validate Captcha
    if (captchaInput.value.toUpperCase() !== captchaText.value) {
        error.value = '❌ Código de seguridad incorrecto'
        refreshCaptcha()
        return
    }

    isLoading.value = true
    
    try {
        await authStore.login(email.value, password.value)
        successMessage.value = '✓ Iniciando sesión...'
        setTimeout(() => {
            router.push('/')
        }, 800)
    } catch (e) {
        error.value = `❌ ${e}`
        refreshCaptcha() // Refresh captcha on failed attempt
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    generateCaptcha()
})
</script>

<template>
<div class="auth-wrapper">
    <!-- Watermark Background -->
    <div class="watermark">EMI</div>
    
    <!-- Decorative Castles -->
    <div class="castle-decoration castle-left">🏰</div>
    <div class="castle-decoration castle-right">🏰</div>

    <!-- Main Login Container -->
    <div class="login-container">
        <!-- Header -->
        <div class="login-header">
            <div class="emi-logo">🎓</div>
            <h1 class="system-title">Estudiantes EMI</h1>
            <p class="system-subtitle">Sistema de Vinculación Laboral</p>
        </div>

        <!-- Tabs -->
        <div class="tabs">
            <button class="tab active">Iniciar Sesión</button>
            <button class="tab" @click="goToRegister">Registrarse</button>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="form-section">
            <div class="form-group">
                <!-- Changed label from 'Code SAGA' to 'Correo Electrónico' as requested -->
                <label for="loginEmail">Correo Electrónico</label>
                <input 
                    type="email" 
                    id="loginEmail" 
                    v-model="email"
                    placeholder="Ingresa tu correo institucional"
                    required
                >
            </div>

            <div class="form-group">
                <label for="loginPassword">Contraseña</label>
                <input 
                    type="password" 
                    id="loginPassword" 
                    v-model="password"
                    placeholder="Ingresa tu contraseña"
                    required
                >
            </div>

            <div class="form-group">
                <label for="loginCaptcha">Código de seguridad</label>
                <div class="captcha-container">
                    <div class="captcha-display">
                        <span class="captcha-text">{{ captchaText }}</span>
                    </div>
                    <button type="button" class="captcha-refresh" @click="refreshCaptcha" title="Generar nuevo código">
                        🔄
                    </button>
                </div>
                <input 
                    type="text" 
                    id="loginCaptcha" 
                    v-model="captchaInput"
                    placeholder="Ingresa el código de seguridad"
                    style="margin-top: 0.5rem;"
                    required
                >
            </div>

            <div v-if="error" class="validation-message error active">
                {{ error }}
            </div>
            
            <div v-if="successMessage" class="validation-message success active">
                {{ successMessage }}
            </div>

            <button type="submit" class="btn-primary" :disabled="isLoading">
                {{ isLoading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
            </button>

            <div class="help-links">
                <a href="#" @click.prevent="alert('Contacta al administrador del sistema')">¿Olvidaste tu contraseña?</a>
            </div>
        </form>

        <!-- Footer -->
        <div class="login-footer">
            <div class="institutional-motto">
                "Mcal. Antonio José de Sucre"<br>
                <strong>Prestigio, Disciplina y Oportunidades</strong>
            </div>
            <p style="margin-top: 1rem;">© 2026 DNTIC - Escuela Militar de Ingeniería</p>
        </div>
    </div>
</div>
</template>
