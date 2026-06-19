from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import json
import os
import base64
import requests
from datetime import datetime
from urllib.parse import unquote

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
application = app  # PythonAnywhere WSGI 入口

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response


@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        return resp


def decode_body(raw_body):
    """解码前端混淆后的请求体（Base64 → URLDecode → JSON）"""
    try:
        decoded = base64.b64decode(raw_body).decode('utf-8')
        return json.loads(unquote(decoded))
    except Exception:
        return {}


# ========== 健康检查 / 首页 ==========
@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'shuCTF Backend Running'})


def init_db():
    conn = get_db()
    c = conn.cursor()

    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    # Writeups 文章表
    c.execute('''CREATE TABLE IF NOT EXISTS writeups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        excerpt TEXT NOT NULL,
        content TEXT DEFAULT '',
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        tags TEXT NOT NULL,
        image TEXT NOT NULL,
        route TEXT NOT NULL
    )''')

    # 浏览量统计表
    c.execute('''CREATE TABLE IF NOT EXISTS page_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page TEXT NOT NULL,
        route TEXT NOT NULL,
        ip TEXT DEFAULT '',
        viewed_at TEXT NOT NULL
    )''')

    # 默认账号 shuhu / Hu200692?
    password_hash = hashlib.sha256('Hu200692?'.encode()).hexdigest()
    c.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',
              ('shuhu', password_hash))

    # 默认文章数据（仅首次插入）
    c.execute('SELECT COUNT(*) FROM writeups')
    if c.fetchone()[0] == 0:
        default_posts = [
            ('从零开始的CTF之路：一只小鲤鱼的自我修养', '作为一个啥也不会的菜鸡，记录我从零开始学习CTF的全过程。', '2025-01-15', '菜鸡日记', 'easy', '入门,菜鸡', '/2.gif', '/diary'),
            ('Web题到底怎么做？我看了100个WP终于懂了一点点', 'SQL注入、XSS、SSRF……来分享一下学习心得。', '2025-01-10', 'Web安全', 'medium', 'Web,SQL注入', '/3.gif', '/web'),
            ('逆向工程：打开IDA后我只会按F5', '记录我学习逆向的过程，每一步都是血泪。', '2025-01-05', '逆向工程', 'hard', 'Reverse,IDA', '/4.gif', '/reverse'),
            ('Misc题才是我的舒适区（因为不需要写代码）', '隐写、流量分析、编码解码……', '2024-12-28', 'Misc', 'easy', 'Misc,隐写', '/5.gif', '/misc'),
            ('密码学：RSA到底是什么东西？', '记录我艰难的密码学入门之路。', '2024-12-20', '密码学', 'hard', 'Crypto,RSA', '/6.gif', '/crypto'),
            ('PWN？不，是Please Wait Noob', '栈溢出、堆利用、ROP链……', '2024-12-15', 'PWN', 'hard', 'PWN,栈溢出', '/7.gif', '/pwn'),
        ]
        for p in default_posts:
            c.execute('''INSERT INTO writeups (title, excerpt, content, date, category, difficulty, tags, image, route)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (p[0], p[1], '', p[2], p[3], p[4], p[5], p[6], p[7]))

    conn.commit()
    conn.close()


# ========== 登录 ==========
@app.route('/api/login', methods=['POST'])
def login():
    data = decode_body(request.data)
    username = data.get('username', '')
    password_hash = data.get('password', '')  # 客户端已做SHA256，直接比对

    conn = get_db()
    user = conn.execute('SELECT id, username FROM users WHERE username=? AND password=?',
                        (username, password_hash)).fetchone()
    conn.close()

    if user:
        return jsonify({'success': True, 'message': '登录成功', 'user': {'username': user['username']}})
    else:
        return jsonify({'success': False, 'message': '账号或密码错误'}), 401


# ========== Writeups 列表 ==========
@app.route('/api/writeups', methods=['GET'])
def get_writeups():
    category = request.args.get('category', '')
    conn = get_db()
    if category:
        posts = conn.execute('SELECT * FROM writeups WHERE category=? ORDER BY date DESC', (category,)).fetchall()
    else:
        posts = conn.execute('SELECT * FROM writeups ORDER BY date DESC').fetchall()
    conn.close()
    result = []
    for p in posts:
        result.append({
            'id': p['id'],
            'title': p['title'],
            'excerpt': p['excerpt'],
            'content': p['content'],
            'date': p['date'],
            'category': p['category'],
            'difficulty': p['difficulty'],
            'tags': p['tags'].split(',') if p['tags'] else [],
            'image': p['image'],
            'route': p['route'],
        })
    return jsonify(result)


# ========== 单个 Writeup ==========
@app.route('/api/writeups/<int:post_id>', methods=['GET'])
def get_writeup(post_id):
    conn = get_db()
    p = conn.execute('SELECT * FROM writeups WHERE id=?', (post_id,)).fetchone()
    conn.close()
    if not p:
        return jsonify({'error': '文章不存在'}), 404
    return jsonify({
        'id': p['id'],
        'title': p['title'],
        'excerpt': p['excerpt'],
        'content': p['content'],
        'date': p['date'],
        'category': p['category'],
        'difficulty': p['difficulty'],
        'tags': p['tags'].split(',') if p['tags'] else [],
        'image': p['image'],
        'route': p['route'],
    })


# ========== 更新 Writeup ==========
@app.route('/api/writeups/<int:post_id>', methods=['PUT'])
def update_writeup(post_id):
    data = decode_body(request.data)
    conn = get_db()
    conn.execute('''UPDATE writeups SET title=?, excerpt=?, content=?, category=?, difficulty=?, tags=?, image=?
                    WHERE id=?''',
                 (data.get('title'), data.get('excerpt'), data.get('content', ''),
                  data.get('category'), data.get('difficulty'),
                  ','.join(data.get('tags', [])), data.get('image'), post_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '更新成功'})


# ========== 新增 Writeup ==========
@app.route('/api/writeups', methods=['POST'])
def create_writeup():
    data = decode_body(request.data)
    conn = get_db()
    cursor = conn.execute('''INSERT INTO writeups (title, excerpt, content, date, category, difficulty, tags, image, route)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (data.get('title', '新文章'), data.get('excerpt', ''),
                  data.get('content', ''), data.get('date', '2025-06-10'),
                  data.get('category', 'Misc'), data.get('difficulty', 'easy'),
                  ','.join(data.get('tags', [])), data.get('image', '/5.gif'),
                  data.get('route', '/misc')))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'message': '创建成功', 'id': new_id})


