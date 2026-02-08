export function useFormatters() {
    const formatDate = (dateStr) => {
        if (!dateStr) return ''
        const date = new Date(dateStr)
        return date.toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        })
    }

    const formatDateLong = (dateString) => {
        if (!dateString) return 'N/A'
        const date = new Date(dateString)
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })
    }

    const formatDateWithTime = (dateString) => {
        if (!dateString) return 'N/A'
        const date = new Date(dateString)
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    const formatScore = (score) => {
        return Math.round((score || 0) * 100)
    }

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB', 'GB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

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

    return {
        formatDate,
        formatDateLong,
        formatDateWithTime,
        formatScore,
        formatFileSize,
        formatScoreLabel
    }
}
