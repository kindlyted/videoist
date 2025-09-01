<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">响应式断点测试</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="p-6 bg-blue-100 rounded-lg">
        <h2 class="text-xl font-semibold mb-2">默认 (所有屏幕)</h2>
        <p>这个区块在所有屏幕尺寸下都可见。</p>
        <div class="mt-4 p-2 bg-white rounded">
          <span class="md:hidden">当前: 小屏幕 (小于 768px)</span>
        </div>
      </div>
      
      <div class="p-6 bg-green-100 rounded-lg">
        <h2 class="text-xl font-semibold mb-2">中等屏幕 (md)</h2>
        <p>这个区块在中等屏幕及以上可见。</p>
        <div class="mt-4 p-2 bg-white rounded">
          <span class="hidden md:block">当前: 中等屏幕 (768px 或更大)</span>
        </div>
      </div>
      
      <div class="p-6 bg-yellow-100 rounded-lg">
        <h2 class="text-xl font-semibold mb-2">大屏幕 (lg)</h2>
        <p>这个区块在大屏幕及以上可见。</p>
        <div class="mt-4 p-2 bg-white rounded">
          <span class="hidden lg:block">当前: 大屏幕 (1024px 或更大)</span>
        </div>
      </div>
    </div>
    
    <div class="mt-8 p-6 bg-purple-100 rounded-lg">
      <h2 class="text-xl font-semibold mb-2">汉堡菜单测试</h2>
      <div class="md:hidden">
        <p class="p-2 bg-white rounded">这个汉堡菜单应该只在小屏幕上显示</p>
      </div>
      <div class="hidden md:block">
        <p class="p-2 bg-white rounded">这个桌面菜单应该只在中等屏幕及以上显示</p>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>