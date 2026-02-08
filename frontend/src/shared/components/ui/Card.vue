<template>
  <component
    :is="clickable ? 'button' : 'div'"
    :class="cardClasses"
    @click="handleClick"
  >
    <!-- Header slot -->
    <div v-if="$slots.header || title || subtitle" :class="headerClasses">
      <slot name="header">
        <h3 v-if="title" class="font-display font-bold text-xl text-emi-navy-900">
          {{ title }}
        </h3>
        <p v-if="subtitle" class="text-sm text-gray-600 mt-1">
          {{ subtitle }}
        </p>
      </slot>
    </div>

    <!-- Body/Content -->
    <div :class="bodyClasses">
      <slot />
    </div>

    <!-- Footer slot -->
    <div v-if="$slots.footer" :class="footerClasses">
      <slot name="footer" />
    </div>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'glass', 'bordered', 'elevated'].includes(value)
  },
  padding: {
    type: String,
    default: 'md',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  shadow: {
    type: String,
    default: 'sm',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'emi'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: true
  },
  clickable: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: String,
    default: 'xl',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl', '2xl', '3xl'].includes(value)
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (props.clickable) {
    emit('click', event)
  }
}

const variantClasses = computed(() => {
  const variants = {
    default: 'bg-white border border-gray-100',
    glass: 'glass backdrop-blur-xl bg-white/95 border border-white/20',
    bordered: 'bg-white border-2 border-emi-navy-200',
    elevated: 'bg-white border-none'
  }
  return variants[props.variant] || variants.default
})

const paddingClasses = computed(() => {
  const paddings = {
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10'
  }
  return paddings[props.padding] || paddings.md
})

const shadowClasses = computed(() => {
  const shadows = {
    none: 'shadow-none',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    emi: 'shadow-emi'
  }
  return shadows[props.shadow] || shadows.sm
})

const roundedClasses = computed(() => {
  const rounded = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    '3xl': 'rounded-3xl'
  }
  return rounded[props.rounded] || rounded.xl
})

const headerClasses = computed(() => {
  return props.padding !== 'none' ? 'mb-4' : ''
})

const bodyClasses = computed(() => {
  return ''
})

const footerClasses = computed(() => {
  return props.padding !== 'none' ? 'mt-4 pt-4 border-t border-gray-100' : ''
})

const cardClasses = computed(() => {
  return [
    'transition-all duration-300',
    variantClasses.value,
    paddingClasses.value,
    shadowClasses.value,
    roundedClasses.value,
    {
      'hover:shadow-emi-lg': props.hoverable && !props.clickable,
      'hover:shadow-emi-lg hover:scale-[1.02] cursor-pointer focus:outline-none focus:ring-2 focus:ring-emi-navy-500 focus:ring-offset-2': props.clickable,
      'text-left': props.clickable
    }
  ]
})
</script>
