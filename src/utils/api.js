// 后端API地址
// 开发环境: VITE_API_BASE 不设置，默认 http://localhost:5000
// 生产环境: 构建时设置 VITE_API_BASE=https://你的后端地址.onrender.com
export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

// 请求体混淆：Base64(URLEncode(JSON))
function obfuscateBody(data) {
  return btoa(encodeURIComponent(JSON.stringify(data)))
}

// POST 请求（请求体混淆，Network面板看到的是Base64乱码）
export async function apiPost(path, data) {
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: obfuscateBody(data),
  })
  return res.json()
}

// GET 请求
export async function apiGet(path) {
  const res = await fetch(API_BASE + path)
  return res.json()
}

// PUT 请求（请求体混淆）
export async function apiPut(path, data) {
  const res = await fetch(API_BASE + path, {
    method: 'PUT',
    headers: { 'Content-Type': 'text/plain' },
    body: obfuscateBody(data),
  })
  return res.json()
}

// DELETE 请求
export async function apiDel(path) {
  const res = await fetch(API_BASE + path, { method: 'DELETE' })
  return res.json()
}

// SHA-256 哈希（客户端密码加密）
export async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message)
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
}
