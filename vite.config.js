import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// base: GitHub Pages 部署路径
// - 如果仓库是 用户名.github.io → base: '/'
// - 如果仓库是 其他名称 → base: '/仓库名/'
// 构建时: npx vite build --base=/shuCTF-Blog/
const base = process.env.VITE_BASE || '/'

export default defineConfig({
  plugins: [vue()],
  base,
  build: {
    sourcemap: false,
    cssMinify: 'esbuild',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        passes: 3,
      },
      mangle: {
        toplevel: true,
        safari10: true,
      },
      output: {
        beautify: false,
        comments: false,
      },
    },
    rollupOptions: {
      output: {
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
      },
    },
  },
})
