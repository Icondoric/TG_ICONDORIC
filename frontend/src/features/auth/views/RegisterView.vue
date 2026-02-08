<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { useRouter } from 'vue-router'

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
<div class="relative min-h-screen w-full flex items-center justify-center overflow-hidden py-3 pt-20">
    <!-- Background Image with Better Visibility (40% smaller) -->
    <div class="absolute inset-0 z-0 flex items-center justify-center">
        <img
            src="@/shared/assets/images/backgroundEMI.png"
            alt="EMI Background"
            class="w-3/5 h-3/5 object-contain opacity-20"
        />
    </div>

    <!-- Lighter Gradient Overlay -->
    <div class="absolute inset-0 z-0 bg-gradient-to-br from-gray-50/70 via-gray-50/50 to-blue-50/70"></div>

    <!-- Main Register Container with Glassmorphism -->
    <div class="relative z-10 w-full max-w-md mx-4">
        <div class="backdrop-blur-lg bg-white/70 rounded-2xl shadow-2xl border border-white/60 p-5 transition-all duration-300">
            <!-- Header -->
            <div class="text-center mb-3">
                <img src="@/shared/assets/icons/logoEmi.png" alt="EMI Logo" class="w-14 h-14 mx-auto mb-2 object-contain" />
            </div>

            <!-- Title -->
            <h2 class="text-lg font-bold text-emi-navy-700 text-center mb-3">Registrarse</h2>

            <!-- Register Form -->
            <form @submit.prevent="handleRegister" class="space-y-2.5">
                <!-- Role Selector -->
                <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1.5">Tipo de Usuario</label>
                    <div class="grid grid-cols-3 gap-2">
                        <label
                            class="relative cursor-pointer"
                            :class="role === 'estudiante' ? 'ring-2 ring-emi-navy-500' : ''"
                            @click="role = 'estudiante'"
                        >
                            <input type="radio" value="estudiante" v-model="role" class="sr-only" />
                            <div class="bg-white/60 backdrop-blur border-2 rounded-lg py-2 px-3 text-center transition-all hover:border-emi-navy-500"
                                 :class="role === 'estudiante' ? 'border-emi-navy-500 bg-emi-navy-50/50' : 'border-gray-200'">
                                <div class="text-xs font-semibold text-gray-700">Estudiante</div>
                            </div>
                        </label>
                        <label
                            class="relative cursor-pointer"
                            :class="role === 'titulado' ? 'ring-2 ring-emi-navy-500' : ''"
                            @click="role = 'titulado'"
                        >
                            <input type="radio" value="titulado" v-model="role" class="sr-only" />
                            <div class="bg-white/60 backdrop-blur border-2 rounded-lg py-2 px-3 text-center transition-all hover:border-emi-navy-500"
                                 :class="role === 'titulado' ? 'border-emi-navy-500 bg-emi-navy-50/50' : 'border-gray-200'">
                                <div class="text-xs font-semibold text-gray-700">Titulado</div>
                            </div>
                        </label>
                        <label
                            class="relative cursor-pointer"
                            :class="role === 'operador' ? 'ring-2 ring-emi-navy-500' : ''"
                            @click="role = 'operador'"
                        >
                            <input type="radio" value="operador" v-model="role" class="sr-only" />
                            <div class="bg-white/60 backdrop-blur border-2 rounded-lg py-2 px-3 text-center transition-all hover:border-emi-navy-500"
                                 :class="role === 'operador' ? 'border-emi-navy-500 bg-emi-navy-50/50' : 'border-gray-200'">
                                <div class="text-xs font-semibold text-gray-700">Operador</div>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Name Input -->
                <div>
                    <label for="registerName" class="block text-xs font-medium text-gray-700 mb-1">
                        Nombre Completo
                    </label>
                    <input
                        type="text"
                        id="registerName"
                        v-model="name"
                        placeholder="Juan Pérez Gómez"
                        required
                        class="w-full px-3 py-2 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg focus:outline-none focus:border-emi-navy-500 focus:ring-2 focus:ring-emi-navy-500/10 transition-all text-gray-800 placeholder-gray-400 text-sm"
                    />
                </div>

                <!-- Email Input -->
                <div>
                    <label for="registerEmail" class="block text-xs font-medium text-gray-700 mb-1">
                        Correo Electrónico
                    </label>
                    <input
                        type="email"
                        id="registerEmail"
                        v-model="email"
                        placeholder="correo@est.emi.edu.bo"
                        required
                        class="w-full px-3 py-2 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg focus:outline-none focus:border-emi-navy-500 focus:ring-2 focus:ring-emi-navy-500/10 transition-all text-gray-800 placeholder-gray-400 text-sm"
                    />
                </div>

                <!-- Password Input -->
                <div>
                    <label for="registerPassword" class="block text-xs font-medium text-gray-700 mb-1">
                        Contraseña
                    </label>
                    <input
                        type="password"
                        id="registerPassword"
                        v-model="password"
                        @input="checkPasswordStrength"
                        placeholder="Mínimo 8 caracteres"
                        required
                        class="w-full px-3 py-2 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg focus:outline-none focus:border-emi-navy-500 focus:ring-2 focus:ring-emi-navy-500/10 transition-all text-gray-800 placeholder-gray-400 text-sm"
                    />
                    <!-- Password Strength Indicator -->
                    <div class="h-1 bg-gray-200 rounded-full mt-1 overflow-hidden">
                        <div
                            class="h-full transition-all duration-300 rounded-full"
                            :class="{
                                'w-1/3 bg-red-500': passwordStrength === 'weak',
                                'w-2/3 bg-yellow-500': passwordStrength === 'medium',
                                'w-full bg-green-500': passwordStrength === 'strong'
                            }"
                        ></div>
                    </div>
                </div>

                <!-- Confirm Password Input -->
                <div>
                    <label for="registerConfirmPassword" class="block text-xs font-medium text-gray-700 mb-1">
                        Confirmar Contraseña
                    </label>
                    <input
                        type="password"
                        id="registerConfirmPassword"
                        v-model="confirmPassword"
                        placeholder="Repite tu contraseña"
                        required
                        class="w-full px-3 py-2 bg-white/60 backdrop-blur border-2 border-gray-200 rounded-lg focus:outline-none focus:border-emi-navy-500 focus:ring-2 focus:ring-emi-navy-500/10 transition-all text-gray-800 placeholder-gray-400 text-sm"
                    />
                </div>

                <!-- Error/Success Messages -->
                <div v-if="error" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-2 rounded-lg text-xs">
                    {{ error }}
                </div>

                <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 text-green-700 p-2 rounded-lg text-xs">
                    {{ successMessage }}
                </div>

                <!-- Submit Button -->
                <button
                    type="submit"
                    :disabled="isLoading"
                    class="w-full py-2.5 bg-gradient-to-r from-emi-navy-500 to-emi-navy-700 text-white font-semibold rounded-lg shadow-lg shadow-emi-navy-500/30 hover:shadow-xl hover:shadow-emi-navy-500/40 hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-sm"
                >
                    {{ isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}
                </button>
            </form>


            <!-- Footer -->
            <div class="text-center mt-3 pt-3 border-t border-gray-200">
                <div class="text-xs text-gray-500 italic mb-1">
                    "Mcal. Antonio José de Sucre"<br>
                    <strong class="text-emi-gold-600">Prestigio, Disciplina y Oportunidades</strong>
                </div>
                <p class="text-xs text-gray-400">© 2026 DNTIC - Escuela Militar de Ingeniería</p>
            </div>
        </div>
    </div>
</div>
</template>
