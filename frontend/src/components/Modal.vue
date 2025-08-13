<template>
  <teleport to="body">
    <div 
      v-if="visible" 
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeModal"
    >
      <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <!-- 背景遮罩 -->
        <div 
          class="fixed inset-0 transition-opacity" 
          :class="{ 'bg-black bg-opacity-50': !transparentBackdrop }"
          aria-hidden="true"
        ></div>
        
        <!-- 间距元素 -->
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        
        <!-- 模态框 -->
        <div 
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
          :class="[sizeClass, customClass]"
        >
          <!-- 头部 -->
          <div class="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex justify-between items-center">
              <div class="flex items-center">
                <div 
                  v-if="icon"
                  class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full sm:mx-0 sm:h-10 sm:w-10"
                  :class="iconBgClass"
                >
                  <component 
                    :is="icon" 
                    class="h-6 w-6"
                    :class="iconClass"
                  />
                </div>
                <div class="mt-0 sm:mt-0 sm:ml-4 sm:text-left">
                  <h3 
                    v-if="title" 
                    class="text-lg leading-6 font-medium text-gray-900"
                  >
                    {{ title }}
                  </h3>
                </div>
              </div>
              <button 
                v-if="showCloseButton"
                type="button" 
                class="text-gray-400 hover:text-gray-500 focus:outline-none"
                @click="closeModal"
              >
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <!-- 内容 -->
            <div class="mt-4">
              <slot></slot>
            </div>
          </div>
          
          <!-- 底部 -->
          <div 
            v-if="showFooter" 
            class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse"
          >
            <slot name="footer">
              <button 
                v-if="confirmText"
                type="button" 
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 sm:ml-3 sm:w-auto sm:text-sm"
                :class="confirmButtonClass"
                @click="handleConfirm"
              >
                {{ confirmText }}
              </button>
              <button 
                v-if="cancelText"
                type="button" 
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                @click="handleCancel"
              >
                {{ cancelText }}
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue'

// 定义属性
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  icon: {
    type: [String, Object],
    default: null
  },
  iconClass: {
    type: String,
    default: 'text-white'
  },
  iconBgClass: {
    type: String,
    default: 'bg-blue-100'
  },
  size: {
    type: String,
    default: 'md', // xs, sm, md, lg, xl, full
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  customClass: {
    type: String,
    default: ''
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  showFooter: {
    type: Boolean,
    default: true
  },
  confirmText: {
    type: String,
    default: '确认'
  },
  cancelText: {
    type: String,
    default: '取消'
  },
  confirmButtonClass: {
    type: String,
    default: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
  },
  transparentBackdrop: {
    type: Boolean,
    default: false
  }
})

// 定义事件
const emit = defineEmits(['update:visible', 'confirm', 'cancel', 'close'])

// 计算属性
const sizeClass = computed(() => {
  const sizeMap = {
    xs: 'sm:max-w-xs',
    sm: 'sm:max-w-sm',
    md: 'sm:max-w-md',
    lg: 'sm:max-w-lg',
    xl: 'sm:max-w-xl',
    full: 'sm:max-w-full'
  }
  return sizeMap[props.size] || sizeMap.md
})

// 关闭模态框
const closeModal = () => {
  emit('update:visible', false)
  emit('close')
}

// 确认
const handleConfirm = () => {
  emit('confirm')
  closeModal()
}

// 取消
const handleCancel = () => {
  emit('cancel')
  closeModal()
}
</script>