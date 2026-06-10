<template>
  <div class="app-wrapper" @mousemove="onMouseMove">
    <img class="custom-cursor" src="/1.gif" :style="{ left: cursorX + 'px', top: cursorY + 'px' }" />
    <img class="running-gif" src="/maodie.gif" />
    <div class="bg-layer" :style="{ backgroundImage: 'url(' + bgImage + ')' }"></div>
    <div class="bg-overlay"></div>
    <!-- 左侧填充 -->
    <div class="glass-side glass-left"></div>
    <!-- 右侧填充 -->
    <div class="glass-side glass-right"></div>
    <!-- 左侧交界处玻璃边框 -->
    <div class="glass-edge glass-edge-left"></div>
    <!-- 右侧交界处玻璃边框 -->
    <div class="glass-edge glass-edge-right"></div>

    <div class="rain-container" ref="rainContainer">
      <div v-for="drop in raindrops" :key="drop.id" class="raindrop" :style="drop.style"></div>
      <div v-for="splash in splashes" :key="splash.id" class="splash-group" :style="splash.groupStyle">
        <div class="ripple-circle ripple-outer" :style="{ animationDelay: '0s' }"></div>
        <div class="ripple-circle ripple-inner" :style="{ animationDelay: '0.15s' }"></div>
        <div class="pentagon-splash" :style="{ animationDelay: (Math.random() * 0.3).toFixed(2) + 's' }"></div>
      </div>
    </div>

    <header class="header">
      <div class="header-inner">
        <div class="logo" @click="$router.push('/')">
          <span class="logo-icon">&#x1f41f;</span>
          <h1>shuCTF</h1>
        </div>
        <nav class="nav">
          <router-link to="/" class="nav-link">首页</router-link>
          <a class="nav-link" @click.prevent="goSection('posts')">WriteUps</a>
          <a class="nav-link" @click.prevent="goSection('about')">关于</a>
          <template v-if="isLoggedIn">
            <router-link to="/agent" class="nav-link">Agent</router-link>
            <router-link to="/edit-writeups" class="nav-link">编辑WriteUps</router-link>
            <router-link to="/admin" class="nav-link">管理</router-link>
            <a class="nav-link nav-logout" @click.prevent="logout">退出</a>
          </template>
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link nav-login">登录</router-link>
          </template>
        </nav>
      </div>
    </header>

    <router-view />

    <footer class="footer">
      <p>&copy; 2025 CTF小鲤鱼 · 成都理工大学编外人员</p>
      <p class="footer-tagline">菜鸡虽菜，永不放弃。</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      bgImage: import.meta.env.BASE_URL + 'doro背景.png',
      cursorX: -100,
      cursorY: -100,
      isLoggedIn: false,
      raindrops: Array.from({ length: 60 }, (_, i) => {
        const size = 0.8 + Math.random() * 3.5 // 0.8~4.3px 粗细不一
        const isHeavy = size > 2.5
        const duration = isHeavy ? 0.7 + Math.random() * 0.5 : 1.2 + Math.random() * 1.6
        const left = Math.random() * 100
        const delay = Math.random() * duration * 4
        return {
          id: i,
          style: {
            left: left + '%',
            animationDelay: delay + 's',
            animationDuration: duration + 's',
            width: size + 'px',
            height: (size * 10 + 4) + 'px',
            opacity: 0.45 + Math.random() * 0.45,
          }
        }
      }),
      splashes: [],
      splashId: 0,
    }
  },
  mounted() {
    this.checkLogin()
    this.splashInterval = setInterval(() => this.createSplash(), 200)
  },
  watch: {
    '$route'() {
      this.checkLogin()
    },
  },
  beforeUnmount() {
    clearInterval(this.splashInterval)
  },
  methods: {
    checkLogin() {
      this.isLoggedIn = !!localStorage.getItem('shuCTF_user')
    },
    logout() {
      localStorage.removeItem('shuCTF_user')
      this.isLoggedIn = false
      this.$router.push('/')
    },
    onMouseMove(e) {
      this.cursorX = e.clientX
      this.cursorY = e.clientY
    },
    goSection(id) {
      if (this.$route.path !== '/') {
        this.$router.push('/')
        this.$nextTick(() => {
          const el = document.getElementById(id)
          if (el) el.scrollIntoView({ behavior: 'smooth' })
        })
      } else {
        const el = document.getElementById(id)
        if (el) el.scrollIntoView({ behavior: 'smooth' })
      }
    },
    createSplash() {
      if (!this.$refs.rainContainer) return
      const w = this.$refs.rainContainer.offsetWidth
      const x = Math.random() * w
      const bottomOffset = 5 + Math.random() * 60
      this.splashes.push({
        id: this.splashId++,
        groupStyle: {
          left: x + 'px',
          bottom: bottomOffset + 'px',
          '--scale': (0.6 + Math.random() * 0.8).toFixed(2),
        }
      })
      if (this.splashes.length > 40) this.splashes.shift()
    },
  }
}
</script>

