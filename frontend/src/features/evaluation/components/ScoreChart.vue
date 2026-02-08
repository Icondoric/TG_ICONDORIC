<script setup>
/**
 * ScoreChart - Fase 7
 * Componente para visualizar scores como barras horizontales
 */

import { computed } from 'vue'

const props = defineProps({
    scores: {
        type: Object,
        required: true
    },
    showLabels: {
        type: Boolean,
        default: true
    },
    colorScheme: {
        type: String,
        default: 'blue' // 'blue', 'gradient', 'status'
    }
})

// Mapeo de nombres de dimension a labels legibles
const dimensionLabels = {
    hard_skills: 'Habilidades Tecnicas',
    soft_skills: 'Habilidades Blandas',
    experience: 'Experiencia',
    education: 'Educacion',
    languages: 'Idiomas'
}

// Computed
const formattedScores = computed(() => {
    return Object.entries(props.scores).map(([key, value]) => ({
        key,
        label: dimensionLabels[key] || key,
        value: typeof value === 'number' ? value : 0,
        percentage: Math.round((typeof value === 'number' ? value : 0) * 100)
    })).sort((a, b) => b.value - a.value)
})

// Obtener color segun esquema y valor
const getBarColor = (value) => {
    if (props.colorScheme === 'status') {
        if (value >= 0.7) return 'bg-green-500'
        if (value >= 0.5) return 'bg-yellow-500'
        return 'bg-red-500'
    }
    if (props.colorScheme === 'gradient') {
        const hue = Math.round(value * 120) // 0 = red, 120 = green
        return `bg-gradient-to-r from-amber-400 to-emerald-400`
    }
    // Default blue
    return 'bg-blue-500'
}

const getTextColor = (value) => {
    if (props.colorScheme === 'status') {
        if (value >= 0.7) return 'text-green-700'
        if (value >= 0.5) return 'text-yellow-700'
        return 'text-red-700'
    }
    return 'text-blue-700'
}
</script>

<template>
    <div class="space-y-4">
        <div
            v-for="score in formattedScores"
            :key="score.key"
            class="space-y-1"
        >
            <!-- Label y Valor -->
            <div v-if="showLabels" class="flex justify-between items-center">
                <span class="text-sm font-medium text-slate-700">{{ score.label }}</span>
                <span :class="['text-sm font-semibold', getTextColor(score.value)]">
                    {{ score.percentage }}%
                </span>
            </div>

            <!-- Barra -->
            <div class="w-full bg-slate-200 rounded-full h-3 overflow-hidden">
                <div
                    :class="['h-full rounded-full transition-all duration-500', getBarColor(score.value)]"
                    :style="{ width: `${score.percentage}%` }"
                ></div>
            </div>
        </div>
    </div>
</template>
