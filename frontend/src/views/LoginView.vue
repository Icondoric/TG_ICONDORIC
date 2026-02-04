<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

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

    try {
        isLoading.value = true
        error.value = ''
        
        await authStore.login(email.value, password.value)
        
        // Redireccionar segun el rol
        if (authStore.isAdmin) {
            router.push('/admin')
        } else {
            router.push('/mi-perfil')
        }
    } catch (e) {
        console.error('Login error:', e)
        error.value = 'Credenciales inválidas o error en el servidor'
        
        // Reset captcha on error
        refreshCaptcha()
        captchaInput.value = ''
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    generateCaptcha()
})
</script>

<template>
<div class="relative min-h-screen w-full flex items-center justify-center overflow-hidden py-6 pt-20">
    <!-- Background Image with Better Visibility (40% smaller) -->
    <div class="absolute inset-0 z-0 flex items-center justify-center">
        <img 
            src="../assets/images/backgroundEMI.png" 
            alt="EMI Background" 
            class="w-3/5 h-3/5 object-contain opacity-20"
        />
    </div>

    <!-- Lighter Gradient Overlay -->
    <div class="absolute inset-0 z-0 bg-gradient-to-br from-gray-50/70 via-gray-50/50 to-blue-50/70"></div>

    <!-- Main Login Container with Glassmorphism -->
    <div class="relative z-10 w-full max-w-md mx-4">
        <div class="backdrop-blur-lg bg-white/70 rounded-2xl shadow-2xl border border-white/60 p-6 transition-all duration-300">
            <!-- Header -->
            <div class="text-center mb-5">
                <img src="../assets/icons/logoEmi.png" alt="EMI Logo" class="w-16 h-16 mx-auto mb-3 object-contain" />
            </div>

            <!-- Title -->
            <h2 class="text-xl font-bold text-emi-navy-700 text-center mb-4">Iniciar Sesión</h2>

            <!-- Login Form -->
            <form @submit.prevent="handleLogin" class="space-y-3.5">
                <!-- Email Input -->
                <div>
                    <label for="loginEmail" class="block text-sm font-medium text-gray-700 mb-1.5">
                        Correo Electrónico
                    </label>
                    <input 
                        type="email" 
                        id="loginEmail" 
                        v-model="email"
                        placeholder="correo@est.emi.edu.bo"
                        required
                        class="w-full px-3 py-2.5 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg focus:outline-none focus:border-emi-navy-500 focus:ring-2 focus:ring-emi-navy-500/10 transition-all text-gray-800 placeholder-gray-400"
                    />
                </div>

                <!-- Password Input -->
                <div>
                    <label for="loginPassword" class="block text-sm font-medium text-gray-700 mb-1.5">
                        Contraseña
                    </label>
                    <input 
                        type="password" 
                        id="loginPassword" 
                        v-model="password"
                        placeholder="Ingresa tu contraseña"
                        required
                        class="w-full px-3 py-2.5 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg focus:outline-none focus:border-emi-navy-500 focus:ring-2 focus:ring-emi-navy-500/10 transition-all text-gray-800 placeholder-gray-400"
                    />
                </div>

                <!-- Captcha -->
                <div>
                    <label for="loginCaptcha" class="block text-sm font-medium text-gray-700 mb-1.5">
                        Código de seguridad
                    </label>
                    <div class="flex gap-2 mb-2">
                        <div class="flex-1 bg-gradient-to-br from-emi-gold-100 to-emi-gold-200 rounded-lg p-3 border-2 border-dashed border-emi-gold-400 relative overflow-hidden">
                            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                            <span class="relative z-10 text-xl font-bold text-emi-gold-800 tracking-widest font-mono select-none">
                                {{ captchaText }}
                            </span>
                        </div>
                        <button 
                            type="button" 
                            @click="refreshCaptcha" 
                            title="Generar nuevo código"
                            class="px-3 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg hover:border-emi-navy-500 hover:bg-white transition-all text-lg"
                        >
                            🔄
                        </button>
                    </div>
                    <input 
                        type="text" 
                        id="loginCaptcha" 
                        v-model="captchaInput"
                        placeholder="Ingresa el código"
                        required
                        class="w-full px-3 py-2.5 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg focus:outline-none focus:border-emi-navy-500 focus:ring-2 focus:ring-emi-navy-500/10 transition-all text-gray-800 placeholder-gray-400"
                    />
                </div>

                <!-- Error/Success Messages -->
                <div v-if="error" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-2.5 rounded-lg text-sm">
                    {{ error }}
                </div>
                
                <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 text-green-700 p-2.5 rounded-lg text-sm">
                    {{ successMessage }}
                </div>

                <!-- Submit Button -->
                <button 
                    type="submit" 
                    :disabled="isLoading"
                    class="w-full py-3 bg-gradient-to-r from-emi-navy-500 to-emi-navy-700 text-white font-semibold rounded-lg shadow-lg shadow-emi-navy-500/30 hover:shadow-xl hover:shadow-emi-navy-500/40 hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                    {{ isLoading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
                </button>

                <!-- Help Links -->
                <div class="text-center pt-3 border-t border-gray-200">
                    <a 
                        href="#" 
                        @click.prevent="alert('Contacta al administrador del sistema')"
                        class="text-sm text-emi-navy-600 hover:text-emi-navy-800 hover:underline transition-colors"
                    >
                        ¿Olvidaste tu contraseña?
                    </a>
                </div>
            </form>

            <!-- Footer -->
            <div class="text-center mt-4 pt-4 border-t border-gray-200">
                <div class="text-xs text-gray-500 italic mb-1.5">
                    "Mcal. Antonio José de Sucre"<br>
                    <strong class="text-emi-gold-600">Prestigio, Disciplina y Oportunidades</strong>
                </div>
                <p class="text-xs text-gray-400">© 2026 DNTIC - Escuela Militar de Ingeniería</p>
            </div>
        </div>
    </div>
</div>
</template>
