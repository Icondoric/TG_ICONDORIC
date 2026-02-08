import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { getMyRecommendations, checkRecommendationEligibility, markRecommendationViewed } from '@/features/recommendations/api/recommendations.api'

export function useRecommendations() {
    const authStore = useAuthStore()

    const recommendations = ref([])
    const perfilSummary = ref(null)
    const loading = ref(true)
    const refreshing = ref(false)
    const error = ref(null)
    const isEligible = ref(true)
    const eligibilityReason = ref('')
    const eligibilityAction = ref('')
    const missingFields = ref([])
    const expandedId = ref(null)

    const userRole = computed(() => authStore.user?.rol || 'estudiante')
    const newCount = computed(() => recommendations.value.filter(r => !r.fue_vista).length)
    const aptoCount = computed(() => recommendations.value.filter(r => r.clasificacion === 'APTO').length)
    const consideradoCount = computed(() => recommendations.value.filter(r => r.clasificacion === 'CONSIDERADO').length)
    const bestMatch = computed(() => {
        if (recommendations.value.length === 0) return null
        return recommendations.value.reduce((best, rec) =>
            rec.match_score > (best?.match_score || 0) ? rec : best
        , null)
    })

    const formatScoreLabel = (key) => {
        const labels = {
            hard_skills_score: 'Habilidades Tecnicas',
            soft_skills_score: 'Habilidades Blandas',
            education_score: 'Formacion Academica',
            experience_score: 'Experiencia',
            languages_score: 'Idiomas'
        }
        return labels[key] || key
    }

    const formatDate = (dateStr) => {
        if (!dateStr) return ''
        const date = new Date(dateStr)
        return date.toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        })
    }

    const toggleExpand = async (recId) => {
        if (expandedId.value === recId) {
            expandedId.value = null
        } else {
            expandedId.value = recId

            const rec = recommendations.value.find(r => r.id === recId)
            if (rec && !rec.fue_vista) {
                try {
                    await markRecommendationViewed(recId)
                    rec.fue_vista = true
                } catch (e) {
                    console.error('Error marking as viewed:', e)
                }
            }
        }
    }

    const checkEligibility = async () => {
        try {
            const result = await checkRecommendationEligibility()

            isEligible.value = result.eligible
            eligibilityReason.value = result.reason || ''
            eligibilityAction.value = result.action_required || ''
            missingFields.value = result.missing_fields || []

            return result.eligible
        } catch (e) {
            return true
        }
    }

    const loadRecommendations = async (forceRefresh = false) => {
        if (forceRefresh) {
            refreshing.value = true
        } else {
            loading.value = true
        }
        error.value = null

        try {
            const eligible = await checkEligibility()

            if (!eligible) {
                loading.value = false
                refreshing.value = false
                return
            }

            const result = await getMyRecommendations({
                top_n: 20,
                recalcular: forceRefresh
            })

            recommendations.value = result.recomendaciones || []
            perfilSummary.value = result.perfil_summary
        } catch (e) {
            error.value = e.response?.data?.detail || 'Error cargando recomendaciones'
        } finally {
            loading.value = false
            refreshing.value = false
        }
    }

    onMounted(() => {
        loadRecommendations()
    })

    return {
        recommendations,
        perfilSummary,
        loading,
        refreshing,
        error,
        isEligible,
        eligibilityReason,
        eligibilityAction,
        missingFields,
        expandedId,
        userRole,
        newCount,
        aptoCount,
        consideradoCount,
        bestMatch,
        formatScoreLabel,
        formatDate,
        toggleExpand,
        loadRecommendations
    }
}
