<script setup>
/**
 * UserDetailView - Fase 7+
 * Vista para ver y editar detalles de un usuario especifico
 */
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUsersStore } from '../../stores/users'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const router = useRouter()
const usersStore = useUsersStore()
const authStore = useAuthStore()

const userId = route.params.id
const isEditing = ref(false)
const saving = ref(false)

const editForm = ref({
    nombre_completo: '',
    rol: ''
})

const ROLES = [
    { value: 'estudiante', label: 'Estudiante' },
    { value: 'titulado', label: 'Titulado' },
    { value: 'administrador', label: 'Administrador' }
]

onMounted(async () => {
    if (!authStore.isAdmin) {
        router.push('/dashboard')
        return
    }
    
    try {
        await usersStore.fetchUser(userId)
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
        await usersStore.updateUser(userId, editForm.value)
        isEditing.value = false
    } catch (error) {
        console.error('Error saving user:', error)
    } finally {
        saving.value = false
    }
}

const deleteUser = async () => {
    if (!confirm('¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.')) {
        return
    }
    
    try {
        await usersStore.deleteUser(userId)
        router.push('/admin/users')
    } catch (error) {
        alert('Error eliminando usuario')
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
    <div class="max-w-7xl mx-auto py-8 px-4">
        <!-- Header -->
        <header class="mb-6">
            <button 
                @click="router.push('/admin/users')"
                class="flex items-center text-slate-500 hover:text-slate-800 mb-2 text-sm font-medium transition-colors"
            >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                Volver a Usuarios
            </button>
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <h1 class="text-3xl font-bold text-slate-800">Detalle de Usuario</h1>
                
                <div class="flex gap-2" v-if="user && user.id !== authStore.user?.user_id">
                    <button 
                        @click="deleteUser"
                        class="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors font-medium border border-red-100"
                    >
                        Eliminar Cuenta
                    </button>
                </div>
            </div>
        </header>

        <!-- Loading -->
        <div v-if="usersStore.loading && !user" class="bg-white rounded-xl shadow-md p-12 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-4 text-slate-500">Cargando datos...</p>
        </div>

        <!-- Error -->
        <div v-else-if="usersStore.error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p class="text-red-700">{{ usersStore.error }}</p>
        </div>

        <!-- Content -->
        <div v-else-if="user" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Left Column: User Info -->
            <div class="lg:col-span-1 space-y-6">
                <!-- User Card -->
                <div class="bg-white rounded-xl shadow-md p-6">
                    <div class="flex justify-between items-start mb-4">
                         <h2 class="text-lg font-semibold text-slate-800">Información de Cuenta</h2>
                         <button 
                            @click="toggleEdit"
                            class="text-sm text-blue-600 hover:text-blue-800 font-medium"
                         >
                            {{ isEditing ? 'Cancelar' : 'Editar' }}
                         </button>
                    </div>

                    <div v-if="!isEditing" class="space-y-4">
                        <div class="flex items-center gap-4">
                            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-2xl">
                                {{ (user.nombre_completo || user.email).charAt(0).toUpperCase() }}
                            </div>
                            <div>
                                <h3 class="font-bold text-slate-800 text-lg">{{ user.nombre_completo || 'Sin nombre' }}</h3>
                                <p class="text-slate-500 text-sm">{{ user.email }}</p>
                            </div>
                        </div>

                        <div class="pt-4 border-t border-slate-100 space-y-3">
                            <div>
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">Rol</span>
                                <span :class="[
                                    'px-2.5 py-1 rounded-full text-xs font-medium capitalize',
                                    user.rol === 'administrador' ? 'bg-purple-100 text-purple-700' :
                                    user.rol === 'titulado' ? 'bg-indigo-100 text-indigo-700' :
                                    'bg-blue-100 text-blue-700'
                                ]">
                                    {{ user.rol }}
                                </span>
                            </div>
                            
                            <div>
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">Registrado el</span>
                                <span class="text-slate-700 text-sm">{{ formatDate(user.created_at, true) }}</span>
                            </div>

                            <div v-if="user.rol !== 'administrador'">
                                <span class="text-xs text-slate-400 block uppercase tracking-wider mb-1">Estado Perfil</span>
                                <div v-if="user.tiene_perfil" class="flex items-center gap-2">
                                    <div class="w-full max-w-[120px] bg-slate-200 rounded-full h-2 overflow-hidden">
                                        <div 
                                            class="h-full rounded-full" 
                                            :class="user.perfil_completo ? 'bg-green-500' : 'bg-yellow-500'"
                                            :style="{ width: `${user.completeness_score * 100}%` }"
                                        ></div>
                                    </div>
                                    <span class="text-xs text-slate-600 font-medium">
                                        {{ Math.round(user.completeness_score * 100) }}%
                                    </span>
                                </div>
                                <span v-else class="text-sm text-slate-500 italic">No ha iniciado perfil</span>
                            </div>
                        </div>
                    </div>

                    <!-- Edit Form -->
                    <form v-else @submit.prevent="saveChanges" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Nombre Completo</label>
                            <input 
                                v-model="editForm.nombre_completo"
                                type="text"
                                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>
                         <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Rol</label>
                            <select 
                                v-model="editForm.rol"
                                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option v-for="role in ROLES" :key="role.value" :value="role.value">
                                    {{ role.label }}
                                </option>
                            </select>
                        </div>
                        
                        <div class="pt-2 flex gap-2">
                            <button 
                                type="submit" 
                                :disabled="saving"
                                class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium text-sm"
                            >
                                {{ saving ? 'Guardando...' : 'Guardar' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Right Column: Profile Details -->
            <div class="lg:col-span-2 space-y-6">
                
                <!-- If Profile Exists -->
                <template v-if="hasProfile">
                    <!-- Stats / Skills Summary -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Hard Skills -->
                        <div class="bg-white rounded-xl shadow-md p-6">
                            <h3 class="font-semibold text-slate-800 mb-4 flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                                Habilidades Técnicas
                            </h3>
                            <div v-if="profile.hard_skills && profile.hard_skills.length > 0" class="flex flex-wrap gap-2">
                                <span 
                                    v-for="skill in profile.hard_skills" 
                                    :key="skill"
                                    class="px-2.5 py-1 bg-blue-50 text-blue-700 rounded-md text-sm font-medium"
                                >
                                    {{ skill }}
                                </span>
                            </div>
                            <p v-else class="text-slate-400 italic text-sm">No se han registrado habilidades técnicas.</p>
                        </div>

                         <!-- Soft Skills -->
                         <div class="bg-white rounded-xl shadow-md p-6">
                            <h3 class="font-semibold text-slate-800 mb-4 flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full bg-green-500"></span>
                                Habilidades Blandas
                            </h3>
                            <div v-if="profile.soft_skills && profile.soft_skills.length > 0" class="flex flex-wrap gap-2">
                                <span 
                                    v-for="skill in profile.soft_skills" 
                                    :key="skill"
                                    class="px-2.5 py-1 bg-green-50 text-green-700 rounded-md text-sm font-medium"
                                >
                                    {{ skill }}
                                </span>
                            </div>
                            <p v-else class="text-slate-400 italic text-sm">No se han registrado habilidades blandas.</p>
                        </div>
                    </div>

                    <!-- Education & Experience -->
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <h3 class="font-semibold text-slate-800 mb-6 pb-2 border-b border-slate-100">
                             Perfil Profesional
                        </h3>
                        
                        <div class="space-y-6">
                            <!-- Education Level -->
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <h4 class="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">Nivel Educativo</h4>
                                    <p class="text-slate-800 font-medium text-lg">
                                        {{ profile.education_level || 'No especificado' }}
                                    </p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">Experiencia Laboral</h4>
                                    <p class="text-slate-800 font-medium text-lg">
                                        {{ profile.experience_years }} años
                                    </p>
                                </div>
                            </div>
                            
                            <!-- Languages -->
                            <div>
                                <h4 class="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">Idiomas</h4>
                                <div v-if="profile.languages && profile.languages.length > 0" class="flex flex-wrap gap-2">
                                    <span v-for="lang in profile.languages" :key="lang" class="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm">
                                        {{ lang }}
                                    </span>
                                </div>
                                <p v-else class="text-slate-500 italic">No especificado</p>
                            </div>
                            
                            <!-- Detailed Lists from CV (if available) -->
                            <div v-if="profile.gemini_extraction?.education?.length > 0">
                                <h4 class="text-sm font-medium text-slate-500 uppercase tracking-wider mb-3 mt-6">Formación Académica (CV)</h4>
                                <ul class="space-y-3">
                                    <li v-for="(edu, idx) in profile.gemini_extraction.education" :key="idx" class="flex gap-3 text-sm">
                                        <div class="min-w-[4px] bg-slate-200 rounded-full my-1"></div>
                                        <div>
                                            <p class="font-semibold text-slate-800">{{ edu.degree }}</p>
                                            <p class="text-slate-600">{{ edu.institution }}</p>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                            
                            <div v-if="profile.gemini_extraction?.experience?.length > 0">
                                <h4 class="text-sm font-medium text-slate-500 uppercase tracking-wider mb-3 mt-6">Experiencia Laboral (CV)</h4>
                                <ul class="space-y-4">
                                    <li v-for="(exp, idx) in profile.gemini_extraction.experience" :key="idx" class="text-sm bg-slate-50 p-3 rounded-lg border border-slate-100">
                                        <p class="font-semibold text-slate-800">{{ exp.role }}</p>
                                        <div class="flex justify-between items-center mt-1 mb-2">
                                            <p class="text-blue-600 font-medium text-xs">{{ exp.company }}</p>
                                            <p class="text-slate-500 text-xs">{{ exp.duration }}</p>
                                        </div>
                                        <p v-if="exp.description" class="text-slate-600 text-xs leading-relaxed">
                                            {{ exp.description }}
                                        </p>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- CV File Info -->
                         <div class="mt-8 pt-4 border-t border-slate-100 flex justify-between items-center text-xs text-slate-400">
                            <span>Archivo CV: {{ profile.cv_filename || 'No disponible' }}</span>
                            <span v-if="profile.cv_uploaded_at">Subido el {{ formatDate(profile.cv_uploaded_at, true) }}</span>
                        </div>
                    </div>
                </template>

                 <!-- No Profile Msg -->
                 <div v-else-if="user.rol !== 'administrador'" class="bg-white rounded-xl shadow-md p-12 text-center border-2 border-dashed border-slate-200">
                    <div class="w-16 h-16 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                    </div>
                    <h3 class="text-lg font-medium text-slate-600">Este usuario aún no ha completado su perfil</h3>
                    <p class="text-slate-400 mt-2 max-w-sm mx-auto">
                        El usuario debe iniciar sesión y completar su perfil o subir su CV para que aparezca información aquí.
                    </p>
                </div>
                 
                 <!-- Admin Msg -->
                 <div v-else class="bg-white rounded-xl shadow-md p-8 text-center bg-purple-50 border border-purple-100">
                    <p class="text-purple-700 font-medium">Las cuentas de administrador no tienen perfil profesional asociado.</p>
                </div>
            </div>
        </div>
    </div>
</template>
