import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,  // Frontend nesta porta
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Backend na porta 8000
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})