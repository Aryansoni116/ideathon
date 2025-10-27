import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/ideathon/',
  build: {
    target: 'esnext', // Add this for Three.js compatibility
    rollupOptions: {
      external: [], // Ensure no dependencies are externalized
    }
  },
  optimizeDeps: {
    exclude: ['three', '@react-three/fiber', '@react-three/drei'] // Add this
  }
})
