import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ command }) => ({
  plugins: [
    vue(),
  ],
  base: command === 'build' ? '/static/' : '/', // 👈 المسار يكون /static/ فقط عند البناء، أما في التطوير فيكون /
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
}))
