<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-emi-navy-500">Configuración de Cuenta</h1>
        <p class="mt-2 text-gray-600">
          Administra tu información personal y configuración de seguridad
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
      </div>

      <!-- Error State -->
      <Card v-else-if="error" class="border-red-200 bg-red-50">
        <p class="text-red-700">{{ error }}</p>
        <button @click="loadAccountInfo" class="mt-2 text-red-600 hover:text-red-800 underline">
          Reintentar
        </button>
      </Card>

      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Account Information Card -->


        <!-- Personal Information Card -->
        <Card title="Información Personal">
          <form @submit.prevent="updatePersonalInfo" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre Completo</label>
              <input
                v-model="personalForm.nombre_completo"
                type="text"
                placeholder="Ingresa tu nombre completo"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                v-model="personalForm.email"
                type="email"
                placeholder="tu@email.com"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
              <p class="mt-1 text-xs text-gray-500">Este email se usará para iniciar sesión</p>
            </div>

            <!-- Success/Error Messages -->
            <div v-if="personalSuccess" class="p-3 bg-green-50 border border-green-200 rounded-lg">
              <p class="text-green-700 text-sm flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ personalSuccess }}
              </p>
            </div>
            <div v-if="personalError" class="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-700 text-sm">{{ personalError }}</p>
            </div>

            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="savingPersonal || !hasPersonalChanges"
                class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ savingPersonal ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </Card>

        <!-- Password Change Card -->
        <Card title="Cambiar Contraseña">
          <form @submit.prevent="updatePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña Actual</label>
              <input
                v-model="passwordForm.current_password"
                type="password"
                placeholder="••••••••"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nueva Contraseña</label>
              <input
                v-model="passwordForm.new_password"
                type="password"
                placeholder="••••••••"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
              <p class="mt-1 text-xs text-gray-500">Mínimo 6 caracteres</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Confirmar Nueva Contraseña</label>
              <input
                v-model="passwordForm.confirm_password"
                type="password"
                placeholder="••••••••"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
            </div>

            <!-- Password Validation Messages -->
            <div v-if="passwordValidationError" class="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p class="text-yellow-700 text-sm">{{ passwordValidationError }}</p>
            </div>

            <!-- Success/Error Messages -->
            <div v-if="passwordSuccess" class="p-3 bg-green-50 border border-green-200 rounded-lg">
              <p class="text-green-700 text-sm flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ passwordSuccess }}
              </p>
            </div>
            <div v-if="passwordError" class="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-700 text-sm">{{ passwordError }}</p>
            </div>

            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="savingPassword || !isPasswordFormValid"
                class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ savingPassword ? 'Actualizando...' : 'Cambiar Contraseña' }}
              </button>
            </div>
          </form>
        </Card>

        <!-- Security Notice -->
        <Card class="border-emi-gold-200 bg-emi-gold-50">
          <div class="flex items-start gap-3">
            <div class="p-2 bg-emi-gold-100 rounded-full">
              <svg class="w-5 h-5 text-emi-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-emi-gold-800">Seguridad de tu Cuenta</h3>
              <ul class="mt-2 text-sm text-emi-gold-700 space-y-1">
                <li>• Usa una contraseña segura y única</li>
                <li>• No compartas tus credenciales con nadie</li>
                <li>• Si cambias tu email, úsalo para iniciar sesión la próxima vez</li>
              </ul>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getAccountInfo, updateAccount, changePassword } from '@/features/account/api/account.api'
import { useAuthStore } from '@/features/auth/store/auth.store'
import AppLayout from '@/shared/components/AppLayout.vue'
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'

const authStore = useAuthStore()

// State
const loading = ref(true)
const error = ref(null)
const accountInfo = ref({
  id: '',
  email: '',
  nombre_completo: '',
  rol: '',
  created_at: ''
})

// Personal Info Form
const personalForm = ref({
  nombre_completo: '',
  email: ''
})
const savingPersonal = ref(false)
const personalSuccess = ref('')
const personalError = ref('')

// Password Form
const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})
const savingPassword = ref(false)
const passwordSuccess = ref('')
const passwordError = ref('')

// Computed
const hasPersonalChanges = computed(() => {
  return personalForm.value.nombre_completo !== accountInfo.value.nombre_completo ||
         personalForm.value.email !== accountInfo.value.email
})

const passwordValidationError = computed(() => {
  if (!passwordForm.value.new_password) return ''
  if (passwordForm.value.new_password.length < 6) {
    return 'La contraseña debe tener al menos 6 caracteres'
  }
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    return 'Las contraseñas no coinciden'
  }
  return ''
})

const isPasswordFormValid = computed(() => {
  return passwordForm.value.current_password &&
         passwordForm.value.new_password &&
         passwordForm.value.confirm_password &&
         !passwordValidationError.value
})

// Methods
const loadAccountInfo = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await getAccountInfo()
    accountInfo.value = data

    // Initialize form with current data
    personalForm.value.nombre_completo = data.nombre_completo || ''
    personalForm.value.email = data.email
  } catch (err) {
    console.error('Error loading account info:', err)
    error.value = err.response?.data?.detail || 'Error al cargar información de la cuenta'
  } finally {
    loading.value = false
  }
}

const updatePersonalInfo = async () => {
  savingPersonal.value = true
  personalSuccess.value = ''
  personalError.value = ''

  try {
    const updates = {}
    if (personalForm.value.nombre_completo !== accountInfo.value.nombre_completo) {
      updates.nombre_completo = personalForm.value.nombre_completo
    }
    if (personalForm.value.email !== accountInfo.value.email) {
      updates.email = personalForm.value.email
    }

    const response = await updateAccount(updates)

    // Update local account info
    accountInfo.value = { ...accountInfo.value, ...response.user }

    // Update auth store
    authStore.user.nombre_completo = response.user.nombre_completo
    authStore.user.email = response.user.email
    localStorage.setItem('user', JSON.stringify(authStore.user))

    personalSuccess.value = 'Información actualizada exitosamente'

    // Clear success message after 3 seconds
    setTimeout(() => {
      personalSuccess.value = ''
    }, 3000)
  } catch (err) {
    console.error('Error updating personal info:', err)
    personalError.value = err.response?.data?.detail || 'Error al actualizar información'
  } finally {
    savingPersonal.value = false
  }
}

const updatePassword = async () => {
  savingPassword.value = true
  passwordSuccess.value = ''
  passwordError.value = ''

  try {
    await changePassword(
      passwordForm.value.current_password,
      passwordForm.value.new_password
    )

    passwordSuccess.value = 'Contraseña actualizada exitosamente'

    // Clear form
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }

    // Clear success message after 3 seconds
    setTimeout(() => {
      passwordSuccess.value = ''
    }, 3000)
  } catch (err) {
    console.error('Error changing password:', err)
    passwordError.value = err.response?.data?.detail || 'Error al cambiar contraseña'
  } finally {
    savingPassword.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Lifecycle
onMounted(() => {
  loadAccountInfo()
})
</script>
