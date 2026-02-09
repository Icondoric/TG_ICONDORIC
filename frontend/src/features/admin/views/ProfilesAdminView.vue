<script setup>
/**
 * ProfilesAdminView - Fase 7
 * Vista administrativa para gestionar perfiles institucionales
 */

import { ref, onMounted, computed } from 'vue'
import { useAdminProfilesStore } from '@/features/admin/store/adminProfiles.store'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { useRouter } from 'vue-router'
import AppLayout from '@/shared/components/AppLayout.vue'

const adminProfilesStore = useAdminProfilesStore()
const authStore = useAuthStore()
const router = useRouter()

// Estado local
const includeInactive = ref(false)
const selectedSector = ref('')
const searchQuery = ref('')
const deleteConfirm = ref(null)

// Cargar al montar
onMounted(async () => {
    if (!authStore.isAdminOrOperator) {
        router.push('/dashboard')
        return
    }

    await loadProfiles()
    await adminProfilesStore.loadSectors()
})

// Computed
const filteredProfiles = computed(() => {
    let profiles = adminProfilesStore.profiles

    // Filtrar por sector
    if (selectedSector.value) {
        profiles = profiles.filter(p => p.sector === selectedSector.value)
    }

    // Filtrar por busqueda
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        profiles = profiles.filter(p =>
            p.institution_name.toLowerCase().includes(query) ||
            p.sector.toLowerCase().includes(query)
        )
    }

    return profiles
})

// Methods
const loadProfiles = async () => {
    try {
        await adminProfilesStore.loadProfiles(includeInactive.value, selectedSector.value || null)
    } catch (error) {
        console.error('Error cargando perfiles:', error)
    }
}

const toggleInactive = async () => {
    includeInactive.value = !includeInactive.value
    await loadProfiles()
}

const filterBySector = async () => {
    await loadProfiles()
}

const editProfile = (profileId) => {
    router.push(`/admin/profiles/${profileId}/edit`)
}

const confirmDelete = (profile) => {
    deleteConfirm.value = profile
}

const cancelDelete = () => {
    deleteConfirm.value = null
}

const deleteProfile = async () => {
    if (!deleteConfirm.value) return

    try {
        await adminProfilesStore.deleteProfileAction(deleteConfirm.value.id)
        deleteConfirm.value = null
    } catch (error) {
        console.error('Error eliminando perfil:', error)
    }
}

const activateProfile = async (profileId) => {
    try {
        await adminProfilesStore.activateProfileAction(profileId)
    } catch (error) {
        console.error('Error activando perfil:', error)
    }
}

// Helpers
const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

const formatWeights = (weights) => {
    if (!weights) return 'N/A'
    return Object.entries(weights)
        .map(([key, val]) => `${key.replace('_', ' ')}: ${Math.round(val * 100)}%`)
        .join(', ')
}
</script>

