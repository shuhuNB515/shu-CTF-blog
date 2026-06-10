<template>
  <div class="detail-content">
    <button class="back-btn" @click="$router.push('/')">&larr; 返回首页</button>
    <div class="detail-card" v-if="post">
      <div class="detail-image">
        <img :src="post.image" :alt="post.title" />
        <span class="post-category">{{ post.category }}</span>
      </div>
      <div class="detail-body">
        <div class="post-meta">
          <span class="post-date">{{ post.date }}</span>
          <span class="post-difficulty" :class="post.difficulty">{{ post.difficulty }}</span>
        </div>
        <h1 class="detail-title">{{ post.title }}</h1>
        <p class="detail-excerpt">{{ post.excerpt }}</p>
        <div class="post-tags">
          <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiGet, apiPost } from '../utils/api.js'

export default {
  name: 'PostDetailView',
  data() {
    return {
      post: null,
    }
  },
  async mounted() {
    const postId = this.$route.meta.postId
    try {
      this.post = await apiGet(`/api/writeups/${postId}`)
      // 记录浏览量
      if (this.post && this.post.title) {
        apiPost('/api/pageview', { page: this.post.title, route: this.$route.path })
      }
    } catch { /* fallback */ }
  },
}
</script>

<style scoped>
.detail-content { padding: 120px 20px 60px; max-width: 900px; margin: 0 auto; position: relative; z-index: 2; }
.back-btn { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); padding: 10px 24px; border-radius: 8px; font-size: 16px; cursor: pointer; margin-bottom: 30px; transition: all 0.3s; }
.back-btn:hover { background: rgba(0,255,136,0.25); box-shadow: 0 0 15px rgba(0,255,136,0.2); }

.detail-card { background: rgba(20,20,40,0.75); border: 1px solid rgba(0,255,136,0.1); border-radius: 16px; overflow: hidden; }
.detail-image { position: relative; height: 350px; overflow: hidden; background: #1a1a2e; display: flex; align-items: center; justify-content: center; }
.detail-image img { max-width: 85%; max-height: 85%; width: auto; height: auto; object-fit: contain; }
.post-category { position: absolute; top: 16px; right: 16px; background: rgba(0,255,136,0.2); color: #00ff88; padding: 6px 16px; border-radius: 20px; font-size: 16px; }
.detail-body { padding: 40px; }
.post-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.post-date { font-size: 15px; color: #888; }
.post-difficulty { font-size: 14px; padding: 4px 14px; border-radius: 10px; }
.post-difficulty.easy { background: rgba(0,200,100,0.2); color: #00c864; }
.post-difficulty.medium { background: rgba(255,180,0,0.2); color: #ffb400; }
.post-difficulty.hard { background: rgba(255,60,60,0.2); color: #ff3c3c; }
.detail-title { font-size: 32px; color: #fff; margin-bottom: 20px; line-height: 1.4; }
.detail-excerpt { font-size: 20px; color: #aaa; line-height: 1.8; margin-bottom: 24px; }
.post-tags { display: flex; gap: 10px; flex-wrap: wrap; }
.tag { font-size: 14px; padding: 6px 16px; background: rgba(255,255,255,0.08); color: #ccc; border-radius: 6px; }
</style>
