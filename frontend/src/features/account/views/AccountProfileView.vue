<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- Encabezado -->
      <header class="mb-8">
        <h1 class="text-3xl font-bold text-emi-navy-500">Mi Cuenta</h1>
        <p class="mt-1 text-slate-500">Información general de tu cuenta en el sistema</p>
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
          <button @click="loadAccountInfo" class="mt-1 text-red-600 hover:text-red-800 underline text-xs">
            Reintentar
          </button>
        </div>
      </div>

      <!-- Contenido -->
      <div v-else class="space-y-6">

        <!-- ── Hero: avatar + identidad ── -->
        <div class="card-emi !p-0 overflow-hidden">
          <div class="h-20 w-full" :class="roleGradient"></div>
          <div class="px-6 pb-6 -mt-10">
            <div class="flex flex-col sm:flex-row sm:items-end gap-4">
              <!-- Avatar inicial -->
              <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center font-bold text-3xl shadow-lg border-4 border-white shrink-0"
                :class="roleTextColor">
                {{ (accountInfo.nombre_completo || accountInfo.email || '?').charAt(0).toUpperCase() }}
              </div>
              <div class="flex-1 pb-1">
                <h2 class="text-xl font-bold text-emi-navy-800">{{ accountInfo.nombre_completo || 'Sin nombre' }}</h2>
                <p class="text-slate-400 text-sm">{{ accountInfo.email }}</p>
              </div>
              <span :class="['badge-emi self-start sm:self-auto mb-1', roleBadgeColor]">
                {{ accountInfo.rol }}
              </span>
            </div>
          </div>
        </div>

        <!-- ── Stats: tipo, miembro desde, estado ── -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="card-emi p-5">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" :class="roleIconBg">
                <svg class="w-4 h-4" :class="roleIconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Tipo de cuenta</span>
            </div>
            <p class="text-base font-bold text-emi-navy-800 capitalize">{{ accountInfo.rol }}</p>
          </div>

          <div class="card-emi p-5">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center shrink-0">
                <svg class="w-4 h-4 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Miembro desde</span>
            </div>
            <p class="text-base font-bold text-emi-navy-800">{{ formatDate(accountInfo.created_at) }}</p>
          </div>

          <div class="card-emi p-5">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center shrink-0">
                <svg class="w-4 h-4 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Estado</span>
            </div>
            <p class="text-base font-bold text-success-600">Activa</p>
          </div>
        </div>

        <!-- ── Detalles de la cuenta ── -->
        <div class="card-emi p-6">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-9 h-9 bg-emi-navy-100 rounded-xl flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-emi-navy-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h2 class="text-base font-semibold text-emi-navy-800">Detalles de la Cuenta</h2>
              <p class="text-xs text-slate-400 mt-0.5">Datos registrados en el sistema</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div class="p-4 bg-slate-50 rounded-xl">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Nombre Completo</p>
              <p class="text-sm font-semibold text-slate-800">{{ accountInfo.nombre_completo || 'Sin definir' }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Correo Electrónico</p>
              <p class="text-sm font-semibold text-slate-800">{{ accountInfo.email }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Rol Asignado</p>
              <p class="text-sm font-semibold text-slate-800 capitalize">{{ accountInfo.rol }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Fecha de Registro</p>
              <p class="text-sm font-semibold text-slate-800">{{ formatDate(accountInfo.created_at) }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl sm:col-span-2">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">ID de Usuario</p>
              <p class="text-sm font-mono text-slate-500">{{ accountInfo.id }}</p>
            </div>
          </div>
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

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-5">
            <div class="p-4 bg-slate-50 rounded-xl">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Carrera</p>
              <p class="text-sm font-semibold text-slate-800">
                {{ profileData.carrera || 'Sin especificar' }}
              </p>
              <p v-if="!profileData.carrera" class="text-xs text-warning-600 mt-1">
                Sin carrera definida — algunas ofertas pueden excluirte del filtro de elegibilidad.
              </p>
            </div>
            <div v-if="accountInfo.rol === 'estudiante'" class="p-4 bg-slate-50 rounded-xl">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Semestre Actual</p>
              <p class="text-sm font-semibold text-slate-800">
                {{ profileData.semestre_actual ? `${profileData.semestre_actual}° semestre` : 'Sin especificar' }}
              </p>
              <p v-if="!profileData.semestre_actual" class="text-xs text-warning-600 mt-1">
                Sin semestre definido — ofertas con rango de semestre podrían no considerarte.
              </p>
            </div>
          </div>
        </div>

        <!-- ── Acción rápida ── -->
        <div class="flex justify-end">
          <router-link to="/configurar-cuenta" class="btn-emi-primary inline-flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Configurar Mi Cuenta
          </router-link>
        </div>

      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getAccountInfo } from '@/features/account/api/account.api'
import { getMyProfile } from '@/features/profile/api/profile.api'
import { useAuthStore } from '@/features/auth/store/auth.store'
import AppLayout from '@/shared/components/AppLayout.vue'
import { formatApiError } from '@/shared/utils/apiError'

const authStore = useAuthStore()

const loading = ref(true)
const error = ref(null)
const accountInfo = ref({ id: '', email: '', nombre_completo: '', rol: '', created_at: '' })
const profileData = ref({ carrera: '', semestre_actual: null })

const rol = computed(() => authStore.user?.rol)

const roleGradient = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'bg-gradient-to-r from-emi-navy-700 to-emi-navy-900'
    case 'operador':      return 'bg-gradient-to-r from-emi-navy-500 to-emi-navy-700'
    case 'titulado':      return 'bg-gradient-to-r from-info-500 to-info-700'
    default:              return 'bg-gradient-to-r from-emi-navy-400 to-emi-navy-600'
  }
})

const roleTextColor = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'text-emi-navy-700'
    case 'operador':      return 'text-emi-navy-600'
    case 'titulado':      return 'text-info-600'
    default:              return 'text-emi-navy-500'
  }
})

const roleBadgeColor = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'bg-emi-navy-100 text-emi-navy-800'
    case 'operador':      return 'bg-warning-100 text-warning-700'
    case 'titulado':      return 'bg-info-100 text-info-700'
    default:              return 'bg-emi-navy-100 text-emi-navy-700'
  }
})

const roleIconBg = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'bg-emi-navy-100'
    case 'operador':      return 'bg-warning-100'
    case 'titulado':      return 'bg-info-100'
    default:              return 'bg-emi-navy-100'
  }
})

const roleIconColor = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'text-emi-navy-700'
    case 'operador':      return 'text-warning-600'
    case 'titulado':      return 'text-info-600'
    default:              return 'text-emi-navy-500'
  }
})

const loadAccountInfo = async () => {
  loading.value = true
  error.value = null
  try {
    const [data, profile] = await Promise.all([
      getAccountInfo(),
      getMyProfile().catch(() => null)
    ])
    accountInfo.value = data
    if (profile) {
      profileData.value.carrera = profile.carrera || ''
      profileData.value.semestre_actual = profile.semestre_actual ?? null
    }
  } catch (err) {
    error.value = formatApiError(err, 'Error al cargar información de la cuenta')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}

onMounted(() => { loadAccountInfo() })
</script>
