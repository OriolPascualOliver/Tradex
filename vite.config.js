import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/fixhub/' // <-- cambia esto si usas otro nombre de repo
})
