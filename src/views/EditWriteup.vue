<template>
  <div class="edit-page">
    <h2 class="page-title">编辑 WriteUps</h2>
    <p class="page-sub">新增、修改、删除文章</p>

    <div class="top-bar">
      <button class="add-btn" @click="startAdd">+ 新增 Writeup</button>
    </div>

    <!-- 新增表单 -->
    <div v-if="showAddForm" class="add-panel">
      <h3>新增文章</h3>
      <div class="form-group">
        <label>标题</label>
        <input v-model="newForm.title" placeholder="文章标题" />
      </div>
      <div class="form-group">
        <label>摘要</label>
        <textarea v-model="newForm.excerpt" rows="2" placeholder="简短摘要"></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>分类</label>
          <input v-model="newForm.category" placeholder="Web安全 / 逆向工程 / Misc / 密码学 / PWN / 菜鸡日记" />
        </div>
        <div class="form-group">
          <label>难度</label>
          <select v-model="newForm.difficulty">
            <option value="easy">easy</option>
            <option value="medium">medium</option>
            <option value="hard">hard</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label>标签（逗号分隔）</label>
        <input v-model="newTags" placeholder="Web, SQL注入" />
      </div>
      <div class="form-group">
        <label>正文内容</label>
        <textarea v-model="newForm.content" rows="6" placeholder="解题思路、代码等..."></textarea>
      </div>
      <div class="form-actions">
        <button class="save-btn" @click="createPost" :disabled="saving">{{ saving ? '创建中...' : '创建' }}</button>
        <button class="cancel-btn" @click="showAddForm = false">取消</button>
      </div>
      <p v-if="addMsg" :class="addMsgType">{{ addMsg }}</p>
    </div>

    <div class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-item" :class="{ active: editingId === post.id }">
        <div class="post-header" @click="selectPost(post)">
          <span class="post-name">{{ post.title }}</span>
          <div class="post-header-right">
            <span class="post-cat">{{ post.category }}</span>
            <button class="del-btn" @click.stop="confirmDelete(post)" title="删除">×</button>
          </div>
        </div>
        <div v-if="editingId === post.id" class="edit-form">
          <div class="form-group">
            <label>标题</label>
            <input v-model="form.title" />
          </div>
          <div class="form-group">
            <label>摘要</label>
            <textarea v-model="form.excerpt" rows="3"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>分类</label>
              <input v-model="form.category" />
            </div>
            <div class="form-group">
              <label>难度</label>
              <select v-model="form.difficulty">
                <option value="easy">easy</option>
                <option value="medium">medium</option>
                <option value="hard">hard</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>标签（逗号分隔）</label>
            <input v-model="tagsInput" placeholder="Web, SQL注入" />
          </div>
          <div class="form-group">
            <label>图片路径</label>
            <input v-model="form.image" />
          </div>
          <div class="form-group">
            <label>正文内容</label>
            <textarea v-model="form.content" rows="5"></textarea>
          </div>
          <div class="form-actions">
            <button class="save-btn" @click="savePost(post.id)" :disabled="saving">
              {{ saving ? '保存中...' : '保存修改' }}
            </button>
            <button class="cancel-btn" @click="editingId = null">取消</button>
          </div>
          <p v-if="saveMsg" class="save-msg">{{ saveMsg }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiGet, apiPost, apiPut, apiDel } from '../utils/api.js'

const CAT_ROUTE = { 'Web安全': '/web', '逆向工程': '/reverse', 'Misc': '/misc', '密码学': '/crypto', 'PWN': '/pwn', '菜鸡日记': '/diary' }
const CAT_IMAGE = { 'Web安全': '/3.gif', '逆向工程': '/4.gif', 'Misc': '/5.gif', '密码学': '/6.gif', 'PWN': '/7.gif', '菜鸡日记': '/耄耋2.gif' }

