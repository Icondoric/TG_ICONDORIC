<script setup>
/**
 * Badge - Componente para etiquetas y estados
 * Props: variant (navy, gold, success, danger, neutral)
 */
defineProps({
    variant: {
        type: String,
        default: 'neutral',
        validator: (value) => ['navy', 'gold', 'success', 'danger', 'neutral'].includes(value)
    },
    size: {
        type: String,
        default: 'md',
        validator: (value) => ['sm', 'md', 'lg'].includes(value)
    }
})

const variantClasses = {
    navy: 'bg-emi-navy-100 text-emi-navy-700',
    gold: 'bg-emi-gold-100 text-emi-gold-700',
    success: 'bg-emi-gold-100 text-emi-gold-700',
    danger: 'bg-red-100 text-red-700',
    neutral: 'bg-gray-100 text-gray-700'
}

const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base'
}
</script>

<template>
    <span
        :class="[
            'inline-flex items-center rounded-full font-medium',
            variantClasses[variant],
            sizeClasses[size]
        ]"
    >
        <slot></slot>
    </span>
</template>
