import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
    base: process.env.RAILWAY_PUBLIC_DOMAIN ? '/' : '/Portfolio/',
    build: {
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'index.html'),
                project: resolve(__dirname, 'project.html'),
            },
        },
    },
})
