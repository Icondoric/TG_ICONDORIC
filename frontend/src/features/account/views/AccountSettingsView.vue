<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- Encabezado -->
      <header class="mb-8">
        <h1 class="text-3xl font-bold text-emi-navy-500">Configurar Mi Cuenta</h1>
        <p class="mt-1 text-slate-500">Administra tu información personal y configuración de seguridad</p>
      </header>

      <!-- Cargando -->
      <div v-if="loading" class="card-emi p-12 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-gold mx-auto"></div>
        <p class="mt-4 text-slate-500">Cargando datos...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
        <svg class="w-5 h-5 text-red-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <p class="text-red-700 text-sm">{{ error }}</p>
          <button @click="loadAccountInfo" class="mt-1 text-red-600 hover:text-red-800 underline text-xs">Reintentar</button>
        </div>
      </div>

      <!-- Contenido -->
      <div v-else class="space-y-6">

        <!-- ── Información Personal ── -->
        <div class="card-emi p-6">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-9 h-9 bg-emi-navy-100 rounded-xl flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-emi-navy-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div>
              <h2 class="text-base font-semibold text-emi-navy-800">Información Personal</h2>
              <p class="text-xs text-slate-400 mt-0.5">Nombre y correo con los que apareces en el sistema</p>
            </div>
          </div>

          <form @submit.prevent="updatePersonalInfo" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Nombre Completo</label>
                <input
                  v-model="personalForm.nombre_completo"
                  type="text"
                  placeholder="Ingresa tu nombre completo"
                  class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Correo Electrónico</label>
                <input
                  v-model="personalForm.email"
                  type="email"
                  placeholder="tu@email.com"
                  class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                />
                <p class="mt-1 text-xs text-slate-400">Este correo se usará para iniciar sesión</p>
              </div>
            </div>

            <div v-if="personalSuccess" class="p-3 bg-success-50 border border-success-200 rounded-lg flex items-center gap-2">
              <svg class="w-4 h-4 text-success-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <p class="text-success-700 text-sm">{{ personalSuccess }}</p>
            </div>
            <div v-if="personalError" class="p-3 bg-danger-50 border border-danger-200 rounded-lg">
              <p class="text-danger-700 text-sm">{{ personalError }}</p>
            </div>

            <div class="flex justify-end pt-1">
              <button
                type="submit"
                :disabled="savingPersonal || !hasPersonalChanges"
                class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ savingPersonal ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </div>

        <!-- ── Información Académica (solo estudiantes y titulados) ── -->
        <div v-if="accountInfo.rol === 'estudiante' || accountInfo.rol === 'titulado'" class="card-emi p-6">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-9 h-9 bg-info-100 rounded-xl flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-info-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
              </svg>
            </div>
            <div>
              <h2 class="text-base font-semibold text-emi-navy-800">Información Académica</h2>
              <p class="text-xs text-slate-400 mt-0.5">Usada para verificar tu elegibilidad en la correspondencia de perfiles</p>
            </div>
          </div>

          <div class="p-3 bg-info-50 border border-info-100 rounded-lg mb-5 mt-4 flex items-start gap-2">
            <svg class="w-4 h-4 text-info-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-info-700 text-xs leading-relaxed">
              Estos datos determinan si cumples el filtro de elegibilidad en ofertas que requieren una carrera o semestre específico.
              Mantenlos actualizados para recibir recomendaciones precisas.
            </p>
          </div>

          <form @submit.prevent="updateAcademicInfo" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Carrera</label>
                <select
                  v-model="academicForm.carrera"
                  class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                >
                  <option value="">Sin especificar</option>
                  <option v-for="c in EMI_CARRERAS" :key="c" :value="c">{{ c }}</option>
                </select>
              </div>
              <div v-if="isEstudiante">
                <label class="block text-sm font-medium text-slate-700 mb-1">Semestre Actual</label>
                <select
                  v-model.number="academicForm.semestre_actual"
                  class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                >
                  <option :value="null">Sin especificar</option>
                  <option v-for="n in 10" :key="n" :value="n">{{ n }}° semestre</option>
                </select>
                <p class="mt-1 text-xs text-slate-400">Solo aplica a estudiantes activos</p>
              </div>
            </div>

            <div v-if="academicSuccess" class="p-3 bg-success-50 border border-success-200 rounded-lg flex items-center gap-2">
              <svg class="w-4 h-4 text-success-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <p class="text-success-700 text-sm">{{ academicSuccess }}</p>
            </div>
            <div v-if="academicError" class="p-3 bg-danger-50 border border-danger-200 rounded-lg">
              <p class="text-danger-700 text-sm">{{ academicError }}</p>
            </div>

            <div class="flex justify-end pt-1">
              <button
                type="submit"
                :disabled="savingAcademic || !hasAcademicChanges"
                class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ savingAcademic ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </div>

        <!-- ── Cambiar Contraseña ── -->
        <div class="card-emi p-6">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-9 h-9 bg-warning-100 rounded-xl flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h2 class="text-base font-semibold text-emi-navy-800">Cambiar Contraseña</h2>
              <p class="text-xs text-slate-400 mt-0.5">Actualiza tu contraseña de acceso al sistema</p>
            </div>
          </div>

          <form @submit.prevent="updatePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Contraseña Actual</label>
              <input
                v-model="passwordForm.current_password"
                type="password"
                placeholder="••••••••"
                class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
              />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Nueva Contraseña</label>
                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  placeholder="••••••••"
                  class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                />
                <p class="mt-1 text-xs text-slate-400">Mínimo 6 caracteres</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Confirmar Nueva Contraseña</label>
                <input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  placeholder="••••••••"
                  class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                />
              </div>
            </div>

            <div v-if="passwordValidationError" class="p-3 bg-warning-50 border border-warning-200 rounded-lg">
              <p class="text-warning-700 text-sm">{{ passwordValidationError }}</p>
            </div>
            <div v-if="passwordSuccess" class="p-3 bg-success-50 border border-success-200 rounded-lg flex items-center gap-2">
              <svg class="w-4 h-4 text-success-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <p class="text-success-700 text-sm">{{ passwordSuccess }}</p>
            </div>
            <div v-if="passwordError" class="p-3 bg-danger-50 border border-danger-200 rounded-lg">
              <p class="text-danger-700 text-sm">{{ passwordError }}</p>
            </div>

            <div class="flex justify-end pt-1">
              <button
                type="submit"
                :disabled="savingPassword || !isPasswordFormValid"
                class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ savingPassword ? 'Actualizando...' : 'Cambiar Contraseña' }}
              </button>
            </div>
          </form>
        </div>

        <!-- ── Aviso de seguridad ── -->
        <div class="p-5 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-3">
          <div class="w-9 h-9 bg-amber-100 rounded-lg flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-amber-800 text-sm">Seguridad de tu Cuenta</h3>
            <ul class="mt-2 text-sm text-amber-700 space-y-1">
              <li>• Usa una contraseña segura y única</li>
              <li>• No compartas tus credenciales con nadie</li>
              <li>• Si cambias tu correo, úsalo para iniciar sesión la próxima vez</li>
            </ul>
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