<template>
    <AppLayout>
        <div class="py-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <!-- Header -->
            <header class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 class="text-3xl font-bold text-slate-800">Perfiles Institucionales</h1>
                    <p class="mt-1 text-slate-600">
                        Gestiona los perfiles de las instituciones para el matching de CVs
                    </p>
                </div>
                <router-link
                    to="/admin/profiles/new"
                    class="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    Nuevo Perfil
                </router-link>
            </header>

            <!-- Filtros -->
            <div class="bg-white rounded-xl shadow-md p-4 mb-6">
                <div class="flex flex-col md:flex-row gap-4">
                    <!-- Busqueda -->
                    <div class="flex-1">
                        <input
                            v-model="searchQuery"
                            type="text"
                            placeholder="Buscar por nombre o sector..."
                            class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    <!-- Filtro Sector -->
                    <div>
                        <select
                            v-model="selectedSector"
                            @change="filterBySector"
                            class="px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">Todos los sectores</option>
                            <option v-for="sector in adminProfilesStore.sectors" :key="sector" :value="sector">
                                {{ sector }}
                            </option>
                        </select>
                    </div>

                    <!-- Toggle Inactivos -->
                    <button
                        @click="toggleInactive"
                        :class="[
                            'px-4 py-2 rounded-lg border font-medium transition-colors',
                            includeInactive
                                ? 'bg-slate-100 border-slate-300 text-slate-700'
                                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                        ]"
                    >
                        {{ includeInactive ? 'Ocultando inactivos' : 'Mostrando todos' }}
                    </button>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="adminProfilesStore.isLoadingProfiles" class="bg-white rounded-xl shadow-md p-8 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-slate-500">Cargando perfiles...</p>
            </div>

            <!-- Error -->
            <div v-else-if="adminProfilesStore.profilesError" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p class="text-red-700">{{ adminProfilesStore.profilesError }}</p>
            </div>

            <!-- Lista de Perfiles -->
            <div v-else class="space-y-4">
                <!-- Stats -->
                <div class="text-sm text-slate-500 mb-2">
                    Mostrando {{ filteredProfiles.length }} de {{ adminProfilesStore.profiles.length }} perfiles
                </div>

                <!-- Sin resultados -->
                <div v-if="filteredProfiles.length === 0" class="bg-white rounded-xl shadow-md p-8 text-center">
                    <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <h3 class="text-lg font-medium text-slate-600">No hay perfiles</h3>
                    <p class="text-sm text-slate-400 mt-2">
                        Crea el primer perfil institucional para comenzar
                    </p>
                </div>

                <!-- Cards de Perfiles -->
                <div
                    v-for="profile in filteredProfiles"
                    :key="profile.id"
                    :class="[
                        'bg-white rounded-xl shadow-md p-6 transition-all',
                        !profile.is_active && 'opacity-60'
                    ]"
                >
                    <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                        <!-- Info Principal -->
                        <div class="flex-1">
                            <div class="flex items-center gap-3">
                                <h3 class="text-lg font-semibold text-slate-800">
                                    {{ profile.institution_name }}
                                </h3>
                                <span
                                    :class="[
                                        'px-2 py-1 text-xs font-medium rounded-full',
                                        profile.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                    ]"
                                >
                                    {{ profile.is_active ? 'Activo' : 'Inactivo' }}
                                </span>
                            </div>
                            <p class="text-sm text-slate-500 mt-1">{{ profile.sector }}</p>
                            <p v-if="profile.description" class="text-sm text-slate-600 mt-2">
                                {{ profile.description }}
                            </p>

                            <!-- Detalles -->
                            <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                <!-- Pesos -->
                                <div>
                                    <p class="text-slate-400">Umbral Apto</p>
                                    <p class="font-medium text-slate-700">
                                        {{ Math.round((profile.thresholds?.apto || 0.7) * 100) }}%
                                    </p>
                                </div>
                                <div>
                                    <p class="text-slate-400">Umbral Considerado</p>
                                    <p class="font-medium text-slate-700">
                                        {{ Math.round((profile.thresholds?.considerado || 0.5) * 100) }}%
                                    </p>
                                </div>
                                <div>
                                    <p class="text-slate-400">Creado</p>
                                    <p class="font-medium text-slate-700">
                                        {{ formatDate(profile.created_at) }}
                                    </p>
                                </div>
                                <div>
                                    <p class="text-slate-400">Actualizado</p>
                                    <p class="font-medium text-slate-700">
                                        {{ formatDate(profile.updated_at) }}
                                    </p>
                                </div>
                            </div>

                            <!-- Pesos -->
                            <div v-if="profile.weights" class="mt-4">
                                <p class="text-xs text-slate-400 mb-2">Pesos de evaluacion:</p>
                                <div class="flex flex-wrap gap-2">
                                    <span
                                        v-for="(weight, key) in profile.weights"
                                        :key="key"
                                        class="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs"
                                    >
                                        {{ key.replace('_', ' ') }}: {{ Math.round(weight * 100) }}%
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Acciones -->
                        <div class="flex md:flex-col gap-2">
                            <button
                                @click="editProfile(profile.id)"
                                class="flex-1 md:flex-none px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors text-sm font-medium"
                            >
                                Editar
                            </button>
                            <button
                                v-if="profile.is_active"
                                @click="confirmDelete(profile)"
                                class="flex-1 md:flex-none px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm font-medium"
                            >
                                Desactivar
                            </button>
                            <button
                                v-else
                                @click="activateProfile(profile.id)"
                                class="flex-1 md:flex-none px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm font-medium"
                            >
                                Activar
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal de Confirmacion de Eliminacion -->
            <Teleport to="body">
                <div
                    v-if="deleteConfirm"
                    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
                    @click.self="cancelDelete"
                >
                    <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
                        <h3 class="text-lg font-semibold text-slate-800 mb-2">
                            Confirmar Desactivacion
                        </h3>
                        <p class="text-slate-600 mb-6">
                            ¿Estas seguro de que deseas desactivar el perfil
                            <span class="font-semibold">{{ deleteConfirm.institution_name }}</span>?
                            El perfil no sera eliminado permanentemente.
                        </p>
                        <div class="flex gap-3 justify-end">
                            <button
                                @click="cancelDelete"
                                class="px-4 py-2 text-slate-600 hover:text-slate-800 font-medium"
                            >
                                Cancelar
                            </button>
                            <button
                                @click="deleteProfile"
                                class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium"
                            >
                                Desactivar
                            </button>
                        </div>
                    </div>
                </div>
            </Teleport>
        </div>
    </AppLayout>
</template>
