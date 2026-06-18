# API 文档

后端 API 基础地址：`https://shuhunb515.pythonanywhere.com`

> 所有 POST/PUT 请求体使用 Base64(URLDecode(JSON)) 混淆编码，Content-Type 为 `text/plain`

---

## 健康检查

### `GET /`

返回服务状态。

**响应**：
```json
{
  "status": "ok",
  "message": "shuCTF Backend Running"
}
```

---

## 用户认证

### `POST /api/login`

用户登录。

**请求体**（混淆前）：
```json
{
  "username": "shuhu",
  "password": "明文密码"
}
```

**成功响应** `200`：
```json
{
  "success": true,
  "message": "登录成功",
  "user": {
    "username": "shuhu"
  }
}
```

**失败响应** `401`：
```json
{
  "success": false,
  "message": "账号或密码错误"
}
```

> 密码在服务端进行 SHA-256 哈希后与数据库比对，不存储明文。

---

## Writeup 文章

### `GET /api/writeups`

获取文章列表。

**查询参数**：
| 参数 | 类型 | 说明 |
|------|------|------|
| category | string | 可选，按分类筛选 |

**响应**：
```json
[
  {
    "id": 1,
    "title": "文章标题",
    "excerpt": "摘要",
    "content": "正文内容",
    "date": "2025-01-15",
    "category": "Web安全",
    "difficulty": "medium",
    "tags": ["SQL注入", "Web"],
    "image": "/2.gif",
    "route": "/web"
  }
]
```

### `GET /api/writeups/:id`

获取单篇文章详情。

**路径参数**：
| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 文章 ID |

**成功响应** `200`：返回单个文章对象

**失败响应** `404`：
```json
{
  "error": "文章不存在"
}
```

### `POST /api/writeups`

创建新文章（需登录）。

**请求体**（混淆前）：
```json
{
  "title": "新文章",
  "excerpt": "摘要",
  "content": "正文",
  "date": "2025-06-10",
  "category": "Misc",
  "difficulty": "easy",
  "tags": ["入门"],
  "image": "/5.gif",
  "route": "/misc"
}
```

**响应**：
```json
{
  "success": true,
  "message": "创建成功",
  "id": 75
}
```

### `PUT /api/writeups/:id`

更新文章（需登录）。

**请求体**：同创建，所有字段可选。

**响应**：
```json
{
  "success": true,
  "message": "更新成功"
}
```

### `DELETE /api/writeups/:id`

删除文章（需登录）。

**响应**：
```json
{
  "success": true,
  "message": "删除成功"
}
```

---

## AI Agent

### `POST /api/agent`

与 AI Agent 对话。

**请求体**（混淆前）：
```json
{
  "message": "SQL注入怎么学？"
}
```

**成功响应**：
```json
{
  "success": true,
  "reply": "SQL注入是Web安全中最常见的漏洞类型之一..."
}
```

**失败响应**：
```json
{
  "success": false,
  "reply": "AI服务暂时不可用: error message"
}
```

> Agent 自动从数据库提取已有 Writeup 摘要作为知识库上下文。

---

## 浏览统计

### `POST /api/pageview`

记录页面浏览。

**请求体**（混淆前）：
```json
{
  "page": "首页",
  "route": "/"
}
```

**响应**：
```json
{
  "success": true
}
```

### `GET /api/admin/stats`

获取浏览统计数据。

**响应**：
```json
{
  "total_views": 1234,
  "by_page": [
    { "page": "首页", "count": 800 }
  ],
  "by_route": [
    { "route": "/", "count": 800 }
  ],
  "recent": [
    {
      "id": 1,
      "page": "首页",
      "route": "/",
      "ip": "1.2.3.4",
      "viewed_at": "2025-06-10 12:00:00"
    }
  ]
}
```

---

## 请求体编码说明

前端发送请求时，请求体经过以下编码：

```
原始 JSON → URL 编码 → Base64 编码
```

示例：
```javascript
// 原始数据
{ "username": "shuhu", "password": "123456" }

// URL 编码后
%7B%22username%22%3A%22shuhu%22%2C%22password%22%3A%22123456%22%7D

// Base64 编码后（实际发送的内容）
JTdCJTIydXNlcm5hbWUlMjIlM0ElMjJzaHVodSUyMiUyQyUyMnBhc3N3b3JkJTIyJTNBJTIyMTIzNDU2JTIyJTdE
```

服务端解码流程：`Base64 → URL 解码 → JSON.parse`
