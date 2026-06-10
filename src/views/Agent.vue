<template>
  <div class="agent-page">
    <h2 class="page-title">CTF AI Agent</h2>
    <p class="page-sub">与 AI Agent 对话，获取 CTF 知识帮助</p>
    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, i) in messages" :key="i" :class="['msg', msg.role]">
        <span class="msg-text">{{ msg.text }}</span>
      </div>
      <p v-if="loading" class="msg bot"><span class="msg-text">思考中...</span></p>
    </div>
    <div class="chat-input">
      <input v-model="input" @keyup.enter="send" type="text" placeholder="输入你的问题..." />
      <button @click="send" :disabled="loading || !input.trim()">发送</button>
    </div>
  </div>
</template>

<script>
import { apiPost } from '../utils/api.js'

export default {
  name: 'AgentView',
  data() {
    return {
      input: '',
      messages: [
        { role: 'bot', text: '你好！我是 shuCTF 的 AI Agent，你可以向我咨询 CTF 相关的问题。' }
      ],
      loading: false,
    }
  },
  methods: {
    async send() {
      const msg = this.input.trim()
      if (!msg) return
      this.messages.push({ role: 'user', text: msg })
      this.input = ''
      this.loading = true
      this.$nextTick(() => this.scrollBottom())
      try {
        const data = await apiPost('/api/agent', { message: msg })
        this.messages.push({ role: 'bot', text: data.reply })
      } catch {
        this.messages.push({ role: 'bot', text: '无法连接到后端服务，请确认服务器已启动。' })
      }
      this.loading = false
      this.$nextTick(() => this.scrollBottom())
    },
    scrollBottom() {
      const el = this.$refs.chatBox
      if (el) el.scrollTop = el.scrollHeight
    },
  },
}
</script>

<style scoped>
.agent-page { padding: 120px 20px 60px; max-width: 800px; margin: 0 auto; position: relative; z-index: 2; }
.page-title { font-size: 34px; color: #00ff88; text-align: center; margin-bottom: 6px; }
.page-sub { text-align: center; color: #888; font-size: 14px; margin-bottom: 30px; }

.chat-box { background: rgba(20,20,40,0.7); border: 1px solid rgba(0,255,136,0.1); border-radius: 14px; padding: 24px; height: 450px; overflow-y: auto; margin-bottom: 16px; display: flex; flex-direction: column; gap: 12px; }
.msg { display: flex; }
.msg.user { justify-content: flex-end; }
.msg-text { max-width: 75%; padding: 10px 16px; border-radius: 10px; font-size: 15px; line-height: 1.6; }
.msg.user .msg-text { background: rgba(0,255,136,0.15); color: #e0ffe0; border: 1px solid rgba(0,255,136,0.2); }
.msg.bot .msg-text { background: rgba(255,255,255,0.06); color: #ccc; border: 1px solid rgba(255,255,255,0.08); }

.chat-input { display: flex; gap: 10px; }
.chat-input input { flex: 1; padding: 12px 16px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #fff; font-size: 15px; outline: none; }
.chat-input input:focus { border-color: rgba(0,255,136,0.4); }
.chat-input button { padding: 12px 24px; background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); border-radius: 8px; font-size: 15px; cursor: pointer; }
.chat-input button:hover:not(:disabled) { background: rgba(0,255,136,0.25); }
.chat-input button:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
