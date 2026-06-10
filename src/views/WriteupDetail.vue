<template>
  <div class="detail-page">
    <button class="back-btn" @click="$router.back()">← 返回列表</button>

    <div v-if="post" class="detail-card">
      <div class="detail-header">
        <span class="detail-category">{{ post.category }}</span>
        <h1 class="detail-title">{{ formatTitle(post.title) }}</h1>
        <div class="detail-meta">
          <span class="detail-date">{{ post.date }}</span>
          <span class="detail-difficulty" :class="post.difficulty">{{ post.difficulty }}</span>
        </div>
        <div class="detail-tags">
          <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>

      <div class="detail-body">
        <div class="content-text" v-html="renderContent(post.content)"></div>
      </div>
    </div>

    <p v-else class="loading">加载中...</p>
  </div>
</template>

<script>
import { apiGet, apiPost } from '../utils/api.js'

export default {
  name: 'WriteupDetailView',
  data() {
    return { post: null }
  },
  async mounted() {
    const id = this.$route.params.id
    try {
      this.post = await apiGet('/api/writeups/' + id)
      if (this.post && this.post.title) {
        apiPost('/api/pageview', { page: this.post.title, route: this.$route.path })
      }
    } catch { /* fallback */ }
  },
  methods: {
    formatTitle(title) {
      return title.replace(/^ISCC \| /, '').replace(/^ISCC \|/, '')
    },
    renderContent(content) {
      if (!content) return '<p style="color:#888">暂无详细内容</p>'
      // 转义HTML
      let html = content
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      // 识别代码块（``` 包裹的内容）
      html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="code-block"><code>$2</code></pre>')
      // 识别行内代码 (`code`)
      html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
      // 处理换行
      html = html.replace(/\n\n/g, '</p><p>')
      html = html.replace(/\n/g, '<br>')
      html = '<p>' + html + '</p>'
      // 修复空段落
      html = html.replace(/<p><\/p>/g, '')
      html = html.replace(/<p><br><\/p>/g, '')
      return html
    },
  },
}
</script>

<style scoped>
.detail-page { padding: 120px 20px 60px; max-width: 900px; margin: 0 auto; position: relative; z-index: 2; }
.back-btn { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); padding: 10px 24px; border-radius: 8px; font-size: 16px; cursor: pointer; margin-bottom: 30px; }
.back-btn:hover { background: rgba(0,255,136,0.25); }

.detail-card { background: rgba(20,20,40,0.75); border: 1px solid rgba(0,255,136,0.1); border-radius: 16px; overflow: hidden; }
.detail-header { padding: 36px 36px 24px; border-bottom: 1px solid rgba(0,255,136,0.08); }
.detail-category { display: inline-block; background: rgba(0,255,136,0.15); color: #00ff88; padding: 4px 14px; border-radius: 20px; font-size: 14px; margin-bottom: 12px; }
.detail-title { font-size: 32px; color: #fff; margin-bottom: 14px; line-height: 1.3; }
.detail-meta { display: flex; gap: 20px; align-items: center; margin-bottom: 14px; }
.detail-date { color: #888; font-size: 15px; }
.detail-difficulty { font-size: 13px; padding: 3px 14px; border-radius: 10px; }
.detail-difficulty.easy { background: rgba(0,200,100,0.2); color: #00c864; }
.detail-difficulty.medium { background: rgba(255,180,0,0.2); color: #ffb400; }
.detail-difficulty.hard { background: rgba(255,60,60,0.2); color: #ff3c3c; }
.detail-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.tag { font-size: 13px; padding: 3px 12px; background: rgba(255,255,255,0.05); color: #888; border-radius: 4px; }

.detail-body { padding: 36px; }
.content-text { color: #ccc; font-size: 16px; line-height: 1.9; word-wrap: break-word; }
.content-text :deep(p) { margin-bottom: 16px; }
.content-text :deep(strong) { color: #00ff88; }
.content-text :deep(.code-block) { background: rgba(0,0,0,0.4); border: 1px solid rgba(0,255,136,0.12); border-radius: 8px; padding: 16px 20px; overflow-x: auto; margin: 16px 0; font-family: 'Courier New', Consolas, monospace; font-size: 14px; line-height: 1.6; color: #b8e6b8; white-space: pre-wrap; }
.content-text :deep(.inline-code) { background: rgba(0,255,136,0.08); padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', Consolas, monospace; font-size: 14px; color: #b8e6b8; }

.loading { color: #888; text-align: center; padding: 60px; font-size: 18px; }
</style>
