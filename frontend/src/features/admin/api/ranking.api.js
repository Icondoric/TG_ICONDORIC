import client from '@/shared/api/client'

/**
 * Lista todas las ofertas con estadísticas de postulaciones.
 * @param {Object} params - { tipo, is_active, include_expired, search }
 */
export const getOfertasConStats = (params = {}) =>
    client.get('/api/admin/ranking/convocatorias', { params }).then(r => r.data)

/**
 * Obtiene el ranking de candidatos para una oferta.
 * @param {string} ofertaId - UUID de la oferta
 * @param {number} topN - Número de candidatos (default: 3)
 */
export const getRankingCandidatos = (ofertaId, topN = 3) =>
    client.get(`/api/admin/ranking/convocatorias/${ofertaId}/candidatos`, {
        params: { top_n: topN }
    }).then(r => r.data)

/**
 * Genera y descarga el informe PDF formal de evaluación de candidatos.
 * @param {string} ofertaId - UUID de la oferta
 * @param {number} topN - Número de candidatos a incluir
 * @param {string} filename - Nombre sugerido del archivo descargado
 */
export const generarInforme = async (ofertaId, topN = 3, filename = 'informe-candidatos.pdf') => {
    const response = await client.get(
        `/api/admin/ranking/convocatorias/${ofertaId}/generar-informe`,
        { params: { top_n: topN }, responseType: 'blob' }
    )
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
}
