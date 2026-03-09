import client from '@/shared/api/client'

/**
 * Lista las ofertas disponibles para el usuario según su rol.
 * Estudiante → pasantías | Titulado → empleos | Admin → todas
 */
export const getOfertasDisponibles = () =>
    client.get('/api/postulaciones/convocatorias').then(r => r.data)

/**
 * Postula al usuario a una oferta y devuelve el resultado de evaluación ML.
 * @param {string} ofertaId - UUID de la oferta
 */
export const postularAOferta = (ofertaId) =>
    client.post(`/api/postulaciones/${ofertaId}`).then(r => r.data)

/**
 * Registra una postulación copiando los datos de la recomendación existente.
 * No re-evalúa el CV — usar desde "Mejor Correspondencia".
 * @param {string} ofertaId - UUID de la oferta
 */
export const postularDesdeRecomendacion = (ofertaId) =>
    client.post(`/api/postulaciones/${ofertaId}/desde-recomendacion`).then(r => r.data)

/**
 * Obtiene todas las postulaciones del usuario actual.
 */
export const getMyPostulaciones = () =>
    client.get('/api/postulaciones').then(r => r.data)
