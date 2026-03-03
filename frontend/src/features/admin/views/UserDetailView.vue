<script setup>
/**
 * UserDetailView - Fase 7+
 * Vista para ver y editar detalles de un usuario especifico
 */
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUsersStore } from '@/features/admin/store/users.store'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { fetchRoles } from '@/features/system/api/roles.api'
import AppLayout from '@/shared/components/AppLayout.vue'
import { formatApiError } from '@/shared/utils/apiError'

const route = useRoute()
const router = useRouter()
const usersStore = useUsersStore()
const authStore = useAuthStore()

const userId = route.params.id
const isEditing = ref(false)
const saving = ref(false)
const showDeleteModal = ref(false)
const deleteError = ref(null)

const editForm = ref({
    nombre_completo: '',
    rol: ''
})

const FIXED_ROLES = [
    { value: 'estudiante', label: 'Estudiante' },
    { value: 'titulado', label: 'Titulado' },
    { value: 'operador', label: 'Operador' },
    { value: 'administrador', label: 'Administrador' }
]
const customRoles = ref([])
const allRoles = computed(() => [
    ...FIXED_ROLES,
    ...customRoles.value.map(r => ({ value: r.nombre, label: r.nombre }))
])

onMounted(async () => {
    try {
        const [, roles] = await Promise.all([
            usersStore.loadUser(userId),
            fetchRoles()
        ])
        customRoles.value = roles
        resetForm()
    } catch (error) {
        // Redirigir si no existe
        setTimeout(() => router.push('/admin/users'), 2000)
    }
})

const user = computed(() => usersStore.currentUser)
const profile = computed(() => usersStore.currentUserProfile)
const hasProfile = computed(() => user.value && user.value.tiene_perfil && profile.value)

const resetForm = () => {
    if (user.value) {
        editForm.value = {
            nombre_completo: user.value.nombre_completo || '',
            rol: user.value.rol
        }
    }
}

const toggleEdit = () => {
    if (isEditing.value) {
        // Cancelar y resetear
        resetForm()
    }
    isEditing.value = !isEditing.value
}

const saveChanges = async () => {
    saving.value = true
    try {
        await usersStore.updateUserAction(userId, editForm.value)
        isEditing.value = false
    } catch (error) {
        console.error('Error saving user:', error)
    } finally {
        saving.value = false
    }
}

const deleteUser = () => {
    deleteError.value = null
    showDeleteModal.value = true
}

const confirmDeleteUser = async () => {
    try {
        await usersStore.deleteUserAction(userId)
        router.push('/admin/users')
    } catch (err) {
        deleteError.value = formatApiError(err, 'Error eliminando usuario')
    }
}

const formatDate = (dateString, includeTime = false) => {
    if (!dateString) return 'N/A'
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }
    if (includeTime) {
        options.hour = '2-digit'
        options.minute = '2-digit'
    }
    return new Date(dateString).toLocaleDateString('es-ES', options)
}
</script>

