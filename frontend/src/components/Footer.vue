<template>
  <footer class="bg-white border-t border-gray-200">
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="md:flex md:items-center md:justify-between">
        <div class="flex justify-center md:justify-start">
          <span class="text-xl font-bold text-blue-600">Videoist</span>
        </div>
        <div class="mt-4 md:mt-0 md:order-1">
          <p class="text-center text-sm text-gray-500">
            &copy; {{ currentYear }} Videoist. 保留所有权利。
          </p>
        </div>
        <div class="mt-4 md:mt-0 md:order-2">
          <nav class="flex justify-center space-x-6">
            <a 
              v-for="item in footerLinks" 
              :key="item.name"
              :href="item.url" 
              class="text-gray-500 hover:text-gray-700 text-sm"
            >
              {{ item.name }}
            </a>
          </nav>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

// 当前年份
const currentYear = new Date().getFullYear()

// 页脚链接
const footerLinks = ref([
  { name: '关于我们', url: '#' },
  { name: '隐私政策', url: '#' },
  { name: '使用条款', url: '#' },
  { name: '联系我们', url: '#' }
])
</script>