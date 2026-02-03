<script setup>
/**
 * AdminDashboardView - Fase 7 + Rediseno EMI
 * Dashboard administrativo con identidad corporativa EMI
 */

import { ref, onMounted, computed } from 'vue'
import { useMLStore } from '../../stores/ml'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'
import Card from '../../components/ui/Card.vue'
import Badge from '../../components/ui/Badge.vue'
import ProgressBar from '../../components/ui/ProgressBar.vue'
import AdminLayout from '../../components/admin/AdminLayout.vue'

const mlStore = useMLStore()
const authStore = useAuthStore()
const router = useRouter()

// Estado local
const stats = ref({
    totalProfiles: 0,
    activeProfiles: 0,
    sectors: []
})

// Cargar datos al montar
onMounted(async () => {
    // Verificar admin
    if (!authStore.isAdmin) {
        router.push('/dashboard')
        return
    }

    try {
        // Cargar info del modelo
        await mlStore.loadModelInfo()

        // Cargar perfiles
        await mlStore.loadProfiles(true) // Incluir inactivos

        // Cargar sectores
        await mlStore.loadSectors()

        // Calcular stats
        stats.value.totalProfiles = mlStore.profiles.length
        stats.value.activeProfiles = mlStore.profiles.filter(p => p.is_active).length
        stats.value.sectors = mlStore.sectors
    } catch (error) {
        console.error('Error cargando dashboard:', error)
    }
})

// Computed
const modelStatus = computed(() => {
    if (!mlStore.modelInfo) return 'Desconocido'
    return mlStore.isModelReady ? 'Activo' : 'Inactivo'
})

const modelMetrics = computed(() => {
    return mlStore.modelInfo?.training_metrics || {}
})
</script>

<template>
    <AdminLayout>
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Header -->
            <div class="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 class="text-3xl font-bold text-emi-navy-500">Panel de Administración</h1>
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
                        Nueva Institución
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
                            <p class="text-xl font-bold mt-1" :class="mlStore.isModelReady ? 'text-emi-gold-600' : 'text-red-600'">
                                {{ modelStatus }}
                            </p>
                        </div>
                        <div :class="['p-2 rounded-full', mlStore.isModelReady ? 'bg-emi-gold-100' : 'bg-red-100']">
                            <svg class="w-5 h-5" :class="mlStore.isModelReady ? 'text-emi-gold-600' : 'text-red-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                <Card title="Información del Modelo ML">
                    <div v-if="mlStore.modelInfo" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="p-3 bg-gray-50 rounded-lg">
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Tipo</p>
                                <p class="font-semibold text-gray-900 mt-1">{{ mlStore.modelInfo.model_type || 'Ridge' }}</p>
                            </div>
                            <div class="p-3 bg-gray-50 rounded-lg">
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Versión</p>
                                <p class="font-semibold text-gray-900 mt-1">{{ mlStore.modelInfo.version || 'v1' }}</p>
                            </div>
                            <div class="p-3 bg-gray-50 rounded-lg">
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Alpha</p>
                                <p class="font-semibold text-gray-900 mt-1">{{ mlStore.modelInfo.alpha || 'N/A' }}</p>
                            </div>
                            <div class="p-3 bg-gray-50 rounded-lg">
                                <p class="text-xs text-gray-500 uppercase tracking-wider">Features</p>
                                <p class="font-semibold text-gray-900 mt-1">{{ mlStore.modelInfo.n_features || '18' }}</p>
                            </div>
                        </div>

                        <!-- Métricas -->
                        <div v-if="Object.keys(modelMetrics).length > 0" class="border-t border-gray-100 pt-4">
                            <h3 class="text-sm font-semibold text-gray-700 mb-4">Métricas de Entrenamiento</h3>
                            <div class="grid grid-cols-2 gap-3">
                                <div
                                    v-if="modelMetrics.r2_score !== undefined"
                                    class="p-3 bg-emi-navy-50 rounded-lg cursor-help hover:bg-emi-navy-100 transition-colors"
                                    title="R2 (Coeficiente de Determinación): Indica que tan confiable es el modelo (0-100%). Más alto es mejor."
                                >
                                    <div class="flex items-center gap-1 mb-1">
                                        <p class="text-xs text-emi-navy-600 uppercase tracking-wider">R2 Score</p>
                                    </div>
                                    <p class="text-xl font-bold text-emi-navy-600">
                                        {{ (modelMetrics.r2_score * 100).toFixed(1) }}%
                                    </p>
                                </div>
                                <div
                                    v-if="modelMetrics.rmse !== undefined"
                                    class="p-3 bg-emi-gold-50 rounded-lg cursor-help hover:bg-emi-gold-100 transition-colors"
                                    title="RMSE (Raiz del Error Cuadratico Medio): Margen de error promedio del modelo. Más bajo es mejor."
                                >
                                    <div class="flex items-center gap-1 mb-1">
                                        <p class="text-xs text-emi-gold-700 uppercase tracking-wider">RMSE</p>
                                    </div>
                                    <p class="text-xl font-bold text-emi-gold-600">
                                        {{ modelMetrics.rmse.toFixed(4) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-else class="text-center py-8">
                        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500 mx-auto mb-4"></div>
                        <p class="text-gray-400">Cargando información del modelo...</p>
                    </div>
                </Card>
            </div>
        </div>
    </AdminLayout>
</template>