export default {
  name: 'EditWriteupView',
  data() {
    return {
      posts: [],
      editingId: null,
      form: {},
      tagsInput: '',
      saving: false,
      saveMsg: '',
      showAddForm: false,
      newForm: { title: '', excerpt: '', content: '', category: 'Misc', difficulty: 'easy' },
      newTags: '',
      addMsg: '',
      addMsgType: 'save-msg',
    }
  },
  async mounted() {
    await this.loadPosts()
  },
  methods: {
    async loadPosts() {
      try {
        this.posts = await apiGet('/api/writeups')
      } catch { /* ignore */ }
    },
    startAdd() {
      this.showAddForm = true
      this.newForm = { title: '', excerpt: '', content: '', category: 'Misc', difficulty: 'easy' }
      this.newTags = ''
      this.addMsg = ''
    },
    async createPost() {
      if (!this.newForm.title.trim()) { this.addMsg = '请输入标题'; this.addMsgType = 'err-msg'; return }
      this.saving = true
      this.addMsg = ''
      const tags = this.newTags.split(',').map(t => t.trim()).filter(t => t)
      try {
        const data = await apiPost('/api/writeups', {
          ...this.newForm,
          tags: tags.length ? tags : [this.newForm.category],
          date: new Date().toISOString().split('T')[0],
          image: CAT_IMAGE[this.newForm.category] || '/5.gif',
          route: CAT_ROUTE[this.newForm.category] || '/misc',
        })
        if (data.success) {
          this.addMsg = '创建成功！ID: ' + data.id
          this.addMsgType = 'save-msg'
          this.showAddForm = false
          await this.loadPosts()
        } else {
          this.addMsg = data.message || '创建失败'
          this.addMsgType = 'err-msg'
        }
      } catch {
        this.addMsg = '无法连接后端'
        this.addMsgType = 'err-msg'
      }
      this.saving = false
    },
    selectPost(post) {
      if (this.editingId === post.id) { this.editingId = null; return }
      this.editingId = post.id
      this.form = { ...post }
      this.tagsInput = (post.tags || []).join(',')
      this.saveMsg = ''
    },
    async savePost(id) {
      this.saving = true
      this.saveMsg = ''
      try {
        const data = await apiPut('/api/writeups/' + id, {
          ...this.form,
          tags: this.tagsInput.split(',').map(t => t.trim()).filter(t => t),
        })
        if (data.success) {
          this.saveMsg = '保存成功！'
          await this.loadPosts()
          this.editingId = null
        } else {
          this.saveMsg = '保存失败'
        }
      } catch {
        this.saveMsg = '无法连接后端'
      }
      this.saving = false
    },
    async confirmDelete(post) {
      if (!confirm('确定要删除「' + post.title + '」吗？此操作不可恢复。')) return
      try {
        const data = await apiDel('/api/writeups/' + post.id)
        if (data.success) {
          await this.loadPosts()
          if (this.editingId === post.id) this.editingId = null
        }
      } catch { /* ignore */ }
    },
  },
}
</script>

<style scoped>
.edit-page { padding: 120px 20px 60px; max-width: 900px; margin: 0 auto; position: relative; z-index: 2; }
.page-title { font-size: 34px; color: #00ff88; text-align: center; margin-bottom: 6px; }
.page-sub { text-align: center; color: #888; font-size: 14px; margin-bottom: 24px; }

.top-bar { display: flex; justify-content: flex-end; margin-bottom: 16px; }
.add-btn { padding: 10px 24px; background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); border-radius: 8px; font-size: 15px; cursor: pointer; }
.add-btn:hover { background: rgba(0,255,136,0.25); }

.add-panel { background: rgba(20,40,20,0.8); border: 1px solid rgba(0,255,136,0.2); border-radius: 12px; padding: 24px; margin-bottom: 20px; }
.add-panel h3 { color: #00ff88; font-size: 20px; margin-bottom: 16px; }

.post-list { display: flex; flex-direction: column; gap: 10px; }
.post-item { background: rgba(20,20,40,0.7); border: 1px solid rgba(0,255,136,0.08); border-radius: 10px; overflow: hidden; }
.post-item.active { border-color: rgba(0,255,136,0.3); }
.post-header { padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; }
.post-header:hover { background: rgba(255,255,255,0.03); }
.post-name { color: #ddd; font-size: 16px; flex: 1; }
.post-header-right { display: flex; align-items: center; gap: 10px; }
.post-cat { color: #00ff88; font-size: 13px; background: rgba(0,255,136,0.1); padding: 3px 10px; border-radius: 4px; }
.del-btn { width: 28px; height: 28px; background: rgba(255,60,60,0.15); color: #ff5555; border: 1px solid rgba(255,60,60,0.25); border-radius: 6px; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; line-height: 1; }
.del-btn:hover { background: rgba(255,60,60,0.3); }

.edit-form { padding: 20px 24px 24px; border-top: 1px solid rgba(255,255,255,0.06); display: flex; flex-direction: column; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { color: #aaa; font-size: 13px; }
.form-group input, .form-group textarea, .form-group select { padding: 10px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #fff; font-size: 14px; outline: none; }
.form-group input:focus, .form-group textarea:focus, .form-group select:focus { border-color: rgba(0,255,136,0.4); }
.form-group textarea { resize: vertical; }
.form-group select { color: #ddd; }
.form-group select option { background: #1a1a2e; color: #fff; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-actions { display: flex; gap: 10px; }
.save-btn { padding: 10px 24px; background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); border-radius: 6px; cursor: pointer; font-size: 14px; }
.save-btn:hover:not(:disabled) { background: rgba(0,255,136,0.25); }
.save-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.cancel-btn { padding: 10px 24px; background: transparent; color: #aaa; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; cursor: pointer; font-size: 14px; }
.cancel-btn:hover { color: #fff; border-color: rgba(255,255,255,0.3); }
.save-msg { color: #00ff88; font-size: 13px; }
.err-msg { color: #ff5555; font-size: 13px; }
</style>
