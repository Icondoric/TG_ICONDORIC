import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRecommendationsStore = defineStore('recommendations', () => {
    const recommendations = ref([])
    const isLoadingRecommendations = ref(false)
    const recommendationsError = ref(null)

    function resetRecommendations() {
        recommendations.value = []
        recommendationsError.value = null
    }

    return {
        recommendations,
        isLoadingRecommendations,
        recommendationsError,
        resetRecommendations
    }
})
