<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-slate-800">Configurar Mi Cuenta</h1>
        <p class="mt-1 text-slate-600">
          Administra tu información personal y configuración de seguridad
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white rounded-xl shadow-md p-12 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-slate-500">Cargando datos...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4">
        <p class="text-red-700">{{ error }}</p>
        <button @click="loadAccountInfo" class="mt-2 text-red-600 hover:text-red-800 underline text-sm">
          Reintentar
        </button>
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">

        <!-- Personal Information Card -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-lg font-semibold text-slate-800 flex items-center gap-2 mb-5">
            <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Información Personal
          </h2>
          <form @submit.prevent="updatePersonalInfo" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Nombre Completo</label>
                <input
                  v-model="personalForm.nombre_completo"
                  type="text"
                  placeholder="Ingresa tu nombre completo"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
                <input
                  v-model="personalForm.email"
                  type="email"
                  placeholder="tu@email.com"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <p class="mt-1 text-xs text-slate-500">Este email se usará para iniciar sesión</p>
              </div>
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
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
              >
                {{ savingPersonal ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Academic Info Card (solo para estudiantes y titulados) -->
        <div v-if="accountInfo.rol === 'estudiante' || accountInfo.rol === 'titulado'" class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-lg font-semibold text-slate-800 flex items-center gap-2 mb-5">
            <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
            </svg>
            Información Académica
          </h2>
          <p class="text-sm text-slate-500 mb-4 -mt-3">
            Esta información se usa para verificar tu elegibilidad en convocatorias que requieren carrera o semestre específico.
          </p>
          <form @submit.prevent="updateAcademicInfo" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Carrera</label>
                <select
                  v-model="academicForm.carrera"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Sin especificar</option>
                  <option v-for="c in EMI_CARRERAS" :key="c" :value="c">{{ c }}</option>
                </select>
              </div>
              <div v-if="isEstudiante">
                <label class="block text-sm font-medium text-slate-700 mb-1">Semestre Actual</label>
                <select
                  v-model.number="academicForm.semestre_actual"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option :value="null">Sin especificar</option>
                  <option v-for="n in 10" :key="n" :value="n">{{ n }}° semestre</option>
                </select>
                <p class="mt-1 text-xs text-slate-500">Solo requerido para estudiantes activos</p>
              </div>
            </div>

            <div v-if="academicSuccess" class="p-3 bg-green-50 border border-green-200 rounded-lg">
              <p class="text-green-700 text-sm flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ academicSuccess }}
              </p>
            </div>
            <div v-if="academicError" class="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-700 text-sm">{{ academicError }}</p>
            </div>

            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="savingAcademic || !hasAcademicChanges"
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
              >
                {{ savingAcademic ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Password Change Card -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-lg font-semibold text-slate-800 flex items-center gap-2 mb-5">
            <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Cambiar Contraseña
          </h2>
          <form @submit.prevent="updatePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Contraseña Actual</label>
              <input
                v-model="passwordForm.current_password"
                type="password"
                placeholder="••••••••"
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Nueva Contraseña</label>
                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  placeholder="••••••••"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <p class="mt-1 text-xs text-slate-500">Mínimo 6 caracteres</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Confirmar Nueva Contraseña</label>
                <input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  placeholder="••••••••"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
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
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
              >
                {{ savingPassword ? 'Actualizando...' : 'Cambiar Contraseña' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Security Notice -->
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <div class="flex items-start gap-3">
            <div class="w-9 h-9 bg-amber-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-amber-800">Seguridad de tu Cuenta</h3>
              <ul class="mt-2 text-sm text-amber-700 space-y-1">
                <li>• Usa una contraseña segura y única</li>
                <li>• No compartas tus credenciales con nadie</li>
                <li>• Si cambias tu email, úsalo para iniciar sesión la próxima vez</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getAccountInfo, updateAccount, changePassword } from '@/features/account/api/account.api'
import { getMyProfile, updateMyProfile } from '@/features/profile/api/profile.api'
import { useAuthStore } from '@/features/auth/store/auth.store'
import AppLayout from '@/shared/components/AppLayout.vue'
import { formatApiError } from '@/shared/utils/apiError'

const authStore = useAuthStore()

const EMI_CARRERAS = [
  'Ingenieria Civil',
  'Ingenieria de Sistemas',
  'Ingenieria Geografica',
  'Ingenieria Mecatronica',
  'Ingenieria en Sistemas Electronicos',
  'Ingenieria Financiera',
  'Ingenieria Industrial',
  'Derecho',
  'Ingenieria Comercial',
]

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

// Academic Info Form
const academicForm = ref({ carrera: '', semestre_actual: null })
const originalAcademic = ref({ carrera: '', semestre_actual: null })
const savingAcademic = ref(false)
const academicSuccess = ref('')
const academicError = ref('')

const isEstudiante = computed(() => authStore.user?.rol === 'estudiante')
const hasAcademicChanges = computed(() =>
  academicForm.value.carrera !== originalAcademic.value.carrera ||
  academicForm.value.semestre_actual !== originalAcademic.value.semestre_actual
)

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
    const [data, profileData] = await Promise.all([getAccountInfo(), getMyProfile().catch(() => null)])
    accountInfo.value = data
    personalForm.value.nombre_completo = data.nombre_completo || ''
    personalForm.value.email = data.email

    if (profileData) {
      academicForm.value.carrera = profileData.carrera || ''
      academicForm.value.semestre_actual = profileData.semestre_actual ?? null
      originalAcademic.value.carrera = profileData.carrera || ''
      originalAcademic.value.semestre_actual = profileData.semestre_actual ?? null
    }
  } catch (err) {
    console.error('Error loading account info:', err)
    error.value = formatApiError(err, 'Error al cargar información de la cuenta')
  } finally {
    loading.value = false
  }
}

const updateAcademicInfo = async () => {
  savingAcademic.value = true
  academicSuccess.value = ''
  academicError.value = ''

  try {
    const updates = {}
    if (academicForm.value.carrera !== originalAcademic.value.carrera) {
      updates.carrera = academicForm.value.carrera || null
    }
    if (academicForm.value.semestre_actual !== originalAcademic.value.semestre_actual) {
      updates.semestre_actual = academicForm.value.semestre_actual || null
    }

    await updateMyProfile(updates)
    originalAcademic.value = { ...academicForm.value }
    academicSuccess.value = 'Información académica actualizada'
    setTimeout(() => { academicSuccess.value = '' }, 3000)
  } catch (err) {
    academicError.value = formatApiError(err, 'Error al actualizar información académica')
  } finally {
    savingAcademic.value = false
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
    personalError.value = formatApiError(err, 'Error al actualizar información')
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
    passwordError.value = formatApiError(err, 'Error al cambiar contraseña')
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
