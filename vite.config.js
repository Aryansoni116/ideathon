import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true
  },
  server: {
    proxy: {
      // Add proxy for your backend API if needed
      '/api': {
        target: 'http://localhost:3000', // Your backend port
        changeOrigin: true
      }
    }
  }
})
