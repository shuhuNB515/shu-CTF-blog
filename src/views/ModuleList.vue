<template>
  <div class="module-page">
    <button class="back-btn" @click="$router.push('/')">← 返回首页</button>
    <h2 class="page-title">{{ categoryLabel }}</h2>
    <p class="page-sub">共 {{ posts.length }} 篇 Writeup</p>

    <div v-if="posts.length" class="post-list">
      <article v-for="post in posts" :key="post.id" class="post-item"
               @click="$router.push('/' + routeName + '/' + post.id)">
        <div class="post-header">
          <h3 class="post-title">{{ formatTitle(post.title) }}</h3>
          <span class="post-difficulty" :class="post.difficulty">{{ post.difficulty }}</span>
        </div>
        <p class="post-excerpt">{{ post.excerpt }}</p>
        <div class="post-tags">
          <span v-for="tag in post.tags.slice(0, 4)" :key="tag" class="tag">{{ tag }}</span>
        </div>
        <span class="read-more">查看详情 &rarr;</span>
      </article>
    </div>
    <p v-else class="empty">暂无 Writeup</p>
  </div>
</template>

<script>
import { apiGet, apiPost } from '../utils/api.js'

const CAT_NAMES = {
  web: 'Web安全',
  reverse: '逆向工程',
  misc: 'Misc',
  crypto: '密码学',
  pwn: 'PWN',
  diary: '菜鸡日记',
}
const CAT_BACKEND = {
  web: 'Web安全',
  reverse: '逆向工程',
  misc: 'Misc',
  crypto: '密码学',
  pwn: 'PWN',
  diary: '菜鸡日记',
}

export default {
  name: 'ModuleListView',
  data() {
    return { posts: [] }
  },
  computed: {
    routeName() {
      return this.$route.path.replace('/', '')
    },
    categoryLabel() {
      return CAT_NAMES[this.routeName] || this.routeName
    },
    backendCategory() {
      return CAT_BACKEND[this.routeName] || 'Misc'
    },
  },
  async mounted() {
    await this.fetchPosts()
  },
  watch: {
    '$route'() { this.fetchPosts() }
  },
  methods: {
    async fetchPosts() {
      const name = this.categoryLabel
      apiPost('/api/pageview', { page: name, route: this.$route.path })
      try {
        this.posts = await apiGet('/api/writeups?category=' + encodeURIComponent(this.backendCategory))
      } catch { /* ignore */ }
    },
    formatTitle(title) {
      return title.replace(/^ISCC \| /, '').replace(/^ISCC \|/, '')
    },
  },
}
</script>

<style scoped>
.module-page { padding: 120px 20px 60px; max-width: 900px; margin: 0 auto; position: relative; z-index: 2; }
.back-btn { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); padding: 10px 24px; border-radius: 8px; font-size: 16px; cursor: pointer; margin-bottom: 30px; }
.back-btn:hover { background: rgba(0,255,136,0.25); }

.page-title { font-size: 38px; color: #00ff88; text-align: center; margin-bottom: 4px; }
.page-sub { text-align: center; color: #888; font-size: 14px; margin-bottom: 30px; }

.post-list { display: flex; flex-direction: column; gap: 14px; }
.post-item { background: rgba(20,20,40,0.65); border: 1px solid rgba(0,255,136,0.08); border-radius: 12px; padding: 22px 28px; cursor: pointer; transition: all 0.3s; }
.post-item:hover { border-color: rgba(0,255,136,0.3); transform: translateX(6px); box-shadow: 0 6px 24px rgba(0,255,136,0.08); }
.post-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.post-title { font-size: 20px; color: #fff; }
.post-difficulty { font-size: 13px; padding: 2px 12px; border-radius: 10px; }
.post-difficulty.easy { background: rgba(0,200,100,0.2); color: #00c864; }
.post-difficulty.medium { background: rgba(255,180,0,0.2); color: #ffb400; }
.post-difficulty.hard { background: rgba(255,60,60,0.2); color: #ff3c3c; }
.post-excerpt { font-size: 15px; color: #aaa; line-height: 1.6; margin-bottom: 10px; }
.post-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }
.tag { font-size: 13px; padding: 2px 10px; background: rgba(255,255,255,0.05); color: #888; border-radius: 4px; }
.read-more { font-size: 14px; color: #00ff88; }
.empty { color: #666; text-align: center; padding: 40px; }
</style>
