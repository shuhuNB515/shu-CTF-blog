import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/shu-CTF-blog/',
  build: {
    sourcemap: false,
    cssMinify: 'esbuild',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router'],
        },
      },
    },
    chunkSizeWarningLimit: 600,
  },
})
