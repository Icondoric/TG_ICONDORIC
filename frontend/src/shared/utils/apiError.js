/**
 * Convierte errores de la API en mensajes legibles en español.
 * Maneja:
 *  - Errores 422 de Pydantic (array de objetos con loc/msg/type)
 *  - Errores con campo `detail` (string o array)
 *  - Errores de red / desconocidos
 */

const FIELD_LABELS = {
    nombre: 'Nombre',
    nombre_completo: 'Nombre completo',
    email: 'Correo electrónico',
    password: 'Contraseña',
    rol: 'Rol',
    sector: 'Sector',
    institution_name: 'Nombre de institución',
    description: 'Descripción',
    ubicacion: 'Ubicación',
    contact_phone: 'Teléfono de contacto',
    contact_email: 'Correo de contacto',
    modulos_permitidos: 'Módulos permitidos',
    titulo: 'Título',
    descripcion: 'Descripción',
    tipo: 'Tipo',
    estado: 'Estado',
}

const MSG_TRANSLATIONS = {
    'Field required': 'Campo requerido',
    'field required': 'Campo requerido',
    'value is not a valid email address': 'Debe ser un correo electrónico válido',
    'Input should be a valid integer': 'Debe ser un número entero',
    'Input should be a valid number': 'Debe ser un número',
    'Input should be a valid string': 'Debe ser texto',
    'Input should be a valid boolean': 'Debe ser verdadero o falso',
}

function translateMsg(msg, ctx) {
    if (!msg) return 'Error de validación'

    // Mapeo exacto
    if (MSG_TRANSLATIONS[msg]) return MSG_TRANSLATIONS[msg]

    // String too short
    const shortMatch = msg.match(/String should have at least (\d+) characters?/i)
    if (shortMatch) return `Debe tener al menos ${shortMatch[1]} caracteres`

    // String too long
    const longMatch = msg.match(/String should have at most (\d+) characters?/i)
    if (longMatch) return `Debe tener máximo ${longMatch[1]} caracteres`

    // Greater than
    const gtMatch = msg.match(/Input should be greater than (\S+)/i)
    if (gtMatch) return `Debe ser mayor que ${gtMatch[1]}`

    // Less than
    const ltMatch = msg.match(/Input should be less than (\S+)/i)
    if (ltMatch) return `Debe ser menor que ${ltMatch[1]}`

    // Value error genérico (Pydantic v2 model_validator)
    // msg = "Value error, <el mensaje real>" — ctx.error puede ser un objeto vacío
    if (msg.toLowerCase().startsWith('value error')) {
        const inner = msg.replace(/^value error,?\s*/i, '').trim()
        return inner || fallback
    }

    return msg
}

function fieldLabel(loc) {
    // loc es algo como ["body", "sector"] o ["body", "weights", "habilidades"]
    // Tomamos el último segmento significativo
    const parts = (loc || []).filter(p => p !== 'body' && typeof p === 'string')
    const key = parts[parts.length - 1] || ''
    return FIELD_LABELS[key] || (key ? key.replace(/_/g, ' ') : 'Campo')
}

/**
 * Formatea un error de axios en un mensaje legible.
 * @param {Error} err - Error capturado en un catch
 * @param {string} fallback - Mensaje por defecto si no se puede formatear
 * @returns {string}
 */
export function formatApiError(err, fallback = 'Ocurrió un error inesperado') {
    if (!err) return fallback

    const data = err.response?.data

    if (!data) {
        // Error de red
        if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
            return 'El servidor tardó demasiado en responder. Intenta de nuevo.'
        }
        if (!err.response) {
            return 'No se pudo conectar con el servidor. Verifica tu conexión.'
        }
        return fallback
    }

    // Detail es un array → errores de validación Pydantic (422)
    const detail = data.detail ?? data
    if (Array.isArray(detail)) {
        const lines = detail.map(e => {
            const field = fieldLabel(e.loc)
            const msg = translateMsg(e.msg, e.ctx)
            return `• ${field}: ${msg}`
        })
        return lines.join('\n')
    }

    // Detail es string
    if (typeof detail === 'string' && detail.trim()) {
        return detail
    }

    // Detail es objeto con message
    if (typeof detail === 'object' && detail.message) {
        return detail.message
    }

    return fallback
}
