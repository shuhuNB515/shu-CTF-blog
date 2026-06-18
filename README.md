# shu-CTF Blog

shu CTF 战队博客，记录 Writeup、分享安全知识。

<div align="center">
  <img src="public/doro背景.png" alt="首页背景" width="600">
</div>

## 吉祥物

<div align="center">
  <img src="public/doro1.png" width="120">
  <img src="public/doro2.png" width="120">
  <img src="public/doro3.png" width="120">
  <img src="public/doro4.png" width="120">
</div>

## 功能预览

<div align="center">
  <img src="public/maodie.gif" alt="耄耋" width="200">
  <img src="public/耄耋2.gif" alt="耄耋2" width="200">
  <img src="public/耄耋3.gif" alt="耄耋3" width="200">
  <img src="public/耄耋4.gif" alt="耄耋4" width="200">
</div>

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vue Router + Vite |
| 后端 | Python Flask |
| 数据库 | SQLite |
| AI | DeepSeek API（Agent 对话）|
| 部署 | GitHub Pages + PythonAnywhere |

## 功能

- **Writeup 展示** — 文章分类浏览，支持 Web / 逆向 / Misc / 密码学 / PWN 等分类
- **用户登录** — 密码 SHA-256 加密，请求体 Base64 混淆
- **AI Agent** — 基于 DeepSeek 的 CTF 题目解答助手
- **文章管理** — 编辑、新增、删除 Writeup
- **浏览统计** — 页面访问量记录与可视化

## 本地开发

### 前端

```bash
npm install
npm run dev
```

### 后端

```bash
cd server
pip install -r requirements.txt
python app.py
```

## 部署

- 前端构建后部署到 GitHub Pages（gh-pages 分支）
- 后端部署到 PythonAnywhere，WSGI 入口为 `app.py`

## 项目结构

```
├── public/          # 静态资源（GIF/PNG）
├── server/
│   ├── app.py       # Flask 后端 API
│   ├── data.db      # SQLite 数据库
│   └── requirements.txt
├── src/
│   ├── views/       # 页面组件
│   ├── utils/       # 工具函数（API 请求）
│   ├── router/      # 路由配置
│   ├── App.vue      # 根组件
│   └── main.js      # 入口
├── vite.config.js   # Vite 构建配置
└── package.json
```
