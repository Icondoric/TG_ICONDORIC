import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    build: {
        // Optimize chunk size
        chunkSizeWarningLimit: 1000,
        rollupOptions: {
            output: {
                // Manual chunking for better caching
                manualChunks: {
                    // Vendor chunks
                    'vue-vendor': ['vue', 'vue-router', 'pinia'],

                    // UI components chunk
                    'ui-components': [
                        './src/components/ui/Button.vue',
                        './src/components/ui/Badge.vue',
                        './src/components/ui/Card.vue',
                    ],

                    // Admin views chunk
                    'admin': [
                        './src/views/admin/AdminDashboardView.vue',
                        './src/views/admin/ProfilesAdminView.vue',
                        './src/views/admin/UsersAdminView.vue',
                        './src/views/admin/OfertasAdminView.vue',
                    ],
                },
                // Optimize asset file names
                assetFileNames: (assetInfo) => {
                    const info = assetInfo.name.split('.')
                    const ext = info[info.length - 1]
                    if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(ext)) {
                        return `assets/images/[name]-[hash][extname]`
                    } else if (/woff|woff2|eot|ttf|otf/i.test(ext)) {
                        return `assets/fonts/[name]-[hash][extname]`
                    }
                    return `assets/[name]-[hash][extname]`
                },
                chunkFileNames: 'assets/js/[name]-[hash].js',
                entryFileNames: 'assets/js/[name]-[hash].js',
            },
        },
        // Enable CSS code splitting
        cssCodeSplit: true,
        // Source maps for production debugging (optional, can be disabled)
        sourcemap: false,
        // Minification
        minify: 'terser',
        terserOptions: {
            compress: {
                drop_console: true, // Remove console.logs in production
                drop_debugger: true,
            },
        },
    },
    // Optimize dependencies
    optimizeDeps: {
        include: ['vue', 'vue-router', 'pinia'],
    },
})
