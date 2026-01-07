<template>
  <div id="app" class="app-container">
    <Header />
    <Navigation />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import Navigation from './components/Navigation.vue'
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.main-content {
  flex: 1;
  max-width: 960px;
  margin: 0 auto;
  padding: 16px;
}
</style>
