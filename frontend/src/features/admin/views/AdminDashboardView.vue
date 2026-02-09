<script setup>
/**
 * AdminDashboardView - Fase 7 + Rediseno EMI
 * Dashboard administrativo con identidad corporativa EMI
 */

import { ref, onMounted, computed } from 'vue'
import { useAdminProfilesStore } from '@/features/admin/store/adminProfiles.store'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { useRouter } from 'vue-router'
import { getModelInfo } from '@/shared/api/ml.api'
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'
import AppLayout from '@/shared/components/AppLayout.vue'

const adminProfilesStore = useAdminProfilesStore()
const authStore = useAuthStore()
const router = useRouter()

// Estado local
const stats = ref({
    totalProfiles: 0,
    activeProfiles: 0,
    sectors: []
})

const modelInfo = ref(null)

// Cargar datos al montar
onMounted(async () => {
    // Verificar admin
    if (!authStore.isAdmin) {
        router.push('/dashboard')
        return
    }

    try {
        // Cargar perfiles
        await adminProfilesStore.loadProfiles(true) // Incluir inactivos

        // Cargar sectores
        await adminProfilesStore.loadSectors()
        
        // Cargar info del modelo
        modelInfo.value = await getModelInfo()

        // Calcular stats
        stats.value.totalProfiles = adminProfilesStore.profiles.length
        stats.value.activeProfiles = adminProfilesStore.profiles.filter(p => p.is_active).length
        stats.value.sectors = adminProfilesStore.sectors
    } catch (error) {
        console.error('Error cargando dashboard:', error)
    }
})

// Computed
const modelStatus = computed(() => {
    if (!modelInfo.value) return 'Cargando...'
    return modelInfo.value.is_ready ? 'Activo' : 'Inactivo'
})

const modelMetrics = computed(() => {
    return modelInfo.value?.training_metrics || {}
})
</script>

<template>
    <AppLayout>
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Header -->
            <div class="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 class="text-3xl font-bold text-emi-navy-500">Panel de Administracion</h1>
                    <p class="mt-2 text-gray-600">
                        Vista general del sistema de Machine Learning
                    </p>
                </div>
                <div class="flex gap-3">
                    <router-link
                        to="/admin/profiles/new"
                        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
                    >
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        Nueva Institucion
                    </router-link>
                </div>
            </div>

            <!-- Stats Cards (Mobile) -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <!-- Modelo ML -->
                <Card :hoverable="true" padding="p-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-xs text-gray-500 uppercase tracking-wider">Modelo</p>
                            <p class="text-xl font-bold mt-1 text-red-600">
                                {{ modelStatus }}
                            </p>
                        </div>
                        <div class="p-2 rounded-full bg-red-100">
                            <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                        </div>
                    </div>
                </Card>

                <!-- Perfiles Totales -->
                <Card :hoverable="true" padding="p-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-xs text-gray-500 uppercase tracking-wider">Perfiles</p>
                            <p class="text-xl font-bold text-emi-navy-500 mt-1">
                                {{ stats.totalProfiles }}
                            </p>
                        </div>
                        <div class="p-2 rounded-full bg-emi-navy-100">
                            <svg class="w-5 h-5 text-emi-navy-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                        </div>
                    </div>
                </Card>

                <!-- Perfiles Activos -->
                <Card :hoverable="true" padding="p-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-xs text-gray-500 uppercase tracking-wider">Activos</p>
                            <p class="text-xl font-bold text-emi-gold-600 mt-1">
                                {{ stats.activeProfiles }}
                            </p>
                        </div>
                        <div class="p-2 rounded-full bg-emi-gold-100">
                            <svg class="w-5 h-5 text-emi-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                    </div>
                </Card>

                <!-- Sectores -->
                <Card :hoverable="true" padding="p-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-xs text-gray-500 uppercase tracking-wider">Sectores</p>
                            <p class="text-xl font-bold text-gray-700 mt-1">
                                {{ stats.sectors.length }}
                            </p>
                        </div>
                        <div class="p-2 rounded-full bg-gray-100">
                            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                            </svg>
                        </div>
                    </div>
                </Card>
            </div>

            <!-- Main Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Info del Modelo -->
                <Card title="Informacion del Modelo ML">
                    <div v-if="modelInfo" class="py-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <p class="text-xs text-gray-500 uppercase">Tipo</p>
                                <p class="font-semibold text-emi-navy-600">{{ modelInfo.model_type }}</p>
                            </div>
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <p class="text-xs text-gray-500 uppercase">Version</p>
                                <p class="font-semibold text-emi-navy-600">{{ modelInfo.model_version }}</p>
                            </div>
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <p class="text-xs text-gray-500 uppercase">R2 Score</p>
                                <p class="font-bold text-green-600">{{ modelMetrics.r2_score?.toFixed(3) || '-' }}</p>
                            </div>
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <p class="text-xs text-gray-500 uppercase">Accuracy</p>
                                <p class="font-bold text-blue-600">{{ modelMetrics.accuracy ? (modelMetrics.accuracy * 100).toFixed(1) + '%' : '-' }}</p>
                            </div>
                        </div>
                        <div class="mt-4 text-center">
                            <Badge :variant="modelInfo.is_ready ? 'success' : 'warning'">
                                {{ modelInfo.status }}
                            </Badge>
                        </div>
                    </div>
                    <div v-else class="text-center py-8">
                        <p class="text-gray-400">Cargando informacion del modelo...</p>
                    </div>
                </Card>
            </div>
        </div>
    </AppLayout>
</template>
