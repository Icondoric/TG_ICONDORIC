import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => Promise.reject(error)
)

let _authStore = null
let _router = null

export function setAuthStore(store) {
    _authStore = store
}

export function setRouter(router) {
    _router = router
}

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            if (error.response.status === 401) {
                if (_authStore) {
                    _authStore.logout()
                }
                if (_router) {
                    _router.push('/login')
                }
            } else if (error.response.status === 403) {
                if (_router) {
                    _router.push('/dashboard')
                }
            }
        }
        return Promise.reject(error)
    }
)

export const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => {
            const base64 = reader.result.split(',')[1]
            resolve(base64)
        }
        reader.onerror = (error) => reject(error)
    })
}

export default api
