/**
 * useAdminProfileEditor.js
 * Composable para la vista BuscarPerfiles (Admin/Operador).
 * Maneja la búsqueda de usuarios, carga de perfil y edición.
 */
import { ref, computed } from 'vue'
import api from '@/shared/api/client'

export function useAdminProfileEditor() {
    // --- Estado de lista de usuarios ---
    const users = ref([])
    const loadingUsers = ref(false)
    const searchQuery = ref('')
    const filterRole = ref('all')
    const usersPage = ref(1)
    const usersTotal = ref(0)
    const PAGE_SIZE = 20

    // --- Estado del perfil seleccionado ---
    const selectedUser = ref(null)
    const selectedProfile = ref(null)
    const loadingProfile = ref(false)
    const profileError = ref(null)

    // --- Estado del modal de edición ---
    const editModal = ref({ show: false, type: '', title: '' })
    const editForm = ref({
        hard_skills: [],
        soft_skills: [],
        languages: [],
        education_level: '',
        experience_years: 0,
        nombre_completo: '',
        direccion: '',
        telefono: '',
        email_contacto: '',
        nacionalidad: ''
    })
    const saving = ref(false)
    const newHardSkill = ref('')
    const newSoftSkill = ref('')
    const newLanguage = ref('')

    // --- Computed: gemini_extraction ---
    const geminiPersonalInfo = computed(() =>
        selectedProfile.value?.gemini_extraction?.personal_info || {}
    )
    const geminiEducation = computed(() =>
        selectedProfile.value?.gemini_extraction?.education || []
    )
    const geminiExperience = computed(() =>
        selectedProfile.value?.gemini_extraction?.experience || []
    )
    const hasGeminiData = computed(() =>
        selectedProfile.value?.cv_filename != null
    )

    // =====================================================
    // Cargar lista de usuarios
    // =====================================================
    async function loadUsers() {
        loadingUsers.value = true
        try {
            const params = new URLSearchParams({
                page: usersPage.value,
                page_size: PAGE_SIZE
            })
            if (searchQuery.value.trim()) {
                params.append('search', searchQuery.value.trim())
            }
            if (filterRole.value && filterRole.value !== 'all') {
                params.append('role', filterRole.value)
            }
            const response = await api.get(`/api/users?${params}`)
            users.value = response.data?.usuarios || response.data || []
            usersTotal.value = response.data?.total || users.value.length
        } catch (e) {
            console.error('Error loading users:', e)
            users.value = []
        } finally {
            loadingUsers.value = false
        }
    }

    // =====================================================
    // Seleccionar usuario y cargar su perfil
    // =====================================================
    async function selectUser(user) {
        selectedUser.value = user
        selectedProfile.value = null
        profileError.value = null
        loadingProfile.value = true
        try {
            const response = await api.get(`/api/users/${user.id}/profile`)
            selectedProfile.value = response.data
        } catch (e) {
            if (e.response?.status === 404) {
                profileError.value = 'Este usuario aún no tiene perfil digitalizado.'
            } else {
                profileError.value = 'Error al cargar el perfil.'
            }
        } finally {
            loadingProfile.value = false
        }
    }

    // =====================================================
    // Modal de edición
    // =====================================================
    function openEditModal(type) {
        if (!selectedProfile.value) return
        editModal.value = { show: true, type, title: '' }
        const p = selectedProfile.value

        switch (type) {
            case 'skills':
                editModal.value.title = 'Editar Habilidades e Idiomas'
                editForm.value.hard_skills = [...(p.hard_skills || [])]
                editForm.value.soft_skills = [...(p.soft_skills || [])]
                editForm.value.languages = [...(p.languages || [])]
                break
            case 'education':
                editModal.value.title = 'Editar Nivel Educativo'
                editForm.value.education_level = p.education_level || ''
                break
            case 'experience':
                editModal.value.title = 'Editar Experiencia'
                editForm.value.experience_years = p.experience_years || 0
                break
            case 'personal_info':
                editModal.value.title = 'Información Personal'
                editForm.value.nombre_completo = p.nombre_completo || ''
                editForm.value.telefono = p.telefono || ''
                editForm.value.email_contacto = p.email_contacto || ''
                editForm.value.direccion = p.direccion || ''
                editForm.value.nacionalidad = p.nacionalidad || ''
                break
        }
    }

    function closeEditModal() {
        editModal.value = { show: false, type: '', title: '' }
    }

    function addSkill(field, value) {
        if (!value?.trim()) return
        if (!editForm.value[field].includes(value.trim())) {
            editForm.value[field].push(value.trim())
        }
    }

    function removeSkill(field, index) {
        editForm.value[field].splice(index, 1)
    }

    function updateField(field, value) {
        editForm.value[field] = value
    }

    async function saveChanges() {
        if (!selectedProfile.value) return
        saving.value = true

        try {
            const updates = {}
            const type = editModal.value.type

            switch (type) {
                case 'skills':
                    updates.hard_skills = editForm.value.hard_skills
                    updates.soft_skills = editForm.value.soft_skills
                    updates.languages = editForm.value.languages
                    break
                case 'education':
                    updates.education_level = editForm.value.education_level
                    break
                case 'experience':
                    updates.experience_years = editForm.value.experience_years
                    break
                case 'personal_info':
                    updates.nombre_completo = editForm.value.nombre_completo || null
                    updates.telefono = editForm.value.telefono || null
                    updates.email_contacto = editForm.value.email_contacto || null
                    updates.direccion = editForm.value.direccion || null
                    updates.nacionalidad = editForm.value.nacionalidad || null
                    break
            }

            await api.put(`/api/users/${selectedProfile.value.usuario_id}/profile`, updates)

            // Recargar el perfil actualizado
            const response = await api.get(`/api/users/${selectedProfile.value.usuario_id}/profile`)
            selectedProfile.value = response.data
            closeEditModal()
        } catch (e) {
            console.error('Error guardando cambios:', e)
        } finally {
            saving.value = false
        }
    }

    // =====================================================
    // Helpers
    // =====================================================
    function formatDate(dateStr) {
        if (!dateStr) return '—'
        return new Date(dateStr).toLocaleDateString('es-BO', {
            year: 'numeric', month: 'short', day: 'numeric'
        })
    }

    function getRoleBadgeClass(rol) {
        const map = {
            admin: 'bg-red-100 text-red-700',
            administrador: 'bg-red-100 text-red-700',
            operador: 'bg-orange-100 text-orange-700',
            estudiante: 'bg-blue-100 text-blue-700',
            titulado: 'bg-green-100 text-green-700',
        }
        return map[rol] || 'bg-gray-100 text-gray-700'
    }

    function getUserInitial(user) {
        return (user.nombre_completo || user.email || '?')[0].toUpperCase()
    }

    return {
        // Lista
        users, loadingUsers, searchQuery, filterRole,
        usersPage, usersTotal,
        loadUsers,
        // Perfil seleccionado
        selectedUser, selectedProfile, loadingProfile, profileError,
        selectUser,
        geminiPersonalInfo, geminiEducation, geminiExperience, hasGeminiData,
        // Modal
        editModal, editForm, saving,
        newHardSkill, newSoftSkill, newLanguage,
        openEditModal, closeEditModal,
        addSkill, removeSkill, updateField, saveChanges,
        // Helpers
        formatDate, getRoleBadgeClass, getUserInitial
    }
}
