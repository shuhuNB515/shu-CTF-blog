// 后端API地址 — 部署到 PythonAnywhere 后在此修改
export const API_BASE = 'https://shuhunb515.pythonanywhere.com'

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
  if (!res.ok) {
    const txt = await res.text()
    throw new Error(`HTTP ${res.status}: ${txt}`)
  }
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