<template>
    <AppLayout>
        <div class="max-w-7xl mx-auto py-8 px-4">
            <!-- Header -->
            <header class="mb-6">
                <button
                    @click="router.push('/admin/users')"
                    class="flex items-center text-emi-navy-500 hover:text-emi-gold mb-2 text-sm font-medium transition-colors"
                >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Volver a Usuarios
                </button>
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <h1 class="text-3xl font-bold text-emi-navy-500">Detalle de Usuario</h1>

                    <div class="flex gap-2" v-if="user && user.id !== authStore.user?.user_id">
                        <button
                            @click="deleteUser"
                            class="px-4 py-2 bg-danger-50 text-danger-600 rounded-lg hover:bg-danger-100 transition-colors font-medium border border-danger-100"
                        >
                            Eliminar Cuenta
                        </button>
                    </div>
                </div>
            </header>

            <!-- Loading -->
            <div v-if="usersStore.loading && !user" class="card-emi p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-gold mx-auto"></div>
                <p class="mt-4 text-slate-500">Cargando datos...</p>
            </div>

            <!-- Error -->
            <div v-else-if="usersStore.error" class="bg-danger-50 border border-danger-200 rounded-lg p-4 mb-6">
                <p class="text-danger-700">{{ usersStore.error }}</p>
            </div>

            <!-- Content -->
            <div v-else-if="user" class="max-w-3xl mx-auto space-y-6">

                <!-- Hero Card: Avatar + Identity -->
                <div class="card-emi overflow-hidden">
                    <div class="h-24 bg-gradient-to-r"
                         :class="user.rol === 'administrador' ? 'from-info-500 to-info-700' :
                                 user.rol === 'operador' ? 'from-warning-400 to-warning-600' :
                                 user.rol === 'titulado' ? 'from-emi-navy-500 to-emi-navy-700' :
                                 'from-emi-gold to-yellow-600'"
                    ></div>
                    <div class="px-6 pb-6 -mt-12">
                        <div class="flex flex-col sm:flex-row sm:items-end gap-4">
                            <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center font-bold text-3xl shadow-lg border-4 border-white"
                                 :class="user.rol === 'administrador' ? 'text-info-600' :
                                         user.rol === 'operador' ? 'text-warning-600' :
                                         user.rol === 'titulado' ? 'text-emi-navy-600' :
                                         'text-emi-gold'"
                            >
                                {{ (user.nombre_completo || user.email).charAt(0).toUpperCase() }}
                            </div>
                            <div class="flex-1">
                                <h2 class="text-2xl font-bold text-slate-800">{{ user.nombre_completo || 'Sin nombre' }}</h2>
                                <p class="text-slate-500 text-sm mt-0.5">{{ user.email }}</p>
                            </div>
                            <span class="badge-rol badge-rol-default self-start sm:self-auto" :data-rol="user.rol">
                                {{ user.rol }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Stats Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <!-- Rol -->
                    <div class="card-emi p-5">
                        <div class="flex items-center gap-3 mb-2">
                            <div class="w-9 h-9 rounded-lg flex items-center justify-center"
                                 :class="user.rol === 'administrador' ? 'bg-info-100' :
                                         user.rol === 'operador' ? 'bg-warning-100' :
                                         user.rol === 'titulado' ? 'bg-emi-navy-100' :
                                         'bg-yellow-100'"
                            >
                                <svg class="w-5 h-5"
                                     :class="user.rol === 'administrador' ? 'text-info-600' :
                                             user.rol === 'operador' ? 'text-warning-600' :
                                             user.rol === 'titulado' ? 'text-emi-navy-600' :
                                             'text-emi-gold'"
                                     fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </div>
                            <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Tipo de Cuenta</span>
                        </div>
                        <p class="text-lg font-bold text-slate-800 capitalize">{{ user.rol }}</p>
                    </div>

                    <!-- Fecha Registro -->
                    <div class="card-emi p-5">
                        <div class="flex items-center gap-3 mb-2">
                            <div class="w-9 h-9 bg-success-100 rounded-lg flex items-center justify-center">
                                <svg class="w-5 h-5 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            </div>
                            <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Registrado</span>
                        </div>
                        <p class="text-lg font-bold text-slate-800">{{ formatDate(user.created_at) }}</p>
                    </div>

                    <!-- Estado Perfil -->
                    <div class="card-emi p-5">
                        <div class="flex items-center gap-3 mb-2">
                            <div class="w-9 h-9 rounded-lg flex items-center justify-center"
                                 :class="user.tiene_perfil ? (user.perfil_completo ? 'bg-success-100' : 'bg-warning-100') : 'bg-slate-100'"
                            >
                                <svg class="w-5 h-5"
                                     :class="user.tiene_perfil ? (user.perfil_completo ? 'text-success-600' : 'text-warning-600') : 'text-slate-400'"
                                     fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <span class="text-xs text-slate-400 uppercase tracking-wider font-medium">Perfil</span>
                        </div>
                        <template v-if="user.rol !== 'administrador'">
                            <div v-if="user.tiene_perfil">
                                <div class="flex items-center gap-2 mb-1">
                                    <p class="text-lg font-bold text-slate-800">{{ Math.round(user.completeness_score * 100) }}%</p>
                                    <span class="text-xs font-medium"
                                          :class="user.perfil_completo ? 'text-success-600' : 'text-warning-600'"
                                    >{{ user.perfil_completo ? 'Completo' : 'En progreso' }}</span>
                                </div>
                                <div class="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                                    <div class="h-full rounded-full transition-all duration-500"
                                         :class="user.perfil_completo ? 'bg-success-500' : 'bg-warning-500'"
                                         :style="{ width: `${user.completeness_score * 100}%` }"
                                    ></div>
                                </div>
                            </div>
                            <p v-else class="text-lg font-bold text-slate-400">Sin perfil</p>
                        </template>
                        <p v-else class="text-lg font-bold text-slate-400">N/A</p>
                    </div>
                </div>

                <!-- Informacion de Cuenta Card -->
                <div class="card-emi p-6">
                    <div class="flex justify-between items-center mb-5">
                        <h2 class="text-lg font-semibold text-slate-800 flex items-center gap-2">
                            <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            Informacion de Cuenta
                        </h2>
                        <button
                            @click="toggleEdit"
                            class="px-3 py-1.5 text-sm text-emi-navy-500 hover:text-emi-gold transition-colors font-medium border border-transparent hover:border-emi-gold rounded-lg"
                        >
                            {{ isEditing ? 'Cancelar' : 'Editar' }}
                        </button>
                    </div>

                    <div v-if="!isEditing">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-5">
                            <div>
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">Nombre Completo</span>
                                <span class="text-slate-800 font-medium">{{ user.nombre_completo || 'Sin nombre' }}</span>
                            </div>
                            <div>
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">Correo Electronico</span>
                                <span class="text-slate-800 font-medium">{{ user.email }}</span>
                            </div>
                            <div>
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">Rol Asignado</span>
                                <span class="badge-rol badge-rol-default" :data-rol="user.rol">
                                    {{ user.rol }}
                                </span>
                            </div>
                            <div>
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">Fecha de Registro</span>
                                <span class="text-slate-800 font-medium">{{ formatDate(user.created_at, true) }}</span>
                            </div>
                            <div v-if="user.cv_uploaded_at">
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">CV Subido</span>
                                <span class="text-slate-800 font-medium">{{ formatDate(user.cv_uploaded_at, true) }}</span>
                            </div>
                            <div>
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">ID de Usuario</span>
                                <span class="text-slate-500 font-mono text-xs">{{ user.id }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Edit Form -->
                    <form v-else @submit.prevent="saveChanges" class="space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-1">Nombre Completo</label>
                                <input
                                    v-model="editForm.nombre_completo"
                                    type="text"
                                    class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-1">Rol</label>
                                <select
                                    v-model="editForm.rol"
                                    class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                >
                                    <optgroup label="Roles del sistema">
                                        <option v-for="role in FIXED_ROLES" :key="role.value" :value="role.value">
                                            {{ role.label }}
                                        </option>
                                    </optgroup>
                                    <optgroup v-if="customRoles.length" label="Roles personalizados">
                                        <option v-for="r in customRoles" :key="r.nombre" :value="r.nombre">
                                            {{ r.nombre }}
                                        </option>
                                    </optgroup>
                                </select>
                            </div>
                        </div>

                        <div class="pt-2 flex gap-2 justify-end">
                            <button
                                type="button"
                                @click="toggleEdit"
                                class="px-4 py-2 text-slate-600 hover:text-slate-800 font-medium text-sm"
                            >
                                Cancelar
                            </button>
                            <button
                                type="submit"
                                :disabled="saving"
                                class="btn-emi-primary font-medium text-sm"
                            >
                                {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    <!-- Modal Eliminar Usuario -->
    <Teleport to="body">
        <div
            v-if="showDeleteModal"
            class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4"
            @click.self="showDeleteModal = false"
        >
            <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
                <div class="flex items-center gap-3 mb-4">
                    <div class="flex-shrink-0 w-10 h-10 bg-danger-100 rounded-full flex items-center justify-center">
                        <svg class="w-5 h-5 text-danger-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold text-slate-800">Eliminar Cuenta</h3>
                </div>
                <p class="text-slate-600 mb-2">
                    Estas a punto de eliminar la cuenta de
                    <span class="font-semibold text-slate-800">{{ user?.nombre_completo || user?.email }}</span>.
                </p>
                <p class="text-sm text-danger-600 bg-danger-50 rounded-lg px-3 py-2 mb-4">
                    Esta accion es irreversible. El usuario y todos sus datos seran eliminados.
                </p>
                <p v-if="deleteError" class="text-sm text-danger-700 bg-danger-50 border border-danger-200 rounded px-3 py-2 mb-4">
                    {{ deleteError }}
                </p>
                <div class="flex gap-3 justify-end">
                    <button
                        @click="showDeleteModal = false"
                        class="px-4 py-2 text-slate-600 hover:text-slate-800 font-medium"
                    >
                        Cancelar
                    </button>
                    <button
                        @click="confirmDeleteUser"
                        class="px-4 py-2 bg-danger-600 text-white rounded-lg hover:bg-danger-700 font-medium"
                    >
                        Eliminar cuenta
                    </button>
                </div>
            </div>
        </div>
    </Teleport>
    </AppLayout>
</template>
