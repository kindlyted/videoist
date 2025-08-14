<template>
  <div class="container mx-auto px-4 py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold mb-2">整理笔记</h1>
      <p class="text-gray-600">将PDF笔记转换为可视化图片</p>
    </div>
    
    <!-- 文件上传区域 -->
    <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6 mb-8">
      <div 
        class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition-colors"
        @dragover.prevent
        @drop.prevent="handleDrop"
        @click="$refs.fileInput.click()"
      >
        <div v-if="!selectedFile" class="flex flex-col items-center justify-center">
          <svg class="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
          <p class="text-gray-600 mb-2">拖拽文件到此处或点击选择文件</p>
          <p class="text-sm text-gray-500">支持PDF格式文件</p>
        </div>
        <div v-else class="flex flex-col items-center justify-center">
          <svg class="w-12 h-12 text-blue-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="text-gray-700 mb-1">已选择文件:</p>
          <p class="text-blue-500 font-medium">{{ selectedFile.name }}</p>
        </div>
        <input 
          type="file" 
          ref="fileInput" 
          class="hidden" 
          accept=".pdf" 
          @change="handleFileSelect"
        >
      </div>
      
      <!-- 上传按钮 -->
      <div class="mt-6 flex justify-center">
        <button 
          @click="uploadFile" 
          :disabled="!selectedFile || isUploading" 
          :class="[
            'px-6 py-2 rounded-md font-medium flex items-center',
            selectedFile && !isUploading 
              ? 'bg-blue-500 text-white hover:bg-blue-600' 
              : 'bg-gray-200 text-gray-500 cursor-not-allowed'
          ]"
        >
          <svg v-if="isUploading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-if="isUploading">处理中...</span>
          <span v-else>开始转换</span>
        </button>
      </div>
    </div>
    
    <!-- 处理结果 -->
    <div v-if="resultImageUrl" class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4">转换结果</h2>
      <div class="flex justify-center">
        <img :src="resultImageUrl" alt="转换结果" class="max-w-full h-auto rounded-lg shadow-md">
      </div>
      <div class="mt-4 flex justify-center">
        <a 
          :href="resultImageUrl" 
          :download="resultImageName" 
          class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
        >
          下载图片
        </a>
      </div>
    </div>
    
    <!-- 错误信息 -->
    <div v-if="errorMessage" class="max-w-2xl mx-auto bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
      <p class="text-red-700">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import longProcessApi from '@/services/longProcessApi'

// 状态
const selectedFile = ref(null)
const isUploading = ref(false)
const resultImageUrl = ref('')
const resultImageName = ref('')
const errorMessage = ref('')

// 处理文件选择
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
    errorMessage.value = ''
  } else {
    errorMessage.value = '请选择PDF格式的文件'
  }
}

// 处理文件拖拽
const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
    errorMessage.value = ''
  } else {
    errorMessage.value = '请选择PDF格式的文件'
  }
}

// 上传文件
const uploadFile = async () => {
  if (!selectedFile.value) {
    errorMessage.value = '请先选择文件'
    return
  }
  
  isUploading.value = true
  errorMessage.value = ''
  resultImageUrl.value = ''
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await longProcessApi.post('/notes-generator', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data.success) {
      resultImageUrl.value = response.data.image_url
      resultImageName.value = selectedFile.value.name.replace('.pdf', '.png')
    } else {
      errorMessage.value = response.data.message || '转换失败'
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '上传失败，请重试'
  } finally {
    isUploading.value = false
  }
}
</script>