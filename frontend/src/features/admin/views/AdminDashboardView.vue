<script setup>
/**
 * AdminDashboardView - Fase 7 + Rediseno EMI
 * Dashboard administrativo con identidad corporativa EMI
 */

import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { useRouter } from 'vue-router'
import { getModelInfo } from '@/shared/api/ml.api'
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'
import AppLayout from '@/shared/components/AppLayout.vue'

const authStore = useAuthStore()
const router = useRouter()

const modelInfo = ref(null)

// Cargar datos al montar
onMounted(async () => {
    // Verificar admin
    if (!authStore.isAdmin) {
        router.push('/dashboard')
        return
    }

    try {
        modelInfo.value = await getModelInfo()
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

// Definición de módulos de la guía
const ALL_MODULE_GUIDE = [
    {
        id: 'gestion_usuarios',
        title: 'Gestión de Usuarios',
        desc: 'Visualiza y administra todas las cuentas registradas en el sistema. Puedes crear nuevos usuarios, editar su información, asignarles un rol específico y activar o desactivar su acceso. Los roles determinan qué módulos y funciones puede utilizar cada usuario.',
        icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>`,
    },
    {
        id: 'digitalizacion_perfiles',
        title: 'Digitalización de Perfiles',
        desc: 'Permite a los usuarios (estudiantes y titulados) construir su perfil profesional dentro del sistema: subir su CV para extracción automática de datos, completar su información académica, experiencia laboral, habilidades técnicas e idiomas. También posibilita buscar y explorar perfiles de otros usuarios registrados.',
        icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>`,
    },
    {
        id: 'oferta_laboral',
        title: 'Gestión de Convocatorias Laborales',
        desc: 'Administra las convocatorias de pasantías y empleos publicadas en el sistema. Puedes crear nuevas convocatorias definiendo requisitos, área, modalidad, cupos y fechas; editarlas, activarlas o cerrarlas. Los estudiantes y titulados podrán visualizarlas y postularse desde su perfil.',
        icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>`,
    },
    {
        id: 'perfiles_institucionales',
        title: 'Perfiles Institucionales',
        desc: 'Registra y gestiona los perfiles de las empresas e instituciones que participan en el sistema como fuentes de convocatorias laborales. Cada perfil incluye información organizacional, sector de actividad y datos de contacto, y sirve como respaldo de las convocatorias publicadas.',
        icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>`,
    },
    {
        id: 'evaluacion_perfiles',
        title: 'Evaluación de Perfiles',
        desc: 'Módulo central del sistema de recomendación. Permite ver la correspondencia entre los perfiles digitalizados y las convocatorias laborales activas, consultar el historial de postulaciones y acceder al ranking de candidatos por convocatoria generado automáticamente por el modelo de Machine Learning, ordenando a los postulantes según su nivel de compatibilidad.',
        icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>`,
    },
    {
        id: 'informes_reportes',
        title: 'Informes y Reportes',
        desc: 'Genera y consulta reportes estadísticos detallados sobre el funcionamiento del sistema: actividad de usuarios, métricas de convocatorias laborales, distribución de perfiles institucionales y más. Permite aplicar filtros avanzados y exportar los resultados en formato PDF para su análisis o presentación.',
        icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>`,
    },
]

const visibleModules = computed(() =>
    ALL_MODULE_GUIDE.filter(m => authStore.hasModuleAccess(m.id))
)
</script>

<template>
    <AppLayout>
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Header -->
            <div class="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 class="text-3xl font-bold text-emi-navy-500">Panel de Administración</h1>
                    <p class="mt-2 text-gray-600">
                        Bienvenido al sistema. Desde aquí puedes acceder a todos los módulos disponibles según tu rol.
                    </p>
                </div>
            </div>

            <!-- Main Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

                <!-- Guía de navegación -->
                <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6 flex flex-col gap-5">
                    <!-- Encabezado -->
                    <div class="flex items-center gap-3">
                        <div class="w-1 h-6 rounded-full bg-emi-gold-500 flex-shrink-0"></div>
                        <h2 class="text-base font-bold text-emi-navy-500">¿Cómo navegar el sistema?</h2>
                    </div>

                    <!-- Texto explicativo -->
                    <p class="text-sm text-gray-600 leading-relaxed">
                        Todos los módulos del sistema están accesibles desde la
                        <span class="font-semibold text-emi-navy-600">barra lateral izquierda</span>.
                        Puedes expandirla o contraerla en cualquier momento usando el ícono del menú en la parte superior.
                    </p>

                    <!-- Lista de módulos filtrada por permisos del rol -->
                    <ul v-if="visibleModules.length > 0" class="space-y-3">
                        <li v-for="mod in visibleModules" :key="mod.id" class="flex items-start gap-3">
                            <div class="mt-0.5 flex-shrink-0 w-7 h-7 rounded-lg bg-emi-navy-50 border border-emi-navy-100 flex items-center justify-center">
                                <svg class="w-4 h-4 text-emi-navy-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="mod.icon"></svg>
                            </div>
                            <div>
                                <p class="text-sm font-semibold text-emi-navy-700">{{ mod.title }}</p>
                                <p class="text-xs text-gray-500 mt-0.5">{{ mod.desc }}</p>
                            </div>
                        </li>
                    </ul>
                    <p v-else class="text-xs text-gray-400 italic">No hay módulos asignados a tu rol actual.</p>

                    <!-- Nota al pie -->
                    <div class="flex items-start gap-2 p-3 bg-emi-navy-50 border border-emi-navy-100 rounded-lg">
                        <svg class="w-4 h-4 text-emi-navy-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <p class="text-xs text-emi-navy-600">
                            Los módulos visibles en la barra lateral varían según el <span class="font-semibold">rol asignado</span> a tu cuenta. Si necesitas acceso a un módulo adicional, contacta al administrador del sistema.
                        </p>
                    </div>
                </div>

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
