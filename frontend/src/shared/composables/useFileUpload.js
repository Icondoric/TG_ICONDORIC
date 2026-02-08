import { ref } from 'vue'

export function useFileUpload({ maxSizeMB = 10, accept = '.pdf' } = {}) {
    const selectedFile = ref(null)
    const isDragging = ref(false)
    const error = ref(null)

    const validateAndSetFile = (file) => {
        error.value = null
        if (!file) return false

        if (accept === '.pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
            error.value = 'Solo se permiten archivos PDF'
            return false
        }

        if (file.size > maxSizeMB * 1024 * 1024) {
            error.value = `El archivo excede el tamano maximo de ${maxSizeMB}MB`
            return false
        }

        selectedFile.value = file
        return true
    }

    const handleFileSelect = (event) => {
        const file = event.target.files[0]
        validateAndSetFile(file)
    }

    const handleDrop = (event) => {
        isDragging.value = false
        const file = event.dataTransfer.files[0]
        validateAndSetFile(file)
    }

    const handleDragOver = () => {
        isDragging.value = true
    }

    const handleDragLeave = () => {
        isDragging.value = false
    }

    const reset = () => {
        selectedFile.value = null
        isDragging.value = false
        error.value = null
    }

    return {
        selectedFile,
        isDragging,
        error,
        validateAndSetFile,
        handleFileSelect,
        handleDrop,
        handleDragOver,
        handleDragLeave,
        reset
    }
}
