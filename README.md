# shu-CTF Blog

上海大学 CTF 战队博客，记录 Writeup、分享安全知识。

## 技术栈

- **前端**: Vue 3 + Vue Router + Vite
- **后端**: Python Flask
- **数据库**: SQLite
- **AI**: DeepSeek API（Agent 对话）
- **部署**: GitHub Pages（前端）+ PythonAnywhere（后端）

## 功能

- Writeup 文章展示与分类浏览
- 用户登录认证
- AI Agent 对话（CTF 题目解答助手）
- Writeup 编辑与管理
- 浏览量统计

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
