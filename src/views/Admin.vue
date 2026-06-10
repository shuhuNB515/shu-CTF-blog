<template>
  <div class="admin-page">
    <h2 class="page-title">管理中心</h2>
    <p class="page-sub">查看网站浏览数据和统计信息</p>

    <div class="refresh-bar">
      <span class="last-update">上次更新: {{ lastUpdate || '加载中...' }}</span>
      <button class="refresh-btn" @click="refreshData" :disabled="loading">
        {{ loading ? '刷新中...' : '手动刷新' }}
      </button>
    </div>

    <div class="stats-cards">
      <div class="stat-card">
        <span class="stat-num">{{ stats.total_views || 0 }}</span>
        <span class="stat-label">总浏览量</span>
      </div>
      <div class="stat-card">
        <span class="stat-num">{{ pageCount }}</span>
        <span class="stat-label">页面数</span>
      </div>
    </div>

    <div class="section">
      <h3>各页面浏览量</h3>
      <div v-if="stats.by_page && stats.by_page.length" class="data-table">
        <div v-for="(item, i) in stats.by_page" :key="i" class="data-row">
          <span class="data-name">{{ item.page }}</span>
          <span class="data-value">{{ item.count }} 次</span>
        </div>
      </div>
      <p v-else class="empty">暂无数据</p>
    </div>

    <div class="section">
      <h3>各路由浏览量</h3>
      <div v-if="stats.by_route && stats.by_route.length" class="data-table">
        <div v-for="(item, i) in stats.by_route" :key="i" class="data-row">
          <span class="data-name">{{ item.route }}</span>
          <span class="data-value">{{ item.count }} 次</span>
        </div>
      </div>
      <p v-else class="empty">暂无数据</p>
    </div>

    <div class="section">
      <h3>最近浏览记录</h3>
      <div v-if="stats.recent && stats.recent.length" class="data-table">
        <div v-for="(item, i) in stats.recent" :key="i" class="data-row">
          <span class="data-name">{{ item.page }}</span>
          <span class="data-time">{{ item.viewed_at }}</span>
        </div>
      </div>
      <p v-else class="empty">暂无数据</p>
    </div>
  </div>
</template>

<script>
import { apiGet } from '../utils/api.js'

export default {
  name: 'AdminView',
  data() {
    return {
      stats: {},
      loading: false,
      lastUpdate: '',
      timer: null,
    }
  },
  computed: {
    pageCount() {
      return this.stats.by_page ? this.stats.by_page.length : 0
    },
  },
  async mounted() {
    await this.fetchStats()
    // 每30秒自动刷新
    this.timer = setInterval(() => this.fetchStats(), 30000)
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer)
  },
  methods: {
    async fetchStats() {
      this.loading = true
      try {
        this.stats = await apiGet('/api/admin/stats')
        const now = new Date()
        this.lastUpdate = now.toLocaleTimeString('zh-CN', { hour12: false })
      } catch {
        this.lastUpdate = '请求失败'
      }
      this.loading = false
    },
    async refreshData() {
      await this.fetchStats()
    },
  },
}
</script>

<style scoped>
.admin-page { padding: 120px 20px 60px; max-width: 900px; margin: 0 auto; position: relative; z-index: 2; }
.page-title { font-size: 34px; color: #00ff88; text-align: center; margin-bottom: 6px; }
.page-sub { text-align: center; color: #888; font-size: 14px; margin-bottom: 30px; }

.refresh-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding: 12px 18px; background: rgba(20,20,40,0.6); border: 1px solid rgba(0,255,136,0.08); border-radius: 10px; }
.last-update { color: #888; font-size: 13px; }
.refresh-btn { padding: 8px 20px; background: rgba(0,255,136,0.12); color: #00ff88; border: 1px solid rgba(0,255,136,0.25); border-radius: 6px; font-size: 14px; cursor: pointer; transition: all 0.3s; }
.refresh-btn:hover:not(:disabled) { background: rgba(0,255,136,0.2); }
.refresh-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.stats-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 30px; }
.stat-card { background: rgba(20,20,40,0.7); border: 1px solid rgba(0,255,136,0.1); border-radius: 12px; padding: 28px 24px; text-align: center; }
.stat-num { display: block; font-size: 42px; color: #00ff88; font-weight: bold; }
.stat-label { display: block; font-size: 14px; color: #888; margin-top: 6px; }

.section { margin-bottom: 24px; }
.section h3 { color: #ccc; font-size: 18px; margin-bottom: 12px; border-left: 3px solid #00ff88; padding-left: 10px; }
.data-table { background: rgba(20,20,40,0.7); border: 1px solid rgba(0,255,136,0.08); border-radius: 10px; overflow: hidden; }
.data-row { display: flex; justify-content: space-between; padding: 12px 18px; border-bottom: 1px solid rgba(255,255,255,0.04); color: #ccc; font-size: 14px; }
.data-row:last-child { border-bottom: none; }
.data-value { color: #00ff88; }
.data-time { color: #888; font-size: 13px; }
.empty { color: #666; text-align: center; padding: 20px; }
</style>