const loading = ref(true)
const error = ref(null)
const accountInfo = ref({ id: '', email: '', nombre_completo: '', rol: '', created_at: '' })

const academicForm = ref({ carrera: '', semestre_actual: null })
const originalAcademic = ref({ carrera: '', semestre_actual: null })
const savingAcademic = ref(false)
const academicSuccess = ref('')
const academicError = ref('')

const personalForm = ref({ nombre_completo: '', email: '' })
const savingPersonal = ref(false)
const personalSuccess = ref('')
const personalError = ref('')

const passwordForm = ref({ current_password: '', new_password: '', confirm_password: '' })
const savingPassword = ref(false)
const passwordSuccess = ref('')
const passwordError = ref('')

const isEstudiante = computed(() => authStore.user?.rol === 'estudiante')

const hasPersonalChanges = computed(() =>
  personalForm.value.nombre_completo !== accountInfo.value.nombre_completo ||
  personalForm.value.email !== accountInfo.value.email
)

const hasAcademicChanges = computed(() =>
  academicForm.value.carrera !== originalAcademic.value.carrera ||
  academicForm.value.semestre_actual !== originalAcademic.value.semestre_actual
)

const passwordValidationError = computed(() => {
  if (!passwordForm.value.new_password) return ''
  if (passwordForm.value.new_password.length < 6) return 'La contraseña debe tener al menos 6 caracteres'
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) return 'Las contraseñas no coinciden'
  return ''
})

const isPasswordFormValid = computed(() =>
  passwordForm.value.current_password &&
  passwordForm.value.new_password &&
  passwordForm.value.confirm_password &&
  !passwordValidationError.value
)

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
    if (academicForm.value.carrera !== originalAcademic.value.carrera)
      updates.carrera = academicForm.value.carrera || null
    if (academicForm.value.semestre_actual !== originalAcademic.value.semestre_actual)
      updates.semestre_actual = academicForm.value.semestre_actual || null
    await updateMyProfile(updates)
    originalAcademic.value = { ...academicForm.value }
    academicSuccess.value = 'Información académica actualizada correctamente'
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
    if (personalForm.value.nombre_completo !== accountInfo.value.nombre_completo)
      updates.nombre_completo = personalForm.value.nombre_completo
    if (personalForm.value.email !== accountInfo.value.email)
      updates.email = personalForm.value.email
    const response = await updateAccount(updates)
    accountInfo.value = { ...accountInfo.value, ...response.user }
    authStore.user.nombre_completo = response.user.nombre_completo
    authStore.user.email = response.user.email
    localStorage.setItem('user', JSON.stringify(authStore.user))
    personalSuccess.value = 'Información actualizada exitosamente'
    setTimeout(() => { personalSuccess.value = '' }, 3000)
  } catch (err) {
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
    await changePassword(passwordForm.value.current_password, passwordForm.value.new_password)
    passwordSuccess.value = 'Contraseña actualizada exitosamente'
    passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
    setTimeout(() => { passwordSuccess.value = '' }, 3000)
  } catch (err) {
    passwordError.value = formatApiError(err, 'Error al cambiar contraseña')
  } finally {
    savingPassword.value = false
  }
}

onMounted(() => { loadAccountInfo() })
</script>
