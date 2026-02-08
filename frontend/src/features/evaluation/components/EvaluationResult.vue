<script setup>
/**
 * EvaluationResult - Fase 7
 * Componente para mostrar el resultado de una evaluacion de CV
 */

import { computed } from 'vue'
import ScoreChart from '@/features/evaluation/components/ScoreChart.vue'

const props = defineProps({
    evaluation: {
        type: Object,
        required: true
    },
    profile: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['reset'])

// Computed
const matchPercentage = computed(() => {
    return Math.round((props.evaluation.match_score || 0) * 100)
})

const classificationConfig = computed(() => {
    const classification = props.evaluation.classification
    const configs = {
        'APTO': {
            label: 'APTO',
            color: 'text-green-700',
            bgColor: 'bg-green-100',
            borderColor: 'border-green-500',
            icon: '✓',
            message: 'Tu perfil cumple con los requisitos de esta institucion'
        },
        'CONSIDERADO': {
            label: 'CONSIDERADO',
            color: 'text-yellow-700',
            bgColor: 'bg-yellow-100',
            borderColor: 'border-yellow-500',
            icon: '~',
            message: 'Tu perfil podria ser considerado, pero hay areas de mejora'
        },
        'NO_APTO': {
            label: 'NO APTO',
            color: 'text-red-700',
            bgColor: 'bg-red-100',
            borderColor: 'border-red-500',
            icon: '✗',
            message: 'Tu perfil no cumple con los requisitos minimos'
        }
    }
    return configs[classification] || configs['NO_APTO']
})

const ringColor = computed(() => {
    const score = props.evaluation.match_score || 0
    if (score >= 0.7) return '#22c55e' // green-500
    if (score >= 0.5) return '#eab308' // yellow-500
    return '#ef4444' // red-500
})

// Calcular el stroke-dasharray para el circulo de progreso
const circumference = 2 * Math.PI * 45 // radio de 45
const strokeDashoffset = computed(() => {
    return circumference - (matchPercentage.value / 100) * circumference
})
</script>

<template>
    <div class="space-y-6">
        <!-- Tarjeta Principal de Resultado -->
        <div :class="['bg-white rounded-xl shadow-lg p-8 border-l-4', classificationConfig.borderColor]">
            <div class="flex flex-col md:flex-row items-center gap-8">
                <!-- Circulo de Score -->
                <div class="relative">
                    <svg class="w-36 h-36 transform -rotate-90">
                        <!-- Circulo de fondo -->
                        <circle
                            cx="72"
                            cy="72"
                            r="45"
                            stroke="#e2e8f0"
                            stroke-width="10"
                            fill="none"
                        />
                        <!-- Circulo de progreso -->
                        <circle
                            cx="72"
                            cy="72"
                            r="45"
                            :stroke="ringColor"
                            stroke-width="10"
                            fill="none"
                            stroke-linecap="round"
                            :stroke-dasharray="circumference"
                            :stroke-dashoffset="strokeDashoffset"
                            class="transition-all duration-1000"
                        />
                    </svg>
                    <div class="absolute inset-0 flex flex-col items-center justify-center">
                        <span class="text-3xl font-bold text-slate-800">{{ matchPercentage }}%</span>
                        <span class="text-xs text-slate-500">Match</span>
                    </div>
                </div>

                <!-- Informacion -->
                <div class="flex-1 text-center md:text-left">
                    <div :class="['inline-block px-4 py-2 rounded-full text-sm font-bold mb-3', classificationConfig.bgColor, classificationConfig.color]">
                        {{ classificationConfig.label }}
                    </div>
                    <h2 class="text-2xl font-bold text-slate-800 mb-2">
                        Resultado de Evaluacion
                    </h2>
                    <p class="text-slate-600 mb-2">
                        {{ classificationConfig.message }}
                    </p>
                    <p v-if="profile" class="text-sm text-slate-500">
                        Evaluado para: <span class="font-medium">{{ profile.institution_name }}</span>
                    </p>
                </div>
            </div>
        </div>

        <!-- Scores por Dimension -->
        <div class="bg-white rounded-xl shadow-md p-6">
            <h3 class="text-lg font-semibold text-slate-800 mb-4">
                Puntuacion por Dimension
            </h3>
            <ScoreChart
                :scores="evaluation.cv_scores"
                color-scheme="status"
            />
        </div>

        <!-- Fortalezas y Debilidades -->
        <div class="grid md:grid-cols-2 gap-6">
            <!-- Fortalezas -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <h3 class="text-lg font-semibold text-green-700 mb-4 flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Fortalezas
                </h3>
                <ul v-if="evaluation.top_strengths?.length" class="space-y-2">
                    <li
                        v-for="(strength, index) in evaluation.top_strengths"
                        :key="index"
                        class="flex items-start"
                    >
                        <span class="text-green-500 mr-2">+</span>
                        <span class="text-slate-600">{{ strength }}</span>
                    </li>
                </ul>
                <p v-else class="text-slate-400 text-sm">Sin fortalezas destacadas</p>
            </div>

            <!-- Debilidades -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <h3 class="text-lg font-semibold text-red-700 mb-4 flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    Areas de Mejora
                </h3>
                <ul v-if="evaluation.top_weaknesses?.length" class="space-y-2">
                    <li
                        v-for="(weakness, index) in evaluation.top_weaknesses"
                        :key="index"
                        class="flex items-start"
                    >
                        <span class="text-red-500 mr-2">-</span>
                        <span class="text-slate-600">{{ weakness }}</span>
                    </li>
                </ul>
                <p v-else class="text-slate-400 text-sm">Sin areas de mejora identificadas</p>
            </div>
        </div>

        <!-- Datos Extraidos del CV (Colapsable) -->
        <details class="bg-white rounded-xl shadow-md overflow-hidden">
            <summary class="px-6 py-4 cursor-pointer hover:bg-slate-50 transition-colors">
                <span class="text-lg font-semibold text-slate-800">
                    Datos Extraidos del CV
                </span>
            </summary>
            <div class="px-6 pb-6 border-t">
                <div v-if="evaluation.gemini_extraction" class="mt-4 space-y-4">
                    <!-- Hard Skills -->
                    <div v-if="evaluation.gemini_extraction.hard_skills?.length">
                        <h4 class="font-medium text-slate-700 mb-2">Habilidades Tecnicas</h4>
                        <div class="flex flex-wrap gap-2">
                            <span
                                v-for="skill in evaluation.gemini_extraction.hard_skills"
                                :key="skill"
                                class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                            >
                                {{ skill }}
                            </span>
                        </div>
                    </div>

                    <!-- Soft Skills -->
                    <div v-if="evaluation.gemini_extraction.soft_skills?.length">
                        <h4 class="font-medium text-slate-700 mb-2">Habilidades Blandas</h4>
                        <div class="flex flex-wrap gap-2">
                            <span
                                v-for="skill in evaluation.gemini_extraction.soft_skills"
                                :key="skill"
                                class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                            >
                                {{ skill }}
                            </span>
                        </div>
                    </div>

                    <!-- Educacion -->
                    <div v-if="evaluation.gemini_extraction.education?.length">
                        <h4 class="font-medium text-slate-700 mb-2">Educacion</h4>
                        <ul class="space-y-1">
                            <li
                                v-for="(edu, idx) in evaluation.gemini_extraction.education"
                                :key="idx"
                                class="text-sm text-slate-600"
                            >
                                {{ edu.degree }} - {{ edu.institution }} ({{ edu.year }})
                            </li>
                        </ul>
                    </div>

                    <!-- Experiencia -->
                    <div v-if="evaluation.gemini_extraction.experience?.length">
                        <h4 class="font-medium text-slate-700 mb-2">Experiencia</h4>
                        <ul class="space-y-2">
                            <li
                                v-for="(exp, idx) in evaluation.gemini_extraction.experience"
                                :key="idx"
                                class="text-sm text-slate-600"
                            >
                                <span class="font-medium">{{ exp.role }}</span> en {{ exp.company }}
                                <span class="text-slate-400">({{ exp.duration }})</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <p v-else class="mt-4 text-slate-400 text-sm">
                    No hay datos de extraccion disponibles
                </p>
            </div>
        </details>

        <!-- Botones de Accion -->
        <div class="flex justify-between items-center">
            <button
                @click="$emit('reset')"
                class="px-6 py-2 text-slate-600 hover:text-slate-800 font-medium transition-colors"
            >
                Nueva Evaluacion
            </button>
            <router-link
                to="/recommendations"
                class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
            >
                Ver Recomendaciones
            </router-link>
        </div>
    </div>
</template>
