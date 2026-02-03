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
    <div class="dashboard-bg min-h-screen pt-16">
        <div class="flex">
            <!-- Sidebar -->
            <aside class="hidden lg:block fixed top-16 left-0 w-[280px] h-[calc(100vh-4rem)] bg-white border-r border-gray-200 overflow-y-auto">
                <div class="p-6">
                    <!-- Model Status -->
                    <div class="text-center mb-6">
                        <div
                            :class="[
                                'w-20 h-20 mx-auto rounded-full flex items-center justify-center',
                                mlStore.isModelReady ? 'bg-emi-gold-100' : 'bg-red-100'
                            ]"
                        >
                            <svg
                                :class="['w-10 h-10', mlStore.isModelReady ? 'text-emi-gold-600' : 'text-red-600']"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <p class="mt-3 font-semibold text-gray-900">Modelo ML</p>
                        <Badge :variant="mlStore.isModelReady ? 'gold' : 'danger'" class="mt-2">
                            {{ modelStatus }}
                        </Badge>
                    </div>

                    <!-- Quick Stats -->
                    <div class="space-y-3 mb-6">
                        <div class="flex justify-between items-center p-3 bg-emi-navy-50 rounded-lg">
                            <span class="text-sm text-gray-600">Perfiles Totales</span>
                            <Badge variant="navy">{{ stats.totalProfiles }}</Badge>
                        </div>
                        <div class="flex justify-between items-center p-3 bg-emi-gold-50 rounded-lg">
                            <span class="text-sm text-gray-600">Perfiles Activos</span>
                            <Badge variant="gold">{{ stats.activeProfiles }}</Badge>
                        </div>
                        <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                            <span class="text-sm text-gray-600">Sectores</span>
                            <Badge variant="neutral">{{ stats.sectors.length }}</Badge>
                        </div>
                    </div>

                    <!-- Quick Actions -->
                    <div class="space-y-2">
                        <router-link
                            to="/admin/profiles"
                            class="w-full flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-emi-navy-50 hover:text-emi-navy-600 rounded-lg transition-colors"
                        >
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                            <span class="font-medium">Gestionar Perfiles</span>
                        </router-link>
                        <router-link
                            to="/admin/users"
                            class="w-full flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-purple-50 hover:text-purple-600 rounded-lg transition-colors"
                        >
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                            </svg>
                            <span class="font-medium">Gestionar Usuarios</span>
                        </router-link>
                        <router-link
                            to="/admin/ofertas"
                            class="w-full flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-emi-gold-50 hover:text-emi-gold-600 rounded-lg transition-colors"
                        >
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            <span class="font-medium">Gestionar Ofertas</span>
                        </router-link>
                        <router-link
                            to="/admin/profiles/new"
                            class="w-full flex items-center gap-3 px-4 py-3 text-emi-gold-600 hover:bg-emi-gold-50 rounded-lg transition-colors"
                        >
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                            </svg>
                            <span class="font-medium">Nuevo Perfil</span>
                        </router-link>
                    </div>
                </div>
            </aside>

            <!-- Main Content -->
            <main class="flex-1 lg:ml-[280px]">
                <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <!-- Header -->
                    <div class="mb-8">
                        <h1 class="text-3xl font-bold text-emi-navy-500">Panel de Administracion</h1>
                        <p class="mt-2 text-gray-600">
                            Vista general del sistema de Machine Learning
                        </p>
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
                        <Card title="Informacion del Modelo ML">
                            <div v-if="mlStore.modelInfo" class="space-y-4">
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="p-3 bg-gray-50 rounded-lg">
                                        <p class="text-xs text-gray-500 uppercase tracking-wider">Tipo</p>
                                        <p class="font-semibold text-gray-900 mt-1">{{ mlStore.modelInfo.model_type || 'Ridge' }}</p>
                                    </div>
                                    <div class="p-3 bg-gray-50 rounded-lg">
                                        <p class="text-xs text-gray-500 uppercase tracking-wider">Version</p>
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

                                <!-- Metricas -->
                                <div v-if="Object.keys(modelMetrics).length > 0" class="border-t border-gray-100 pt-4">
                                    <h3 class="text-sm font-semibold text-gray-700 mb-4">Metricas de Entrenamiento</h3>
                                    <div class="grid grid-cols-2 gap-3">
                                        <div
                                            v-if="modelMetrics.r2_score !== undefined"
                                            class="p-3 bg-emi-navy-50 rounded-lg cursor-help hover:bg-emi-navy-100 transition-colors"
                                            title="R2 (Coeficiente de Determinacion): Indica que tan confiable es el modelo (0-100%). Mas alto es mejor."
                                        >
                                            <div class="flex items-center gap-1 mb-1">
                                                <p class="text-xs text-emi-navy-600 uppercase tracking-wider">R2 Score</p>
                                                <svg class="w-3 h-3 text-emi-navy-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                            </div>
                                            <p class="text-xl font-bold text-emi-navy-600">
                                                {{ (modelMetrics.r2_score * 100).toFixed(1) }}%
                                            </p>
                                        </div>
                                        <div
                                            v-if="modelMetrics.rmse !== undefined"
                                            class="p-3 bg-emi-gold-50 rounded-lg cursor-help hover:bg-emi-gold-100 transition-colors"
                                            title="RMSE (Raiz del Error Cuadratico Medio): Margen de error promedio del modelo. Mas bajo es mejor."
                                        >
                                            <div class="flex items-center gap-1 mb-1">
                                                <p class="text-xs text-emi-gold-700 uppercase tracking-wider">RMSE</p>
                                                <svg class="w-3 h-3 text-emi-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                            </div>
                                            <p class="text-xl font-bold text-emi-gold-600">
                                                {{ modelMetrics.rmse.toFixed(4) }}
                                            </p>
                                        </div>
                                        <div
                                            v-if="modelMetrics.mae !== undefined"
                                            class="p-3 bg-gray-50 rounded-lg cursor-help hover:bg-gray-100 transition-colors"
                                            title="MAE (Error Absoluto Medio): Desviacion promedio de las predicciones. Mas bajo es mejor."
                                        >
                                            <div class="flex items-center gap-1 mb-1">
                                                <p class="text-xs text-gray-600 uppercase tracking-wider">MAE</p>
                                                <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                            </div>
                                            <p class="text-xl font-bold text-gray-700">
                                                {{ modelMetrics.mae.toFixed(4) }}
                                            </p>
                                        </div>
                                        <div
                                            v-if="modelMetrics.accuracy !== undefined"
                                            class="p-3 bg-emi-navy-50 rounded-lg cursor-help hover:bg-emi-navy-100 transition-colors"
                                            title="Accuracy (Exactitud): Porcentaje global de aciertos del modelo."
                                        >
                                            <div class="flex items-center gap-1 mb-1">
                                                <p class="text-xs text-emi-navy-600 uppercase tracking-wider">Accuracy</p>
                                                <svg class="w-3 h-3 text-emi-navy-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                            </div>
                                            <p class="text-xl font-bold text-emi-navy-600">
                                                {{ (modelMetrics.accuracy * 100).toFixed(1) }}%
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-else class="text-center py-8">
                                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500 mx-auto mb-4"></div>
                                <p class="text-gray-400">Cargando informacion del modelo...</p>
                            </div>
                        </Card>

                        <!-- Acciones Rapidas -->
                        <Card title="Acciones Rapidas">
                            <div class="space-y-3">
                                <router-link
                                    to="/admin/profiles"
                                    class="flex items-center justify-between p-4 bg-emi-navy-50 rounded-xl hover:bg-emi-navy-100 transition-colors group"
                                >
                                    <div class="flex items-center">
                                        <div class="p-2 bg-emi-navy-100 rounded-lg mr-4 group-hover:bg-emi-navy-200 transition-colors">
                                            <svg class="w-5 h-5 text-emi-navy-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                            </svg>
                                        </div>
                                        <div>
                                            <p class="font-semibold text-emi-navy-700">Gestionar Perfiles</p>
                                            <p class="text-sm text-gray-500">CRUD de perfiles institucionales</p>
                                        </div>
                                    </div>
                                    <svg class="w-5 h-5 text-emi-navy-400 group-hover:text-emi-gold-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                    </svg>
                                </router-link>

                                <router-link
                                    to="/admin/users"
                                    class="flex items-center justify-between p-4 bg-purple-50 rounded-xl hover:bg-purple-100 transition-colors group"
                                >
                                    <div class="flex items-center">
                                        <div class="p-2 bg-purple-100 rounded-lg mr-4 group-hover:bg-purple-200 transition-colors">
                                           <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                                            </svg>
                                        </div>
                                        <div>
                                            <p class="font-semibold text-purple-700">Gestionar Usuarios</p>
                                            <p class="text-sm text-gray-500">Administrar estudiantes y titulados</p>
                                        </div>
                                    </div>
                                    <svg class="w-5 h-5 text-purple-400 group-hover:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                    </svg>
                                </router-link>

                                <router-link
                                    to="/admin/ofertas"
                                    class="flex items-center justify-between p-4 bg-emi-gold-50 rounded-xl hover:bg-emi-gold-100 transition-colors group"
                                >
                                    <div class="flex items-center">
                                        <div class="p-2 bg-emi-gold-100 rounded-lg mr-4 group-hover:bg-emi-gold-200 transition-colors">
                                            <svg class="w-5 h-5 text-emi-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                            </svg>
                                        </div>
                                        <div>
                                            <p class="font-semibold text-emi-gold-700">Gestionar Ofertas</p>
                                            <p class="text-sm text-gray-500">Pasantias y empleos</p>
                                        </div>
                                    </div>
                                    <svg class="w-5 h-5 text-emi-gold-400 group-hover:text-emi-navy-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                    </svg>
                                </router-link>

                                <router-link
                                    to="/admin/profiles/new"
                                    class="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors group"
                                >
                                    <div class="flex items-center">
                                        <div class="p-2 bg-gray-100 rounded-lg mr-4 group-hover:bg-gray-200 transition-colors">
                                            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                            </svg>
                                        </div>
                                        <div>
                                            <p class="font-semibold text-gray-700">Nuevo Perfil</p>
                                            <p class="text-sm text-gray-500">Crear perfil institucional</p>
                                        </div>
                                    </div>
                                    <svg class="w-5 h-5 text-gray-400 group-hover:text-emi-gold-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                    </svg>
                                </router-link>
                            </div>

                            <!-- Sectores -->
                            <div class="mt-6 pt-6 border-t border-gray-100">
                                <h3 class="text-sm font-semibold text-gray-700 mb-3">Sectores Existentes</h3>
                                <div class="flex flex-wrap gap-2">
                                    <Badge
                                        v-for="sector in stats.sectors"
                                        :key="sector"
                                        variant="navy"
                                    >
                                        {{ sector }}
                                    </Badge>
                                    <span v-if="stats.sectors.length === 0" class="text-gray-400 text-sm">
                                        No hay sectores definidos
                                    </span>
                                </div>
                            </div>
                        </Card>
                    </div>
                </div>
            </main>
        </div>

        <!-- Mobile menu toggle -->
        <button
            class="lg:hidden fixed bottom-4 right-4 z-40 p-3 bg-emi-navy-500 text-white rounded-full shadow-lg hover:bg-emi-navy-600 transition-colors"
        >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
        </button>
    </div>
</template>
