import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ModuleList from '../views/ModuleList.vue'
import WriteupDetail from '../views/WriteupDetail.vue'
import Login from '../views/Login.vue'
import Agent from '../views/Agent.vue'
import EditWriteup from '../views/EditWriteup.vue'
import Admin from '../views/Admin.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/agent', component: Agent },
  { path: '/edit-writeups', component: EditWriteup },
  { path: '/admin', component: Admin },
  // 6个模块列表页
  { path: '/web', component: ModuleList },
  { path: '/reverse', component: ModuleList },
  { path: '/misc', component: ModuleList },
  { path: '/crypto', component: ModuleList },
  { path: '/pwn', component: ModuleList },
  { path: '/diary', component: ModuleList },
  // 题目详情页
  { path: '/web/:id', component: WriteupDetail },
  { path: '/reverse/:id', component: WriteupDetail },
  { path: '/misc/:id', component: WriteupDetail },
  { path: '/crypto/:id', component: WriteupDetail },
  { path: '/pwn/:id', component: WriteupDetail },
  { path: '/diary/:id', component: WriteupDetail },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
