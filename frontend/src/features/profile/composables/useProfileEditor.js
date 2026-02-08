import { ref, computed, onMounted } from 'vue'
import { getMyProfile, getProfileCompleteness, deleteMyProfile, updateMyProfile, uploadCV } from '@/features/profile/api/profile.api'

export function useProfileEditor() {
    const profile = ref({
        hard_skills: [],
        soft_skills: [],
        languages: [],
        education_level: null,
        experience_years: 0,
        is_complete: false,
        completeness_score: 0,
        cv_filename: null,
        cv_uploaded_at: null,
        gemini_extraction: {}
    })
    const completeness = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const showDeleteConfirm = ref(false)
    const deleting = ref(false)

    // Upload CV
    const showUploadModal = ref(false)
    const uploadFile = ref(null)
    const uploading = ref(false)
    const isDragging = ref(false)

    // Edit Modal
    const editModal = ref({ show: false, type: '', title: '' })
    const editForm = ref({
        hard_skills: [],
        soft_skills: [],
        languages: [],
        education_level: '',
        experience_years: 0
    })
    const saving = ref(false)
    const newHardSkill = ref('')
    const newSoftSkill = ref('')
    const newLanguage = ref('')

    // Computed
    const geminiEducation = computed(() => {
        return profile.value.gemini_extraction?.education || []
    })

    const geminiExperience = computed(() => {
        return profile.value.gemini_extraction?.experience || []
    })

    const geminiPersonalInfo = computed(() => {
        return profile.value.gemini_extraction?.personal_info || {}
    })

    const hasGeminiData = computed(() => {
        const extraction = profile.value.gemini_extraction
        if (!extraction) return false
        return (
            (extraction.education && extraction.education.length > 0) ||
            (extraction.experience && extraction.experience.length > 0) ||
            (extraction.hard_skills && extraction.hard_skills.length > 0) ||
            (extraction.soft_skills && extraction.soft_skills.length > 0) ||
            (extraction.personal_info && Object.keys(extraction.personal_info).length > 0)
        )
    })

    // Formatters
    const formatDate = (dateStr) => {
        if (!dateStr) return ''
        const date = new Date(dateStr)
        return date.toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        })
    }

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB', 'GB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // Actions
    const loadProfile = async () => {
        loading.value = true
        error.value = null

        try {
            const [profileData, completenessData] = await Promise.all([
                getMyProfile(),
                getProfileCompleteness()
            ])

            profile.value = profileData
            completeness.value = completenessData
        } catch (e) {
            error.value = e.response?.data?.detail || 'Error cargando el perfil'
        } finally {
            loading.value = false
        }
    }

    const deleteProfile = async () => {
        deleting.value = true

        try {
            await deleteMyProfile()
            showDeleteConfirm.value = false
            await loadProfile()
        } catch (e) {
            error.value = e.response?.data?.detail || 'Error eliminando el perfil'
        } finally {
            deleting.value = false
        }
    }

    // Upload CV handlers
    const handleFileSelect = (event) => {
        const file = event.target.files[0]
        validateAndSetFile(file)
    }

    const handleDrop = (event) => {
        isDragging.value = false
        const file = event.dataTransfer.files[0]
        validateAndSetFile(file)
    }

    const validateAndSetFile = (file) => {
        if (!file) return

        if (!file.name.toLowerCase().endsWith('.pdf')) {
            alert('Solo se permiten archivos PDF')
            return
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('El archivo excede el tamano maximo de 10MB')
            return
        }

        uploadFile.value = file
    }

    const processCV = async () => {
        if (!uploadFile.value) return

        uploading.value = true

        try {
            await uploadCV(uploadFile.value)
            showUploadModal.value = false
            uploadFile.value = null
            await loadProfile()
        } catch (e) {
            alert(e.response?.data?.detail || 'Error procesando el CV')
        } finally {
            uploading.value = false
        }
    }

    // Edit Modal handlers
    const openEditModal = (type) => {
        editModal.value.type = type
        editModal.value.show = true

        switch (type) {
            case 'skills':
                editModal.value.title = 'Editar Competencias'
                editForm.value.hard_skills = [...profile.value.hard_skills]
                editForm.value.soft_skills = [...profile.value.soft_skills]
                editForm.value.languages = [...profile.value.languages]
                break
            case 'education':
                editModal.value.title = 'Editar Formacion'
                editForm.value.education_level = profile.value.education_level || ''
                break
            case 'experience':
                editModal.value.title = 'Editar Experiencia'
                editForm.value.experience_years = profile.value.experience_years || 0
                break
        }
    }

    const closeEditModal = () => {
        editModal.value.show = false
        editModal.value.type = ''
        editModal.value.title = ''
        newHardSkill.value = ''
        newSoftSkill.value = ''
        newLanguage.value = ''
    }

    const addSkill = (field, value) => {
        if (!value || !value.trim()) return
        const trimmed = value.trim()
        if (!editForm.value[field].includes(trimmed)) {
            editForm.value[field].push(trimmed)
        }
    }

    const removeSkill = (field, index) => {
        editForm.value[field].splice(index, 1)
    }

    const saveChanges = async () => {
        saving.value = true

        try {
            const updates = {}

            switch (editModal.value.type) {
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
            }

            await updateMyProfile(updates)
            closeEditModal()
            await loadProfile()
        } catch (e) {
            alert(e.response?.data?.detail || 'Error guardando los cambios')
        } finally {
            saving.value = false
        }
    }

    onMounted(() => {
        loadProfile()
    })

    return {
        // State
        profile,
        completeness,
        loading,
        error,
        showDeleteConfirm,
        deleting,
        showUploadModal,
        uploadFile,
        uploading,
        isDragging,
        editModal,
        editForm,
        saving,
        newHardSkill,
        newSoftSkill,
        newLanguage,
        // Computed
        geminiEducation,
        geminiExperience,
        geminiPersonalInfo,
        hasGeminiData,
        // Methods
        formatDate,
        formatFileSize,
        loadProfile,
        deleteProfile,
        handleFileSelect,
        handleDrop,
        processCV,
        openEditModal,
        closeEditModal,
        addSkill,
        removeSkill,
        saveChanges
    }
}
