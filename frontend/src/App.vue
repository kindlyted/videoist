<template>
  <div id="app" class="flex flex-col min-h-screen">
    <Navbar />
    <main class="flex-grow">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

// 在这里添加应用级别的逻辑
const userStore = useUserStore()

// 应用启动时尝试恢复用户状态
onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (token) {
    await userStore.fetchUser()
  }
})
</script>

<style>
/* 全局样式 */
@import './style.css';
</style>
