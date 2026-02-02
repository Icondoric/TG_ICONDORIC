<script setup>
/**
 * Card - Componente reutilizable con estilo EMI
 * Props: title, subtitle, padding, shadow
 */
defineProps({
    title: {
        type: String,
        default: ''
    },
    subtitle: {
        type: String,
        default: ''
    },
    padding: {
        type: String,
        default: 'p-6',
        validator: (value) => ['p-4', 'p-6', 'p-8'].includes(value)
    },
    shadow: {
        type: String,
        default: 'shadow-sm',
        validator: (value) => ['shadow-none', 'shadow-sm', 'shadow-md', 'shadow-lg'].includes(value)
    },
    hoverable: {
        type: Boolean,
        default: true
    }
})
</script>

<template>
    <div
        :class="[
            'bg-white rounded-xl border border-gray-100 transition-shadow duration-200',
            padding,
            shadow,
            hoverable ? 'hover:shadow-md' : ''
        ]"
    >
        <div v-if="title || subtitle" class="mb-4">
            <h3 v-if="title" class="text-lg font-semibold text-gray-900">{{ title }}</h3>
            <p v-if="subtitle" class="text-sm text-gray-500 mt-1">{{ subtitle }}</p>
        </div>
        <slot></slot>
    </div>
</template>
