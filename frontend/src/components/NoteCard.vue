<template>
  <div class="card h-full flex flex-col mx-auto w-full max-w-sm">
    <div class="relative pb-[75%] h-0 overflow-hidden rounded-t-lg">
      <img 
        :src="note.image_url" 
        :alt="note.title" 
        class="absolute inset-0 w-full h-full object-contain"
      />
    </div>
    <div class="card-body flex-grow flex flex-col">
      <h3 class="card-title text-truncate mb-2">{{ note.title }}</h3>
      <p class="text-gray-600 text-sm mb-3 flex-grow text-truncate">{{ note.description || t('noteCard.noDescription') }}</p>
      <div class="flex justify-between items-center text-sm text-gray-500 mb-3">
        <span>{{ formatDate(note.created_at) }}</span>
        <span class="badge badge-success">
          {{ t('noteCard.generated') }}
        </span>
      </div>
      <div class="flex justify-between items-center mt-auto">
        <div class="flex space-x-2">
          <button 
            v-if="showPreview" 
            @click="$emit('preview', note)"
            class="btn btn-primary text-sm"
          >
            {{ t('noteCard.preview') }}
          </button>
          <button 
            v-if="showEdit" 
            @click="$emit('edit', note)"
            class="btn btn-secondary text-sm"
          >
            {{ t('noteCard.edit') }}
          </button>
          <button 
            v-if="showDelete" 
            @click="$emit('delete', note)"
            class="btn btn-danger text-sm"
          >
            {{ t('noteCard.delete') }}
          </button>
        </div>
        <div v-if="showDownload" class="flex space-x-2">
          <button 
            @click="$emit('download', note)"
            class="text-gray-500 hover:text-gray-700"
            :title="t('noteCard.download')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
          <button 
            @click="$emit('share', note)"
            class="text-gray-500 hover:text-gray-700"
            :title="t('noteCard.share')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

// 定义属性
const props = defineProps({
  note: {
    type: Object,
    required: true
  },
  showPreview: {
    type: Boolean,
    default: true
  },
  showEdit: {
    type: Boolean,
    default: false
  },
  showDelete: {
    type: Boolean,
    default: false
  },
  showDownload: {
    type: Boolean,
    default: true
  }
})

// 初始化国际化
const { t } = useI18n()

// 定义事件
const emit = defineEmits(['preview', 'edit', 'delete', 'download', 'share'])

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}
</script>

<style scoped>
/* 可以根据需要添加特定样式 */
</style>