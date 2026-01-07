import { createRouter, createWebHistory } from 'vue-router'

import Home from './pages/Home.vue'
import Map from './pages/Map.vue'
import Routes from './pages/Routes.vue'
import AiChat from './pages/AiChat.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/map', component: Map },
  { path: '/routes', component: Routes },
  { path: '/ai-chat', component: AiChat },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
