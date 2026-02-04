<template>
  <span
    :class="badgeClasses"
  >
    <!-- Dot indicator (optional) -->
    <span
      v-if="dot"
      class="w-2 h-2 rounded-full mr-1.5"
      :class="dotColorClass"
    ></span>

    <!-- Icon slot (optional) -->
    <span v-if="$slots.icon" class="inline-flex mr-1" :class="iconSizeClass">
      <slot name="icon" />
    </span>

    <!-- Content -->
    <slot />
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'neutral',
    validator: (value) => ['navy', 'gold', 'success', 'danger', 'warning', 'info', 'neutral'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg'].includes(value)
  },
  dot: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: String,
    default: 'full',
    validator: (value) => ['sm', 'md', 'lg', 'full'].includes(value)
  }
})

const variantClasses = computed(() => {
  const variants = {
    navy: 'bg-emi-navy-100 text-emi-navy-700 border border-emi-navy-200',
    gold: 'bg-emi-gold-100 text-emi-gold-700 border border-emi-gold-200',
    success: 'bg-success-50 text-success-700 border border-success-200',
    danger: 'bg-danger-50 text-danger-700 border border-danger-200',
    warning: 'bg-warning-50 text-warning-700 border border-warning-200',
    info: 'bg-info-50 text-info-700 border border-info-200',
    neutral: 'bg-gray-100 text-gray-700 border border-gray-200'
  }
  return variants[props.variant] || variants.neutral
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'px-2 py-0.5 text-xs',
    sm: 'px-2.5 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base'
  }
  return sizes[props.size] || sizes.md
})

const roundedClasses = computed(() => {
  const rounded = {
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    full: 'rounded-full'
  }
  return rounded[props.rounded] || rounded.full
})

const iconSizeClass = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  }
  return sizes[props.size] || sizes.md
})

const dotColorClass = computed(() => {
  const colors = {
    navy: 'bg-emi-navy-600',
    gold: 'bg-emi-gold-600',
    success: 'bg-success-600',
    danger: 'bg-danger-600',
    warning: 'bg-warning-600',
    info: 'bg-info-600',
    neutral: 'bg-gray-600'
  }
  return colors[props.variant] || colors.neutral
})

const badgeClasses = computed(() => {
  return [
    'inline-flex items-center font-medium transition-colors duration-200',
    variantClasses.value,
    sizeClasses.value,
    roundedClasses.value
  ]
})
</script>