<style>
.app-wrapper { min-height: 100vh; position: relative; cursor: none; overflow-x: hidden; font-family: Arial, sans-serif; }

.bg-layer { position: fixed; inset: 0; background-size: cover; background-position: center; background-repeat: no-repeat; z-index: -2; }
.bg-overlay { position: fixed; inset: 0; z-index: -1; }
.glass-side { position: fixed; top: 64px; bottom: 0; width: 75px; z-index: 0; }
.glass-left { left: 0; background: linear-gradient(90deg, #1a1a1a 0%, #222 50%, #2a2a2a 80%, #333 100%); border-radius: 8px 0 0 8px; box-shadow: inset 6px 0 15px rgba(255,255,255,0.04), inset -4px 0 10px rgba(0,0,0,0.25); }
.glass-right { right: 0; background: linear-gradient(270deg, #1a1a1a 0%, #222 50%, #2a2a2a 80%, #333 100%); border-radius: 0 8px 8px 0; box-shadow: inset -6px 0 15px rgba(255,255,255,0.04), inset 4px 0 10px rgba(0,0,0,0.25); }
.glass-edge { position: fixed; top: 64px; bottom: 0; width: 12px; z-index: 1; pointer-events: none; }
.glass-edge-left { left: 75px; border-radius: 8px 0 0 8px; background: linear-gradient(180deg, rgba(200,210,230,0.45), rgba(160,170,190,0.18) 30%, rgba(120,130,150,0.08) 60%, transparent); box-shadow: inset 2px 0 6px rgba(255,255,255,0.06), inset -2px 0 4px rgba(80,85,95,0.15), 3px 0 8px rgba(0,0,0,0.15); }
.glass-edge-right { right: 75px; border-radius: 0 8px 8px 0; background: linear-gradient(180deg, rgba(200,210,230,0.38), rgba(160,170,190,0.14) 30%, rgba(120,130,150,0.06) 60%, transparent); box-shadow: inset -2px 0 6px rgba(255,255,255,0.05), inset 2px 0 4px rgba(80,85,95,0.13), -3px 0 8px rgba(0,0,0,0.12); }

.custom-cursor { position: fixed; width: 48px; height: 48px; pointer-events: none; z-index: 99999; transform: translate(-50%, -50%); image-rendering: pixelated; }
.running-gif { position: fixed; bottom: 20px; width: 200px; height: auto; z-index: 99; animation: runAcross 20s linear infinite alternate; pointer-events: none; }

.header { position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(25,25,28,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(40,40,45,0.9); padding: 0 24px; height: 64px; display: flex; align-items: center; font-family: 'Freestyle Script', cursive, sans-serif; }
.header-inner { max-width: 1080px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; width: 100%; }
.logo { display: flex; align-items: center; gap: 8px; color: #00ff88; font-weight: bold; font-size: 40px; cursor: pointer; }
.logo h1 { font-size: 40px; margin: 0; }
.nav { display: flex; gap: 28px; }
.nav-link { color: #aaa; text-decoration: none; font-size: 18px; transition: all 0.3s; }
.nav-link:hover { color: #00ff88; text-shadow: 0 0 12px rgba(0,255,136,0.5); }
.nav-link.router-link-active { color: #00ff88; }
.nav-login { background: rgba(0,255,136,0.12); padding: 6px 16px; border-radius: 6px; border: 1px solid rgba(0,255,136,0.2); }
.nav-login:hover { background: rgba(0,255,136,0.2); }
.nav-logout { background: rgba(255,80,80,0.12); padding: 6px 16px; border-radius: 6px; border: 1px solid rgba(255,80,80,0.2); color: #ff6b6b !important; }
.nav-logout:hover { background: rgba(255,80,80,0.2); color: #ff4444 !important; }

.footer { text-align: center; padding: 30px 20px; color: #00ff88; font-size: 16px; position: relative; z-index: 2; background: rgba(26,26,26,0.3); backdrop-filter: blur(8px); }
.footer-tagline { margin-top: 6px; color: #00ff88; }

/* 雨滴 */
.rain-container { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.raindrop {
  position: absolute;
  top: -80px;
  background: linear-gradient(to bottom, transparent, rgba(174,194,224,0.55), rgba(200,220,255,0.7));
  border-radius: 0 0 3px 3px;
  animation: rainFall linear infinite;
  box-shadow: 0 0 4px rgba(174,194,224,0.3);
}
@keyframes rainFall {
  0%   { transform: translate(0, 0); }
  100% { transform: translate(12vw, calc(100vh + 120px)); }
}

/* 水花波纹组 */
.splash-group {
  position: absolute;
  pointer-events: none;
  transform: scale(var(--scale, 1));
}
.ripple-circle {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  animation: rippleWave 1.8s ease-out forwards;
}
.ripple-outer {
  width: 0; height: 0;
  border: 3px solid rgba(150,210,255,0.4);
  box-shadow: 0 0 12px rgba(150,210,255,0.25), 0 0 30px rgba(150,210,255,0.1);
}
.ripple-inner {
  width: 0; height: 0;
  border: 2px solid rgba(180,230,255,0.35);
  box-shadow: 0 0 8px rgba(180,230,255,0.2);
}
@keyframes rippleWave {
  0%   { width: 0; height: 0; opacity: 1; border-radius: 50% 50% 50% 50%; }
  30%  { width: 20px; height: 20px; opacity: 0.9; border-radius: 50% 50% 50% 50%; }
  60%  { width: 45px; height: 45px; opacity: 0.5; border-radius: 55% 45% 60% 40% / 40% 55% 45% 60%; }
  80%  { width: 70px; height: 70px; opacity: 0.2; border-radius: 40% 60% 35% 65% / 65% 35% 60% 40%; }
  100% { width: 90px; height: 90px; opacity: 0; border-radius: 30% 70% 50% 50% / 70% 30% 50% 50%; }
}

/* 五角形水花 */
.pentagon-splash {
  width: 10px; height: 10px;
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%, -50%);
  background: rgba(150,210,255,0.3);
  clip-path: polygon(50% 0%, 98% 37%, 79% 100%, 21% 100%, 2% 37%);
  animation: pentagonPop 1.4s ease-out forwards;
}
@keyframes pentagonPop {
  0%   { opacity: 0; transform: translate(-50%, -50%) scale(0) rotate(0deg); }
  20%  { opacity: 0.9; }
  50%  { opacity: 0.6; transform: translate(-50%, -50%) scale(1.4) rotate(120deg); }
  100% { opacity: 0; transform: translate(-50%, -50%) scale(0.6) rotate(280deg); }
}
@keyframes runAcross { 0% { left: calc(75px - 210px); transform: scaleX(1); } 49.9% { transform: scaleX(1); } 50% { left: calc(100vw - 75px - 200px); transform: scaleX(-1); } 100% { left: calc(75px - 210px); transform: scaleX(-1); } }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #555; }
</style>
