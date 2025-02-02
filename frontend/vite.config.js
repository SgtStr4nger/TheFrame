import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    host: true,  // Listen on all addresses
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
})