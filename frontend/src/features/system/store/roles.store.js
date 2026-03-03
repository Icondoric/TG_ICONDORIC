import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchRoles, createRole, updateRole, deleteRole } from '@/features/system/api/roles.api'

export const useRolesStore = defineStore('roles', () => {
    const roles = ref([])
    const loading = ref(false)
    const error = ref(null)

    async function loadRoles() {
        loading.value = true
        error.value = null
        try {
            roles.value = await fetchRoles()
        } catch (e) {
            error.value = e.response?.data?.detail || 'Error cargando roles'
        } finally {
            loading.value = false
        }
    }

    async function createRoleAction(data) {
        const created = await createRole(data)
        roles.value.push(created)
        return created
    }

    async function updateRoleAction(id, data) {
        const updated = await updateRole(id, data)
        const idx = roles.value.findIndex(r => r.id === id)
        if (idx !== -1) roles.value[idx] = updated
        return updated
    }

    async function deleteRoleAction(id) {
        await deleteRole(id)
        roles.value = roles.value.filter(r => r.id !== id)
    }

    return { roles, loading, error, loadRoles, createRoleAction, updateRoleAction, deleteRoleAction }
})
