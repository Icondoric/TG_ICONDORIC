<script setup>
/**
 * ProgressBar - Barra de progreso con colores EMI
 * Props: value, showLabel, variant
 * Colores segun valor: Dorado >=70%, Azul >=50%, Rojo <50%
 */
import { computed } from 'vue'

const props = defineProps({
    value: {
        type: Number,
        default: 0,
        validator: (v) => v >= 0 && v <= 100
    },
    showLabel: {
        type: Boolean,
        default: true
    },
    label: {
        type: String,
        default: ''
    },
    variant: {
        type: String,
        default: 'auto',
        validator: (v) => ['auto', 'navy', 'gold', 'danger'].includes(v)
    },
    size: {
        type: String,
        default: 'md',
        validator: (v) => ['sm', 'md', 'lg'].includes(v)
    }
})

const barColor = computed(() => {
    if (props.variant !== 'auto') {
        const colors = {
            navy: 'bg-emi-navy-500',
            gold: 'bg-emi-gold-500',
            danger: 'bg-danger'
        }
        return colors[props.variant]
    }
    // Auto color based on value
    if (props.value >= 70) return 'bg-emi-gold-500'
    if (props.value >= 50) return 'bg-emi-navy-500'
    return 'bg-danger'
})

const heightClass = computed(() => {
    const heights = {
        sm: 'h-1.5',
        md: 'h-2.5',
        lg: 'h-4'
    }
    return heights[props.size]
})
</script>

<template>
    <div class="w-full">
        <div v-if="showLabel || label" class="flex justify-between text-sm mb-1">
            <span class="text-gray-600">{{ label }}</span>
            <span v-if="showLabel" class="font-medium text-gray-900">{{ Math.round(value) }}%</span>
        </div>
        <div :class="['w-full bg-gray-200 rounded-full overflow-hidden', heightClass]">
            <div
                :class="['rounded-full transition-all duration-500 ease-out', heightClass, barColor]"
                :style="{ width: `${value}%` }"
            ></div>
        </div>
    </div>
</template>
