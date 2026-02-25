import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import {
    getOferta, createOferta, updateOferta, getContactSuggestions
} from '@/features/admin/api/ofertas.api'
import { listProfiles } from '@/features/admin/api/profiles.api'

export const useOfertasStore = defineStore('ofertas', () => {
    const profiles = ref([])
    const currentOferta = ref(null)
    const suggestions = reactive({
        contact_phone: null,
        contact_email: null,
        area: null,
        ubicacion: null
    })
    const loadingSuggestions = ref(false)

    async function loadProfiles() {
        try {
            const result = await listProfiles(false)
            profiles.value = result.profiles || []
        } catch (error) {
            console.error('Error cargando perfiles:', error)
        }
    }

    async function fetchOferta(ofertaId) {
        const result = await getOferta(ofertaId)
        currentOferta.value = result
        return result
    }

    async function saveOferta(ofertaId, data) {
        if (ofertaId) {
            const result = await updateOferta(ofertaId, data)
            currentOferta.value = result
            return result
        }
        const result = await createOferta(data)
        currentOferta.value = result
        return result
    }

    async function fetchContactSuggestions(institutionId) {
        loadingSuggestions.value = true
        try {
            const result = await getContactSuggestions(institutionId)
            suggestions.contact_phone = result.contact_phone || null
            suggestions.contact_email = result.contact_email || null
            suggestions.area = result.area || null
        } catch (error) {
            console.error('Error cargando sugerencias:', error)
        } finally {
            loadingSuggestions.value = false
        }
    }

    function clearSuggestions() {
        suggestions.contact_phone = null
        suggestions.contact_email = null
        suggestions.area = null
        suggestions.ubicacion = null
    }

    return {
        profiles, currentOferta, suggestions, loadingSuggestions,
        loadProfiles, fetchOferta, saveOferta, fetchContactSuggestions, clearSuggestions
    }
})
