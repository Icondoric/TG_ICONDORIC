import { classificationConfig, getClassificationBadge, getClassificationVariant } from '@/shared/constants/classifications'

export function useClassification() {
    const getConfig = (classification) => {
        return classificationConfig[classification] || classificationConfig.NO_APTO
    }

    const getBadgeClasses = (classification) => {
        return getClassificationBadge(classification)
    }

    const getVariant = (classification) => {
        return getClassificationVariant(classification)
    }

    const getScoreColor = (score) => {
        if (score >= 0.7) return 'text-green-600'
        if (score >= 0.5) return 'text-yellow-600'
        return 'text-red-600'
    }

    const getScoreBgColor = (score) => {
        if (score >= 0.7) return 'bg-green-500'
        if (score >= 0.5) return 'bg-yellow-500'
        return 'bg-red-500'
    }

    return {
        getConfig,
        getBadgeClasses,
        getVariant,
        getScoreColor,
        getScoreBgColor
    }
}
