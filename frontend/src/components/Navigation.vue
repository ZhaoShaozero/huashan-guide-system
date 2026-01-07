<template>
  <nav class="nav">
    <router-link to="/" class="item" :class="{ active: $route.path === '/' }">首页</router-link>
    <router-link to="/map" class="item" :class="{ active: $route.path === '/map' }">景点列表</router-link>
    <router-link to="/routes" class="item" :class="{ active: $route.path === '/routes' }">推荐路线</router-link>
    <router-link to="/ai-chat" class="item" :class="{ active: $route.path === '/ai-chat' }">AI问答</router-link>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.item {
  flex: 1;
  text-align: center;
  padding: 10px;
  text-decoration: none;
  color: #333;
  border-bottom: 2px solid transparent;
}
.item.active {
  color: #667eea;
  border-bottom-color: #667eea;
}
</style>
