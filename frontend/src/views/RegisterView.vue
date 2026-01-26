<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import '../assets/css/auth.css'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const role = ref('estudiante') // 'estudiante' | 'titulado'

const error = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const passwordStrength = ref('') // 'weak', 'medium', 'strong'

const authStore = useAuthStore()
const router = useRouter()

// Password Strength Logic
const checkPasswordStrength = () => {
    if (password.value.length < 6) {
        passwordStrength.value = 'weak'
    } else if (password.value.length < 10) {
        passwordStrength.value = 'medium'
    } else {
        passwordStrength.value = 'strong'
    }
}

// Navigation
const goToLogin = () => {
    router.push('/login')
}

const handleRegister = async () => {
    error.value = ''
    successMessage.value = ''
    
    // Validations
    if (password.value.length < 8) {
        error.value = '❌ La contraseña debe tener al menos 8 caracteres'
        return
    }
    
    if (password.value !== confirmPassword.value) {
        error.value = '❌ Las contraseñas no coinciden'
        return
    }
    
    // Validation removed requested by user context (or just not enforced strictly)
    if (!email.value.endsWith('@est.emi.edu.bo') && !email.value.endsWith('@emi.edu.bo')) {
         // Just a warning in console or UI, but allowing proceed if user insists 
         // For now let's keep it but maybe less strict? 
         // User didn't allow removal of email validation, so keeping same as previous logic
         error.value = '⚠️ Se recomienda usar tu correo institucional EMI (ej: @est.emi.edu.bo)'
         return 
    }

    isLoading.value = true
    
    try {
        // Updated to pass name (nombre_completo)
        await authStore.register(email.value, password.value, role.value, name.value)
        successMessage.value = '✓ Cuenta creada exitosamente. Redirigiendo...'
        setTimeout(() => {
            router.push('/login')
        }, 1500)
    } catch (e) {
        error.value = `❌ ${e}`
    } finally {
        isLoading.value = false
    }
}
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
            <button class="tab" @click="goToLogin">Iniciar Sesión</button>
            <button class="tab active">Registrarse</button>
        </div>

        <!-- Register Form -->
        <form @submit.prevent="handleRegister" class="form-section">
            <div class="form-group">
                <label>Tipo de Usuario</label>
                <div class="role-selector">
                    <label class="role-option" :class="{ selected: role === 'estudiante' }" @click="role = 'estudiante'">
                        <input type="radio" value="estudiante" v-model="role">
                        <div class="role-icon">👨🎓</div>
                        <div class="role-label">Estudiante</div>
                    </label>
                    <label class="role-option" :class="{ selected: role === 'titulado' }" @click="role = 'titulado'">
                        <input type="radio" value="titulado" v-model="role">
                        <div class="role-icon">🎓</div>
                        <div class="role-label">Titulado</div>
                    </label>
                </div>
            </div>

            <div class="form-group">
                <label for="registerName">Nombre Completo</label>
                <input 
                    type="text" 
                    id="registerName" 
                    v-model="name"
                    placeholder="Juan Pérez Gómez"
                    required
                >
            </div>

            <div class="form-group">
                <label for="registerEmail">Correo Electrónico</label>
                <input 
                    type="email" 
                    id="registerEmail" 
                    v-model="email"
                    placeholder="juan.perez@est.emi.edu.bo"
                    required
                >
            </div>

            <!-- Removed CI and Carrera fields as requested -->

            <div class="form-group">
                <label for="registerPassword">Contraseña</label>
                <input 
                    type="password" 
                    id="registerPassword" 
                    v-model="password"
                    @input="checkPasswordStrength"
                    placeholder="Mínimo 8 caracteres"
                    required
                >
                <div class="password-strength">
                    <div class="password-strength-bar" :class="passwordStrength"></div>
                </div>
            </div>

            <div class="form-group">
                <label for="registerConfirmPassword">Confirmar Contraseña</label>
                <input 
                    type="password" 
                    id="registerConfirmPassword" 
                    v-model="confirmPassword"
                    placeholder="Repite tu contraseña"
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
                {{ isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}
            </button>
        </form>

        <!-- Administrative Access -->
        <button class="btn-secondary" @click="alert('Esta funcionalidad estará disponible pronto')">
            🔐 Acceso Administrativo
        </button>

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
