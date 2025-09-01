<template>
  <div class="px-container py-container">
    <div class="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('noteList.title') }}</h1>
      <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-space-x-3 w-full sm:w-auto">
        <input 
          v-model="searchQuery" 
          type="text" 
          :placeholder="$t('noteList.searchPlaceholder')" 
          class="form-input w-full sm:w-64"
        >
        <button 
          @click="fetchNotes" 
          class="btn btn-primary w-full sm:w-auto"
        >
          {{ $t('noteList.refresh') }}
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-10">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      <p class="mt-4 text-gray-600">{{ $t('noteList.loading') }}</p>
    </div>
    
    <div v-else-if="filteredNotes.length === 0" class="text-center py-10">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="mt-2 text-lg font-medium text-gray-900">{{ $t('noteList.noNotesFound') }}</h3>
      <p class="mt-1 text-gray-500">{{ $t('noteList.noNotesDescription') }}</p>
    </div>
    
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <NoteCard 
        v-for="note in filteredNotes" 
        :key="note.id" 
        :note="note"
        :show-preview="true"
        :show-edit="true"
        :show-delete="true"
        :show-download="true"
        @preview="previewNote"
        @download="downloadNote"
        @edit="editNote"
        @delete="requestDeleteNote"
        @share="shareNote"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import NoteCard from '@/components/NoteCard.vue'
import api from '@/services/api.js'

// 初始化国际化
const { t } = useI18n()

// 状态
const loading = ref(false)
const notes = ref([])
const searchQuery = ref('')

// 路由
const router = useRouter()

// 获取笔记
const fetchNotes = async () => {
  loading.value = true
  
  try {
    const response = await api.get('/notes');
    notes.value = response.data.data || [];
  } catch (error) {
    console.error('获取笔记失败:', error);
    notes.value = [];
  } finally {
    loading.value = false;
  }
}

// 过滤后的笔记
const filteredNotes = computed(() => {
  return notes.value.filter(note => {
    const matchesSearch = note.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         (note.description && note.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchesSearch
  })
})

// 预览笔记
const previewNote = (note) => {
  // 在新窗口中打开图片
  window.open(note.image_url, '_blank');
}

// 编辑笔记
const editNote = (note) => {
  console.log('编辑笔记:', note)
  // 这里可以导航到编辑页面
}

// 请求删除笔记
const requestDeleteNote = async (note) => {
  console.log('请求删除笔记:', note)
  
  // 显示确认对话框
  if (!confirm(t('noteList.deleteConfirm', { title: note.title }))) {
    return;
  }
  
  try {
    // 调用后端API删除笔记
    await api.delete(`/note/${note.id}`);
    
    // 从本地列表中移除笔记
    notes.value = notes.value.filter(n => n.id !== note.id);
    
    console.log('笔记删除成功');
  } catch (error) {
    console.error('删除笔记失败:', error);
    alert('删除笔记失败，请重试');
  }
}

// 下载笔记
const downloadNote = (note) => {
  // 创建一个隐藏的a标签来触发下载
  const link = document.createElement('a');
  link.href = note.image_url;
  link.download = `${note.title}.png`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// 分享笔记
const shareNote = (note) => {
  console.log('分享笔记:', note)
  // 这里可以实现分享逻辑
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// 组件挂载时获取笔记
onMounted(() => {
  fetchNotes()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>