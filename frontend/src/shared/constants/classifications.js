export const classificationConfig = {
    APTO: {
        label: 'APTO',
        variant: 'gold',
        color: 'text-green-700',
        bgColor: 'bg-green-100',
        borderColor: 'border-green-500',
        message: 'Tu perfil cumple con los requisitos de esta institucion'
    },
    CONSIDERADO: {
        label: 'CONSIDERADO',
        variant: 'navy',
        color: 'text-yellow-700',
        bgColor: 'bg-yellow-100',
        borderColor: 'border-yellow-500',
        message: 'Tu perfil podria ser considerado, pero hay areas de mejora'
    },
    NO_APTO: {
        label: 'NO APTO',
        variant: 'danger',
        color: 'text-red-700',
        bgColor: 'bg-red-100',
        borderColor: 'border-red-500',
        message: 'Tu perfil no cumple con los requisitos minimos'
    }
}

export const getClassificationBadge = (classification) => {
    const badges = {
        'APTO': 'bg-green-100 text-green-700',
        'CONSIDERADO': 'bg-yellow-100 text-yellow-700',
        'NO_APTO': 'bg-red-100 text-red-700'
    }
    return badges[classification] || badges['NO_APTO']
}

export const getClassificationVariant = (classification) => {
    return classificationConfig[classification]?.variant || 'danger'
}
