<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-slate-800">Ver Mi Cuenta</h1>
        <p class="mt-1 text-slate-600">
          Información general de tu cuenta
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

        <!-- Hero Card: Avatar + Identity -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="h-24 bg-gradient-to-r"
               :class="roleGradient"
          ></div>
          <div class="px-6 pb-6 -mt-12">
            <div class="flex flex-col sm:flex-row sm:items-end gap-4">
              <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center font-bold text-3xl shadow-lg border-4 border-white"
                   :class="roleTextColor"
              >
                {{ (accountInfo.nombre_completo || accountInfo.email || '?').charAt(0).toUpperCase() }}
              </div>
              <div class="flex-1">
                <h2 class="text-2xl font-bold text-slate-800">{{ accountInfo.nombre_completo || 'Sin nombre' }}</h2>
                <p class="text-slate-500 text-sm mt-0.5">{{ accountInfo.email }}</p>
              </div>
              <span :class="['px-3 py-1.5 rounded-full text-xs font-semibold capitalize self-start sm:self-auto', roleBadgeColor]">
                  {{ accountInfo.rol }}
              </span>
            </div>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <!-- Tipo de Cuenta -->
          <div class="bg-white rounded-xl shadow-md p-5">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-9 h-9 rounded-lg flex items-center justify-center" :class="roleIconBg">
                <svg class="w-5 h-5" :class="roleIconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Tipo de Cuenta</span>
            </div>
            <p class="text-lg font-bold text-slate-800 capitalize">{{ accountInfo.rol }}</p>
          </div>

          <!-- Miembro Desde -->
          <div class="bg-white rounded-xl shadow-md p-5">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-9 h-9 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Miembro desde</span>
            </div>
            <p class="text-lg font-bold text-slate-800">{{ formatDate(accountInfo.created_at) }}</p>
          </div>

          <!-- Estado -->
          <div class="bg-white rounded-xl shadow-md p-5">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-9 h-9 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Estado</span>
            </div>
            <p class="text-lg font-bold text-green-600">Activa</p>
          </div>
        </div>

        <!-- Account Details Card -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-lg font-semibold text-slate-800 flex items-center gap-2 mb-5">
            <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Detalles de la Cuenta
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="p-4 bg-slate-50 rounded-lg">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Nombre Completo</p>
              <p class="text-sm font-semibold text-slate-800">{{ accountInfo.nombre_completo || 'Sin definir' }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Correo Electrónico</p>
              <p class="text-sm font-semibold text-slate-800">{{ accountInfo.email }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Rol Asignado</p>
              <p class="text-sm font-semibold text-slate-800 capitalize">{{ accountInfo.rol }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">Fecha de Registro</p>
              <p class="text-sm font-semibold text-slate-800">{{ formatDate(accountInfo.created_at) }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg sm:col-span-2">
              <p class="text-xs text-slate-400 uppercase tracking-wider font-medium mb-1">ID de Usuario</p>
              <p class="text-sm font-mono text-slate-600">{{ accountInfo.id }}</p>
            </div>
          </div>
        </div>

        <!-- Quick Action -->
        <div class="flex justify-center">
          <router-link
            to="/configurar-cuenta"
            class="inline-flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm transition-colors shadow-sm"
          >
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
import { useAuthStore } from '@/features/auth/store/auth.store'
import AppLayout from '@/shared/components/AppLayout.vue'

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

// Computed role styles
const rol = computed(() => authStore.user?.rol)

const roleGradient = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'from-purple-500 to-purple-700'
    case 'operador': return 'from-orange-400 to-orange-600'
    case 'titulado': return 'from-indigo-500 to-indigo-700'
    default: return 'from-blue-500 to-blue-700'
  }
})

const roleTextColor = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'text-purple-600'
    case 'operador': return 'text-orange-600'
    case 'titulado': return 'text-indigo-600'
    default: return 'text-blue-600'
  }
})

const roleBadgeColor = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'bg-purple-100 text-purple-700'
    case 'operador': return 'bg-orange-100 text-orange-700'
    case 'titulado': return 'bg-indigo-100 text-indigo-700'
    default: return 'bg-blue-100 text-blue-700'
  }
})

const roleIconBg = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'bg-purple-100'
    case 'operador': return 'bg-orange-100'
    case 'titulado': return 'bg-indigo-100'
    default: return 'bg-blue-100'
  }
})

const roleIconColor = computed(() => {
  switch (rol.value) {
    case 'administrador': return 'text-purple-600'
    case 'operador': return 'text-orange-600'
    case 'titulado': return 'text-indigo-600'
    default: return 'text-blue-600'
  }
})

// Methods
const loadAccountInfo = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await getAccountInfo()
    accountInfo.value = data
  } catch (err) {
    console.error('Error loading account info:', err)
    error.value = err.response?.data?.detail || 'Error al cargar información de la cuenta'
  } finally {
    loading.value = false
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
