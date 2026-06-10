<template>
  <div>
    <section class="hero">
      <div class="hero-text">
        <div class="glitch-text" data-text="CTF小鲤鱼">CTF小鲤鱼</div>
        <p class="hero-subtitle">成都理工大学编外人员 · 啥也不会但爱折腾的CTF菜鸡</p>
      </div>
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-num">0</span>
          <span class="stat-label">拿过的Flag</span>
        </div>
        <div class="stat-item">
          <span class="stat-num">999+</span>
          <span class="stat-label">踩过的坑</span>
        </div>
        <div class="stat-item">
          <span class="stat-num">1</span>
          <span class="stat-label">永不放弃的心</span>
        </div>
        <div class="stat-item">
          <span class="stat-num">∞</span>
          <span class="stat-label">学习热情</span>
        </div>
      </div>
    </section>

    <section class="modules-section" id="posts">
      <h2 class="section-title">
        <span class="title-decor"></span>
         WriteUps
      </h2>
      <div class="module-grid">
        <div class="module-card" @click="$router.push('/web')">
          <img class="module-gif" src="/2.gif" />
          <h3>Web安全</h3>
          <p>SQL注入、XSS、SSRF、命令执行等Web方向Writeup</p>
          <span class="module-arrow">查看题目 &rarr;</span>
        </div>
        <div class="module-card" @click="$router.push('/reverse')">
          <img class="module-gif" src="/4.gif" />
          <h3>逆向工程</h3>
          <p>IDA反汇编、脱壳、反混淆、二进制分析</p>
          <span class="module-arrow">查看题目 &rarr;</span>
        </div>
        <div class="module-card" @click="$router.push('/misc')">
          <img class="module-gif" src="/5.gif" />
          <h3>Misc</h3>
          <p>隐写、流量分析、编码解码、取证等杂项题目</p>
          <span class="module-arrow">查看题目 &rarr;</span>
        </div>
        <div class="module-card" @click="$router.push('/crypto')">
          <img class="module-gif" src="/6.gif" />
          <h3>密码学</h3>
          <p>RSA、AES、古典密码、现代密码学分析</p>
          <span class="module-arrow">查看题目 &rarr;</span>
        </div>
        <div class="module-card" @click="$router.push('/pwn')">
          <img class="module-gif" src="/7.gif" />
          <h3>PWN</h3>
          <p>栈溢出、堆利用、ROP链、格式化字符串</p>
          <span class="module-arrow">查看题目 &rarr;</span>
        </div>
        <div class="module-card" @click="$router.push('/diary')">
          <img class="module-gif" src="/耄耋2.gif" />
          <h3>菜鸡总结</h3>
          <p>比赛心得、学习笔记、成长记录与经验总结</p>
          <span class="module-arrow">查看文章 &rarr;</span>
        </div>
      </div>
    </section>

    <section class="about-section" id="about">
      <h2 class="section-title">
        <span class="title-decor"></span>
        关于
      </h2>
      <div class="about-content">
        <div class="about-card">
          <img class="about-icon-gif" src="/耄耋2.gif" />
          <h3>我是谁</h3>
          <p>成都理工大学编外人员，一只啥也不会但热爱CTF的小鲤鱼，在网安的海洋里摸爬滚打。</p>
        </div>
        <div class="about-card">
          <img class="about-icon-gif" src="/耄耋3.gif" />
          <h3>在学什么</h3>
          <p>Web安全、逆向工程、密码学、PWN、Misc……什么都想学，什么都学不会，但从未放弃。</p>
        </div>
        <div class="about-card">
          <img class="about-icon-gif" src="/耄耋4.gif" />
          <h3>为什么写博客</h3>
          <p>记录每一次翻车和偶尔的灵光一现，希望有一天回头看，发现自己已经不是菜鸡了。</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { apiPost } from '../utils/api.js'

export default {
  name: 'HomeView',
  mounted() {
    apiPost('/api/pageview', { page: '首页', route: '/' })
  },
}
</script>

<style scoped>
.hero, .modules-section, .about-section { font-family: 'Freestyle Script', cursive, sans-serif; }
.hero { padding: 140px 0 80px; text-align: left; position: relative; z-index: 2; max-width: 1080px; margin-left: 105px; margin-right: auto; }
.hero-text { margin-bottom: 30px; }
.glitch-text { font-size: clamp(48px, 8vw, 80px); color: #00ff88; font-weight: bold; letter-spacing: 6px; animation: glitch 3s infinite; text-shadow: 0 0 10px rgba(0,255,136,0.5); }
@keyframes glitch { 0%,90%,100% { transform: translate(0); } 92% { transform: translate(-2px, 1px); } 94% { transform: translate(2px, -1px); } 96% { transform: translate(-1px, 2px); } 98% { transform: translate(1px, -2px); } }
.hero-subtitle { color: #aaa; font-size: 20px; margin-top: 16px; letter-spacing: 2px; }
.hero-stats { display: flex; justify-content: flex-start; gap: 50px; margin-top: 40px; flex-wrap: wrap; }
.stat-item { text-align: center; }
.stat-num { display: block; font-size: 40px; color: #00ff88; font-weight: bold; }
.stat-label { font-size: 16px; color: #888; margin-top: 4px; }

.modules-section { max-width: 1100px; margin: 0 auto; padding: 80px 20px 100px; position: relative; z-index: 2; }
.section-title { font-size: 36px; color: #fff; text-align: center; margin-bottom: 50px; display: inline-flex; align-items: center; gap: 12px; left: 50%; transform: translateX(-50%); position: relative; }
.title-decor { width: 30px; height: 2px; background: linear-gradient(90deg, transparent, #00ff88); }

.module-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.module-card { background: rgba(20,20,40,0.55); border: 1px solid rgba(0,255,136,0.08); border-radius: 16px; padding: 36px 24px 28px; text-align: center; cursor: pointer; transition: all 0.35s; }
.module-card:hover { transform: translateY(-8px); border-color: rgba(0,255,136,0.35); box-shadow: 0 15px 40px rgba(0,255,136,0.1); }
.module-gif { width: 80px; height: 80px; object-fit: contain; margin-bottom: 16px; }
.module-card h3 { font-size: 24px; color: #00ff88; margin-bottom: 10px; }
.module-card p { font-size: 15px; color: #aaa; line-height: 1.6; margin-bottom: 16px; min-height: 44px; }
.module-arrow { font-size: 14px; color: #00ff88; opacity: 0.7; transition: opacity 0.3s; }
.module-card:hover .module-arrow { opacity: 1; }

.about-section { max-width: 1200px; margin: 0 auto; padding: 60px 20px 100px; position: relative; z-index: 1; }
.about-content { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
.about-card { background: rgba(20,20,40,0.85); border: 1px solid rgba(0,255,136,0.1); border-radius: 12px; padding: 40px 30px; text-align: center; transition: border-color 0.3s; }
.about-card:hover { border-color: rgba(0,255,136,0.3); }
.about-icon-gif { width: 80px; height: 80px; object-fit: contain; margin-bottom: 16px; }
.about-card h3 { color: #00ff88; font-size: 22px; margin-bottom: 12px; }
.about-card p { color: #aaa; font-size: 16px; line-height: 1.7; }
</style>
