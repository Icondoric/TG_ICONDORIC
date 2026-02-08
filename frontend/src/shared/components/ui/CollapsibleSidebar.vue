<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: true
  },
  width: {
    type: String,
    default: '280px'
  },
  collapsedWidth: {
    type: String,
    default: '60px'
  },
  position: {
    type: String,
    default: 'left', // 'left' or 'right'
  },
  persistenceKey: {
      type: String,
      default: null
  },
  leftOffset: {
      type: String,
      default: '256px'
  }
})

const emit = defineEmits(['update:isOpen', 'toggle'])

const isExpanded = ref(props.isOpen)
// ... keeping existing code ...
</script>

<template>
  <aside 
    class="fixed h-screen bg-white border-r border-gray-200 transition-all duration-300 ease-in-out z-30 hidden lg:block"
    :style="{ 
      width: isExpanded ? width : collapsedWidth,
      left: leftOffset
    }"
  >
    <!-- Toggle Button -->
    <button 
      @click="toggle"
      class="absolute top-4 -right-3 z-50 w-6 h-6 bg-white border border-gray-200 rounded-full flex items-center justify-center text-gray-500 hover:text-emi-navy-500 hover:border-emi-navy-300 transition-colors shadow-sm focus:outline-none"
    >
        <div :class="{ 'rotate-180': !isExpanded }" class="transition-transform duration-300">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
        </div>
    </button>

    <!-- Content Container -->
    <div class="h-full w-full overflow-y-auto overflow-x-hidden custom-scrollbar">
        <!-- Expanded Content -->
        <div 
            class="transition-opacity duration-300 delay-100"
            :class="{ 'opacity-0 invisible absolute': !isExpanded, 'opacity-100 visible': isExpanded }"
            :style="{ width: width }"
        >
            <slot></slot>
        </div>

        <!-- Collapsed Content (Icons) -->
        <div 
            class="transition-opacity duration-300"
            :class="{ 'opacity-0 invisible absolute': isExpanded, 'opacity-100 visible w-full flex flex-col items-center pt-16': !isExpanded }"
        >
            <slot name="collapsed"></slot>
        </div>
    </div>
  </aside>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e2e8f0;
  border-radius: 20px;
}
</style>
