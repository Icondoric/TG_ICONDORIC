import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
    listProfiles, getProfile, createProfile, updateProfile,
    deleteProfile, activateProfile, listSectors
} from '@/features/admin/api/profiles.api'

export const useAdminProfilesStore = defineStore('adminProfiles', () => {
    const profiles = ref([])
    const currentProfile = ref(null)
    const isLoadingProfiles = ref(false)
    const profilesError = ref(null)
    const sectors = ref([])

    const hasActiveProfiles = computed(() => profiles.value.some(p => p.is_active))
    const activeProfiles = computed(() => profiles.value.filter(p => p.is_active))

    async function loadProfiles(includeInactive = false, sector = null) {
        isLoadingProfiles.value = true
        profilesError.value = null
        try {
            const result = await listProfiles(includeInactive, sector)
            profiles.value = result.profiles || []
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al cargar perfiles'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    async function loadProfile(profileId) {
        isLoadingProfiles.value = true
        profilesError.value = null
        try {
            const result = await getProfile(profileId)
            currentProfile.value = result
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al cargar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    async function createProfileAction(profileData) {
        isLoadingProfiles.value = true
        profilesError.value = null
        try {
            const result = await createProfile(profileData)
            profiles.value.unshift(result)
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al crear perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    async function updateProfileAction(profileId, profileData) {
        isLoadingProfiles.value = true
        profilesError.value = null
        try {
            const result = await updateProfile(profileId, profileData)
            const index = profiles.value.findIndex(p => p.id === profileId)
            if (index !== -1) profiles.value[index] = result
            if (currentProfile.value?.id === profileId) currentProfile.value = result
            return result
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al actualizar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    async function deleteProfileAction(profileId) {
        isLoadingProfiles.value = true
        profilesError.value = null
        try {
            await deleteProfile(profileId)
            const index = profiles.value.findIndex(p => p.id === profileId)
            if (index !== -1) profiles.value[index].is_active = false
            return true
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al eliminar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    async function activateProfileAction(profileId) {
        isLoadingProfiles.value = true
        profilesError.value = null
        try {
            await activateProfile(profileId)
            const index = profiles.value.findIndex(p => p.id === profileId)
            if (index !== -1) profiles.value[index].is_active = true
            return true
        } catch (error) {
            profilesError.value = error.response?.data?.detail || 'Error al activar perfil'
            throw error
        } finally {
            isLoadingProfiles.value = false
        }
    }

    async function loadSectors() {
        try {
            const result = await listSectors()
            sectors.value = result.sectors || []
            return result
        } catch (error) {
            console.error('Error cargando sectores:', error)
            return { sectors: [] }
        }
    }

    return {
        profiles, currentProfile, isLoadingProfiles, profilesError, sectors,
        hasActiveProfiles, activeProfiles,
        loadProfiles, loadProfile, createProfileAction, updateProfileAction,
        deleteProfileAction, activateProfileAction, loadSectors
    }
})
