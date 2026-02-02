<script setup>
/**
 * Accordion - Componente acordeon para menus de navegacion
 * Props: items (array con title, content, icon)
 */
import { ref } from 'vue'

defineProps({
    items: {
        type: Array,
        required: true,
        // Each item: { id, title, content?, icon?, expanded? }
    },
    allowMultiple: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['select'])

const expandedItems = ref(new Set())

const toggleItem = (id) => {
    if (expandedItems.value.has(id)) {
        expandedItems.value.delete(id)
    } else {
        expandedItems.value.add(id)
    }
    // Force reactivity
    expandedItems.value = new Set(expandedItems.value)
}

const isExpanded = (id) => expandedItems.value.has(id)
</script>

<template>
    <div class="space-y-1">
        <div
            v-for="item in items"
            :key="item.id"
            class="rounded-lg overflow-hidden"
        >
            <!-- Header -->
            <button
                @click="item.content ? toggleItem(item.id) : emit('select', item.id)"
                class="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-emi-navy-50 transition-colors rounded-lg"
                :class="isExpanded(item.id) ? 'bg-emi-navy-50' : ''"
            >
                <div class="flex items-center gap-3">
                    <span v-if="item.icon" class="text-emi-navy-400" v-html="item.icon"></span>
                    <span class="font-medium text-gray-700">{{ item.title }}</span>
                </div>
                <svg
                    v-if="item.content"
                    :class="[
                        'w-4 h-4 text-gray-400 transition-transform duration-200',
                        isExpanded(item.id) ? 'rotate-180' : ''
                    ]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
            </button>

            <!-- Content -->
            <div
                v-if="item.content && isExpanded(item.id)"
                class="px-4 pb-3 pl-11"
            >
                <slot :name="`content-${item.id}`" :item="item">
                    <p class="text-sm text-gray-600">{{ item.content }}</p>
                </slot>
            </div>
        </div>
    </div>
</template>
