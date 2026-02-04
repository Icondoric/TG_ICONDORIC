<template>
  <component
    :is="tag"
    :type="nativeType"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <!-- Loading spinner -->
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-5 w-5"
      :class="iconSizeClass"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      ></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>

    <!-- Icon (left) -->
    <span v-if="$slots.icon && !loading" class="inline-flex" :class="iconSizeClass">
      <slot name="icon" />
    </span>

    <!-- Content -->
    <slot />

    <!-- Icon (right) -->
    <span v-if="$slots.iconRight" class="inline-flex ml-2" :class="iconSizeClass">
      <slot name="iconRight" />
    </span>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'gold', 'outline', 'ghost', 'danger'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  tag: {
    type: String,
    default: 'button'
  },
  nativeType: {
    type: String,
    default: 'button'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  fullWidth: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: String,
    default: 'lg',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl', 'full'].includes(value)
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}

const baseClasses = 'inline-flex items-center justify-center font-semibold transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2'

const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-gradient-to-r from-emi-navy-600 to-emi-navy-700 hover:from-emi-navy-700 hover:to-emi-navy-800 text-white shadow-md hover:shadow-emi-lg focus:ring-emi-navy-500 disabled:from-gray-400 disabled:to-gray-500',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-900 shadow-sm hover:shadow-md focus:ring-gray-500 disabled:bg-gray-50 disabled:text-gray-400',
    gold: 'bg-gradient-to-r from-emi-gold-500 to-emi-gold-600 hover:from-emi-gold-600 hover:to-emi-gold-700 text-white shadow-md hover:shadow-gold focus:ring-emi-gold-500 disabled:from-gray-400 disabled:to-gray-500',
    outline: 'border-2 border-emi-navy-600 text-emi-navy-600 hover:bg-emi-navy-50 focus:ring-emi-navy-500 disabled:border-gray-300 disabled:text-gray-400',
    ghost: 'text-emi-navy-600 hover:bg-emi-navy-50 focus:ring-emi-navy-500 disabled:text-gray-400',
    danger: 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-md hover:shadow-lg focus:ring-red-500 disabled:from-gray-400 disabled:to-gray-500'
  }
  return variants[props.variant] || variants.primary
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'px-3 py-1.5 text-xs',
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
    xl: 'px-10 py-5 text-xl'
  }
  return sizes[props.size] || sizes.md
})

const roundedClasses = computed(() => {
  const rounded = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    full: 'rounded-full'
  }
  return rounded[props.rounded] || rounded.lg
})

const iconSizeClass = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-7 h-7'
  }
  return sizes[props.size] || sizes.md
})

const buttonClasses = computed(() => {
  return [
    baseClasses,
    variantClasses.value,
    sizeClasses.value,
    roundedClasses.value,
    {
      'w-full': props.fullWidth,
      'opacity-60 cursor-not-allowed': props.disabled || props.loading,
      'transform hover:scale-105': !props.disabled && !props.loading && props.variant !== 'ghost'
    }
  ]
})
</script>
