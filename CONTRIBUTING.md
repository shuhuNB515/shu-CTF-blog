# 贡献指南

感谢你对 shu-CTF Blog 项目的关注！欢迎提交 Writeup、修复 Bug 或添加新功能。

## 如何贡献

### 1. Fork & Clone

```bash
# Fork 后 clone 你的仓库
git clone https://github.com/YOUR_USERNAME/shu-CTF-blog.git
cd shu-CTF-blog
```

### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
```

分支命名规范：
- `feature/` — 新功能
- `fix/` — Bug 修复
- `docs/` — 文档更新
- `refactor/` — 代码重构

### 3. 开发 & 测试

```bash
# 前端
npm install
npm run dev

# 后端
cd server
pip install -r requirements.txt
python app.py
```

### 4. 提交代码

```bash
git add .
git commit -m "feat: 简短描述你的改动"
```

Commit 规范（Conventional Commits）：
- `feat:` 新功能
- `fix:` 修复 Bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 重构
- `chore:` 构建/工具变更

### 5. 提交 Pull Request

1. Push 到你的 Fork 仓库
2. 在 GitHub 上创建 Pull Request
3. 填写 PR 模板，描述改动内容和原因

## 贡献 Writeup

### 通过 Web 界面

1. 登录博客后台
2. 点击「编辑 WriteUps」
3. 填写标题、分类、难度、内容
4. 保存

### 通过代码提交

1. 在 `server/` 目录下准备文章数据
2. 通过 API 或直接操作数据库添加
3. 提交 PR

## 代码规范

### 前端（Vue）
- 组件名使用 PascalCase：`MyComponent.vue`
- Props 使用 camelCase
- CSS 使用 scoped 样式

### 后端（Python）
- 遵循 PEP 8
- 函数名使用 snake_case
- API 路由使用 kebab-case：`/api/my-endpoint`

## 问题反馈

- 提交 [Issue](https://github.com/shuhuNB515/shu-CTF-blog/issues) 描述问题
- 附上复现步骤和截图
- 标注 Bug / Feature Request / Question

## 许可

提交代码即表示你同意项目使用 MIT License 发布你的贡献。
