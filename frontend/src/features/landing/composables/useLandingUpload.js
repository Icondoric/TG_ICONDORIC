import { ref } from 'vue'
import { useRouter } from 'vue-router'

export function useLandingUpload() {
    const router = useRouter()
    const fileInputRef = ref(null)
    const isDragging = ref(false)
    const isProcessing = ref(false)
    const processingFileName = ref('')

    const triggerFileInput = () => {
        fileInputRef.value.click()
    }

    const handleDragOver = () => {
        isDragging.value = true
    }

    const handleDragLeave = () => {
        isDragging.value = false
    }

    const handleDrop = (e) => {
        isDragging.value = false
        const file = e.dataTransfer.files[0]
        if (file) validateAndProcessFile(file)
    }

    const handleFileChange = (e) => {
        const file = e.target.files[0]
        if (file) validateAndProcessFile(file)
    }

    const validateAndProcessFile = (file) => {
        if (file.type !== 'application/pdf') {
            alert('Por favor sube un archivo PDF válido')
            return
        }

        if (file.size > 2 * 1024 * 1024) {
            alert('El archivo no debe superar 2MB')
            return
        }

        processFile(file)
    }

    const processFile = (file) => {
        isProcessing.value = true
        processingFileName.value = file.name

        setTimeout(() => {
            alert('En la versión completa, serías redirigido al formulario de validación con tus datos pre-llenados.')
            isProcessing.value = false
            processingFileName.value = ''
            router.push('/register')
        }, 2000)
    }

    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    return {
        fileInputRef,
        isDragging,
        isProcessing,
        processingFileName,
        triggerFileInput,
        handleDragOver,
        handleDragLeave,
        handleDrop,
        handleFileChange,
        scrollToTop
    }
}
