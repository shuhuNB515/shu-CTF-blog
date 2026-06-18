<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="login-title">登录</h2>
      <p class="login-sub">登录后查看更多 WriteUps</p>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>账号</label>
          <input v-model="username" type="text" placeholder="请输入账号" />
        </div>
        <div class="input-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" />
        </div>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>
      <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>
      <button v-if="loggedIn" class="back-btn" @click="$router.push('/')">返回首页</button>
    </div>
  </div>
</template>

<script>
import { apiPost } from '../utils/api.js'

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      errorMsg: '',
      successMsg: '',
      loading: false,
      loggedIn: false,
    }
  },
  methods: {
    async handleLogin() {
      this.errorMsg = ''
      this.successMsg = ''
      if (!this.username || !this.password) {
        this.errorMsg = '请输入账号和密码'
        return
      }
      this.loading = true
      try {
        // 密码由服务端做SHA-256哈希，前端只负责Base64混淆
        const data = await apiPost('/api/login', {
          username: this.username,
          password: this.password,
        })
        if (data.success) {
          this.successMsg = '登录成功！欢迎回来，' + data.user.username
          this.loggedIn = true
          localStorage.setItem('shuCTF_user', JSON.stringify(data.user))
          setTimeout(() => this.$router.push('/'), 1000)
        } else {
          this.errorMsg = data.message
        }
      } catch (e) {
        this.errorMsg = '连接失败: ' + (e.message || '网络错误')
      }
      this.loading = false
    },
  },
}
</script>

<style scoped>
.login-page { display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 120px 20px 60px; position: relative; z-index: 2; }
.login-card { background: rgba(20,20,40,0.8); border: 1px solid rgba(0,255,136,0.15); border-radius: 16px; padding: 50px 40px; width: 420px; max-width: 90vw; }
.login-title { font-size: 36px; color: #00ff88; text-align: center; margin-bottom: 8px; }
.login-sub { text-align: center; color: #888; font-size: 14px; margin-bottom: 30px; }
.input-group { margin-bottom: 20px; }
.input-group label { display: block; color: #aaa; font-size: 14px; margin-bottom: 8px; }
.input-group input { width: 100%; padding: 12px 16px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #fff; font-size: 16px; outline: none; transition: border-color 0.3s; box-sizing: border-box; }
.input-group input:focus { border-color: rgba(0,255,136,0.4); }
.error-msg { color: #ff4d4d; font-size: 14px; margin-bottom: 12px; text-align: center; }
.success-msg { color: #00ff88; font-size: 14px; margin-top: 16px; text-align: center; }
.login-btn { width: 100%; padding: 14px; background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); border-radius: 8px; font-size: 18px; cursor: pointer; transition: all 0.3s; }
.login-btn:hover:not(:disabled) { background: rgba(0,255,136,0.25); box-shadow: 0 0 20px rgba(0,255,136,0.15); }
.login-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.back-btn { display: block; width: 100%; padding: 12px; margin-top: 16px; background: transparent; color: #aaa; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; font-size: 16px; cursor: pointer; transition: all 0.3s; }
.back-btn:hover { color: #fff; border-color: rgba(255,255,255,0.3); }
</style>
