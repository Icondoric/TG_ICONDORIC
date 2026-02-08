import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@/style.css'
import '@/shared/assets/styles/design-tokens.css'
import App from './App.vue'
import router from './router'
import { setAuthStore, setRouter } from '@/shared/api/client'
import { useAuthStore } from '@/features/auth/store/auth.store'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Wire up the shared API client with auth store and router
const authStore = useAuthStore()
setAuthStore(authStore)
setRouter(router)

app.mount('#app')
