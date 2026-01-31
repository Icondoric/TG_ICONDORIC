<script setup>
/**
 * AdminDashboardView - Fase 7
 * Dashboard administrativo para ver metricas del sistema ML
 */

import { ref, onMounted, computed } from 'vue'
import { useMLStore } from '../../stores/ml'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

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
    return mlStore.modelInfo.model_loaded ? 'Activo' : 'Inactivo'
})

const modelMetrics = computed(() => {
    return mlStore.modelInfo?.training_metrics || {}
})
</script>

<template>
    <div class="max-w-7xl mx-auto py-8 px-4">
        <!-- Header -->
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-slate-800">Panel de Administracion</h1>
            <p class="mt-2 text-slate-600">
                Vista general del sistema de Machine Learning
            </p>
        </header>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Modelo ML -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-slate-500">Estado del Modelo</p>
                        <p class="text-2xl font-bold mt-1" :class="mlStore.isModelReady ? 'text-green-600' : 'text-red-600'">
                            {{ modelStatus }}
                        </p>
                    </div>
                    <div :class="['p-3 rounded-full', mlStore.isModelReady ? 'bg-green-100' : 'bg-red-100']">
                        <svg class="w-6 h-6" :class="mlStore.isModelReady ? 'text-green-600' : 'text-red-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Perfiles Totales -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-slate-500">Perfiles Totales</p>
                        <p class="text-2xl font-bold text-slate-800 mt-1">
                            {{ stats.totalProfiles }}
                        </p>
                    </div>
                    <div class="p-3 rounded-full bg-blue-100">
                        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Perfiles Activos -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-slate-500">Perfiles Activos</p>
                        <p class="text-2xl font-bold text-green-600 mt-1">
                            {{ stats.activeProfiles }}
                        </p>
                    </div>
                    <div class="p-3 rounded-full bg-green-100">
                        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Sectores -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-slate-500">Sectores</p>
                        <p class="text-2xl font-bold text-purple-600 mt-1">
                            {{ stats.sectors.length }}
                        </p>
                    </div>
                    <div class="p-3 rounded-full bg-purple-100">
                        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contenido Principal -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Info del Modelo -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <h2 class="text-lg font-semibold text-slate-800 mb-4">
                    Informacion del Modelo ML
                </h2>

                <div v-if="mlStore.modelInfo" class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <p class="text-sm text-slate-500">Tipo de Modelo</p>
                            <p class="font-medium text-slate-800">{{ mlStore.modelInfo.model_type || 'Ridge' }}</p>
                        </div>
                        <div>
                            <p class="text-sm text-slate-500">Version</p>
                            <p class="font-medium text-slate-800">{{ mlStore.modelInfo.version || 'v1' }}</p>
                        </div>
                        <div>
                            <p class="text-sm text-slate-500">Alpha</p>
                            <p class="font-medium text-slate-800">{{ mlStore.modelInfo.alpha || 'N/A' }}</p>
                        </div>
                        <div>
                            <p class="text-sm text-slate-500">Features</p>
                            <p class="font-medium text-slate-800">{{ mlStore.modelInfo.n_features || '18' }}</p>
                        </div>
                    </div>

                    <!-- Metricas -->
                    <div v-if="Object.keys(modelMetrics).length > 0" class="border-t pt-4 mt-4">
                        <h3 class="text-sm font-medium text-slate-700 mb-3">Metricas de Entrenamiento</h3>
                        <div class="grid grid-cols-2 gap-3">
                            <div v-if="modelMetrics.r2_score !== undefined" class="bg-slate-50 p-3 rounded-lg">
                                <p class="text-xs text-slate-500">R2 Score</p>
                                <p class="text-lg font-bold text-blue-600">
                                    {{ (modelMetrics.r2_score * 100).toFixed(1) }}%
                                </p>
                            </div>
                            <div v-if="modelMetrics.rmse !== undefined" class="bg-slate-50 p-3 rounded-lg">
                                <p class="text-xs text-slate-500">RMSE</p>
                                <p class="text-lg font-bold text-blue-600">
                                    {{ modelMetrics.rmse.toFixed(4) }}
                                </p>
                            </div>
                            <div v-if="modelMetrics.mae !== undefined" class="bg-slate-50 p-3 rounded-lg">
                                <p class="text-xs text-slate-500">MAE</p>
                                <p class="text-lg font-bold text-blue-600">
                                    {{ modelMetrics.mae.toFixed(4) }}
                                </p>
                            </div>
                            <div v-if="modelMetrics.accuracy !== undefined" class="bg-slate-50 p-3 rounded-lg">
                                <p class="text-xs text-slate-500">Accuracy</p>
                                <p class="text-lg font-bold text-blue-600">
                                    {{ (modelMetrics.accuracy * 100).toFixed(1) }}%
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else class="text-center py-8">
                    <p class="text-slate-400">Cargando informacion del modelo...</p>
                </div>
            </div>

            <!-- Acciones Rapidas -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <h2 class="text-lg font-semibold text-slate-800 mb-4">
                    Acciones Rapidas
                </h2>

                <div class="space-y-3">
                    <router-link
                        to="/admin/profiles"
                        class="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors"
                    >
                        <div class="flex items-center">
                            <div class="p-2 bg-blue-100 rounded-lg mr-4">
                                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                </svg>
                            </div>
                            <div>
                                <p class="font-medium text-slate-800">Gestionar Perfiles</p>
                                <p class="text-sm text-slate-500">CRUD de perfiles institucionales</p>
                            </div>
                        </div>
                        <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                    </router-link>

                    <router-link
                        to="/admin/profiles/new"
                        class="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors"
                    >
                        <div class="flex items-center">
                            <div class="p-2 bg-green-100 rounded-lg mr-4">
                                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                </svg>
                            </div>
                            <div>
                                <p class="font-medium text-slate-800">Nuevo Perfil</p>
                                <p class="text-sm text-slate-500">Crear perfil institucional</p>
                            </div>
                        </div>
                        <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                    </router-link>
                </div>

                <!-- Sectores -->
                <div class="mt-6 pt-6 border-t">
                    <h3 class="text-sm font-medium text-slate-700 mb-3">Sectores Existentes</h3>
                    <div class="flex flex-wrap gap-2">
                        <span
                            v-for="sector in stats.sectors"
                            :key="sector"
                            class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                        >
                            {{ sector }}
                        </span>
                        <span v-if="stats.sectors.length === 0" class="text-slate-400 text-sm">
                            No hay sectores definidos
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
