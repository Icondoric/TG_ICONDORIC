<script setup>
/**
 * GaugeChart - Medidor circular con animacion
 * Props: value (0-100), size (sm, md, lg), label
 * Colores: Dorado EMI >=70%, Azul >=50%, Rojo <50%
 */
import { computed, ref, onMounted } from 'vue'

const props = defineProps({
    value: {
        type: Number,
        default: 0,
        validator: (v) => v >= 0 && v <= 100
    },
    size: {
        type: String,
        default: 'md',
        validator: (v) => ['sm', 'md', 'lg'].includes(v)
    },
    label: {
        type: String,
        default: ''
    },
    showPercentage: {
        type: Boolean,
        default: true
    }
})

const animatedValue = ref(0)

onMounted(() => {
    // Animate value on mount
    const duration = 1000
    const startTime = performance.now()
    const startValue = 0
    const endValue = props.value

    const animate = (currentTime) => {
        const elapsed = currentTime - startTime
        const progress = Math.min(elapsed / duration, 1)
        // Easing function (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3)
        animatedValue.value = Math.round(startValue + (endValue - startValue) * easeOut)

        if (progress < 1) {
            requestAnimationFrame(animate)
        }
    }
    requestAnimationFrame(animate)
})

const sizeConfig = {
    sm: { width: 80, stroke: 6, fontSize: 'text-lg' },
    md: { width: 120, stroke: 8, fontSize: 'text-2xl' },
    lg: { width: 160, stroke: 10, fontSize: 'text-3xl' }
}

const config = computed(() => sizeConfig[props.size])
const radius = computed(() => (config.value.width - config.value.stroke) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const strokeDashoffset = computed(() => {
    const progress = animatedValue.value / 100
    return circumference.value * (1 - progress)
})

const strokeColor = computed(() => {
    if (props.value >= 70) return '#D4AF37' // Dorado EMI
    if (props.value >= 50) return '#003366' // Azul Navy EMI
    return '#DC3545' // Rojo peligro
})

const textColor = computed(() => {
    if (props.value >= 70) return 'text-emi-gold-500'
    if (props.value >= 50) return 'text-emi-navy-500'
    return 'text-danger'
})
</script>

<template>
    <div class="flex flex-col items-center">
        <div class="relative" :style="{ width: `${config.width}px`, height: `${config.width}px` }">
            <!-- Background circle -->
            <svg
                :width="config.width"
                :height="config.width"
                class="transform -rotate-90"
            >
                <circle
                    :cx="config.width / 2"
                    :cy="config.width / 2"
                    :r="radius"
                    fill="none"
                    stroke="#e5e7eb"
                    :stroke-width="config.stroke"
                />
                <!-- Progress circle -->
                <circle
                    :cx="config.width / 2"
                    :cy="config.width / 2"
                    :r="radius"
                    fill="none"
                    :stroke="strokeColor"
                    :stroke-width="config.stroke"
                    stroke-linecap="round"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="strokeDashoffset"
                    class="transition-all duration-1000 ease-out"
                />
            </svg>
            <!-- Center text -->
            <div
                v-if="showPercentage"
                class="absolute inset-0 flex items-center justify-center"
            >
                <span :class="['font-bold', config.fontSize, textColor]">
                    {{ animatedValue }}%
                </span>
            </div>
        </div>
        <p v-if="label" class="mt-2 text-sm text-gray-600 text-center">{{ label }}</p>
    </div>
</template>