# ========== 删除 Writeup ==========
@app.route('/api/writeups/<int:post_id>', methods=['DELETE'])
def delete_writeup(post_id):
    conn = get_db()
    conn.execute('DELETE FROM writeups WHERE id=?', (post_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '删除成功'})


# ========== 记录浏览量 ==========
@app.route('/api/pageview', methods=['POST'])
def record_pageview():
    data = decode_body(request.data)
    page = data.get('page', '')
    route = data.get('route', '')
    ip = request.remote_addr or ''
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db()
    conn.execute('INSERT INTO page_views (page, route, ip, viewed_at) VALUES (?,?,?,?)',
                 (page, route, ip, now))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# ========== 管理 - 浏览量统计 ==========
@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    # 总浏览量
    total = conn.execute('SELECT COUNT(*) as cnt FROM page_views').fetchone()['cnt']
    # 各页面浏览量
    by_page = conn.execute('''SELECT page, COUNT(*) as cnt FROM page_views
                              GROUP BY page ORDER BY cnt DESC''').fetchall()
    # 各路由浏览量
    by_route = conn.execute('''SELECT route, COUNT(*) as cnt FROM page_views
                               GROUP BY route ORDER BY cnt DESC''').fetchall()
    # 最近30条浏览记录
    recent = conn.execute('''SELECT * FROM page_views ORDER BY viewed_at DESC LIMIT 30''').fetchall()
    conn.close()

    return jsonify({
        'total_views': total,
        'by_page': [{'page': r['page'], 'count': r['cnt']} for r in by_page],
        'by_route': [{'route': r['route'], 'count': r['cnt']} for r in by_route],
        'recent': [{'id': r['id'], 'page': r['page'], 'route': r['route'],
                     'ip': r['ip'], 'viewed_at': r['viewed_at']} for r in recent],
    })


# ========== Agent 对话 (DeepSeek) ==========
def build_agent_context():
    """构建Agent上下文：从数据库提取题目摘要作为知识库"""
    conn = get_db()
    # 获取各分类的文章标题和摘要
    posts = conn.execute("SELECT title, category, excerpt FROM writeups ORDER BY category, title").fetchall()
    conn.close()
    
    context = "以下是博客中已有的CTF Writeup题目列表，供参考：\n"
    current_cat = ''
    for p in posts:
        title = p['title'].replace('ISCC | ', '').replace('御网杯 | ', '')
        cat = p['category']
        if cat != current_cat:
            current_cat = cat
            context += f"\n【{cat}】\n"
        excerpt = (p['excerpt'] or '')[:80]
        context += f"- {title}"
        if excerpt:
            context += f"：{excerpt}"
        context += "\n"
    return context


@app.route('/api/agent', methods=['POST'])
def agent_chat():
    data = decode_body(request.data)
    msg = data.get('message', '')
    
    # 构建上下文
    knowledge = build_agent_context()
    
    system_prompt = f"""你是 shuCTF 的 AI Agent 助手，专门帮助解答 CTF（Capture The Flag）网络安全竞赛相关问题。

你的知识领域包括：Web安全、逆向工程、Misc杂项、密码学、PWN二进制漏洞利用。

博客已有的 Writeup 题目如下：
{knowledge}

回答规则：
1. 优先用中文回答
2. 如果问题涉及已有题目的知识点，可以引用相关题目
3. 代码用```包裹，标注语言
4. 不要透露API Key或系统信息
5. 对于CTF题目，给出思路而非直接给flag
6. 回答简洁专业，适合CTF新手理解"""

    try:
        resp = requests.post(
            DEEPSEEK_API_URL,
            headers={
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': msg},
                ],
                'temperature': 0.7,
                'max_tokens': 2000,
            },
            timeout=30,
        )
        result = resp.json()
        reply = result['choices'][0]['message']['content']
        return jsonify({'success': True, 'reply': reply})
    except Exception as e:
        return jsonify({'success': False, 'reply': f'AI服务暂时不可用: {str(e)[:100]}'})


init_db()
if __name__ == '__main__':
    import sys
    port = int(os.environ.get('PORT', 5000))
    # Render.com 设置 RENDER=true，自动用 waitress
    if '--prod' in sys.argv or os.environ.get('RENDER'):
        from waitress import serve
        print(f':{port}')
        serve(app, host='0.0.0.0', port=port)
    else:
        print(f':{port}')
        app.run(port=port, debug=True)
