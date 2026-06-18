<div align="center">

# 🏴 shu-CTF Blog

**shu CTF 战队博客** — 记录 Writeup、分享安全知识、探索 CTF 世界

<img src="public/doro背景.png" alt="首页背景" width="700">

</div>

---

## ✨ 吉祥物

<div align="center">
  <img src="public/doro1.png" width="140">
  <img src="public/doro2.png" width="140">
  <img src="public/doro3.png" width="140">
  <img src="public/doro4.png" width="140">
</div>

## 🎬 功能预览

<div align="center">
  <img src="public/maodie.gif" alt="耄耋" width="220">
  <img src="public/耄耋2.gif" alt="耄耋2" width="220">
  <img src="public/耄耋3.gif" alt="耄耋3" width="220">
  <img src="public/耄耋4.gif" alt="耄耋4" width="220">
</div>

---

## 🛠 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vue Router + Vite | 单页应用，组件化开发 |
| 后端 | Python Flask | RESTful API，CORS 跨域支持 |
| 数据库 | SQLite | 轻量级，零配置部署 |
| AI | DeepSeek API | Agent 对话，CTF 题目解答 |
| 部署 | GitHub Pages + PythonAnywhere | 前后端分离部署 |

## 📋 功能特性

### Writeup 展示
- 文章分类浏览：Web 安全 / 逆向工程 / Misc / 密码学 / PWN
- 支持 ISCC、御网杯等赛事题目分类
- 难度标签：Easy / Medium / Hard
- 文章详情页，支持 Markdown 内容渲染

### 用户系统
- 用户登录认证
- 密码 SHA-256 加密存储
- 请求体 Base64 混淆传输（Network 面板看不到明文）
- 登录后解锁编辑、管理功能

### AI Agent
- 基于 DeepSeek 大模型的 CTF 题目解答助手
- 自动从数据库提取题目摘要作为知识库
- 支持多轮对话，给出解题思路而非直接给 Flag

### 文章管理
- 新增、编辑、删除 Writeup
- 支持标题、摘要、正文、分类、难度、标签编辑
- 图片上传与 GIF 动图支持

### 浏览统计
- 页面访问量自动记录
- 按页面、路由分类统计
- 最近 30 条访问记录查看

---

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Python 3.8+

### 前端

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
```

### 后端

```bash
# 安装依赖
cd server
pip install -r requirements.txt

# 开发模式
python app.py

# 生产模式（waitress）
python app.py --prod
```

### 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥，用于 Agent 对话 | 是 |
| `PORT` | 后端端口，默认 5000 | 否 |

---

## 🌐 部署

### 前端（GitHub Pages）

1. 执行 `npm run build` 生成 `dist/` 目录
2. 将 `dist/` 内容推送到 `gh-pages` 分支
3. 在 GitHub 仓库 Settings → Pages 中选择 `gh-pages` 分支

### 后端（PythonAnywhere）

1. 将 `server/` 目录上传到 PythonAnywhere
2. 配置 WSGI 入口指向 `app.py` 中的 `application`
3. 设置环境变量 `DEEPSEEK_API_KEY`
4. 点击 Reload 重启服务

---

## 📁 项目结构

```
shu-CTF-blog/
├── public/                  # 静态资源
│   ├── 1.gif ~ 9.gif       # 分类图标
│   ├── doro1~4.png         # 吉祥物图片
│   ├── doro背景.png         # 首页背景
│   ├── maodie.gif           # 耄耋动图
│   └── 耄耋2~4.gif          # 功能预览动图
├── server/                  # 后端
│   ├── app.py               # Flask API（登录/文章/Agent/统计）
│   ├── data.db              # SQLite 数据库
│   ├── init_db.py           # 数据库初始化脚本
│   └── requirements.txt     # Python 依赖
├── src/                     # 前端源码
│   ├── views/               # 页面组件
│   │   ├── Home.vue         # 首页（文章列表+分类）
│   │   ├── Login.vue        # 登录页
│   │   ├── Agent.vue        # AI 对话页
│   │   ├── Admin.vue        # 管理中心（浏览统计）
│   │   ├── EditWriteup.vue  # 编辑文章
│   │   ├── PostDetail.vue   # 文章详情
│   │   ├── WriteupDetail.vue# Writeup 详情
│   │   └── ModuleList.vue   # 分类模块列表
│   ├── utils/
│   │   └── api.js           # API 请求封装（Base64 混淆）
│   ├── router/
│   │   └── index.js         # 路由配置
│   ├── App.vue              # 根组件（导航栏+雨滴动画）
│   ├── main.js              # 入口文件
│   └── style.css            # 全局样式
├── vite.config.js           # Vite 构建配置
├── package.json             # 项目依赖
└── README.md
```

---

## 🔒 安全设计

- **密码加密**：服务端 SHA-256 哈希存储，不存明文
- **请求混淆**：前端请求体 Base64 编码，Network 面板无法直接读取
- **API Key 保护**：DeepSeek Key 从环境变量读取，不硬编码在源码中
- **CORS 配置**：仅允许 `/api/*` 路径跨域访问

---

## 📄 License

MIT License
