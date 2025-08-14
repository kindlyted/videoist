<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 页面标题 -->
    <div class="mb-8 text-center flex flex-col items-center">
      <div class="flex items-center justify-center">
        <h1 class="text-3xl font-bold">AI视频创作助手</h1>
        <SparklesIcon class="h-8 w-8 text-blue-500 ml-4" />
      </div>
      <p class="text-gray-600">一键将文章转化为高质量短视频</p>
    </div>
    
    <!-- 文章网址处理卡片 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4 flex items-center">
        <LinkIcon class="h-5 w-5 mr-2 text-blue-500" />
        文章网址处理
      </h2>
      
      <!-- 文章网址输入 -->
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="articleUrl">
          文章网址
        </label>
        <input
          id="articleUrl"
          v-model="urlForm.articleUrl"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          type="url"
          placeholder="输入文章网址 (https://...)"
        />
      </div>
      
      <!-- 发布平台开关 -->
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">
          发布平台
        </label>
        <div class="flex space-x-4">
          <Switch
            id="wordpressSwitch"
            v-model="urlForm.wordpressSwitch"
            label="发布到WordPress"
            :disabled="!hasWordPressSites"
          />
          <Switch
            id="wechatSwitch"
            v-model="urlForm.wechatSwitch"
            label="发布到微信公众号"
            :disabled="!hasWeChatAccounts"
          />
        </div>
      </div>
      
      <!-- 内容模式选择 -->
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">
          内容模式
        </label>
        <div class="flex space-x-4">
          <label class="inline-flex items-center">
            <input
              id="modeRecite"
              type="radio"
              v-model="urlForm.contentMode"
              value="朗诵"
              class="form-radio"
            />
            <span class="ml-2">朗诵</span>
          </label>
          <label class="inline-flex items-center">
            <input
              id="modeDialogue"
              type="radio"
              v-model="urlForm.contentMode"
              value="对话"
              class="form-radio"
            />
            <span class="ml-2">对话</span>
          </label>
        </div>
      </div>
      
      <!-- 上传并处理按钮 -->
      <div class="flex items-center justify-between">
        <button
          id="processUrl"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center"
          @click="processUrl"
          :disabled="isProcessing"
        >
          <SpinnerIcon v-if="isProcessing" />
          <CloudArrowUpIcon v-else class="h-5 w-5 mr-2" />
          {{ isProcessing ? '处理中...' : '上传并处理' }}
        </button>
      </div>
      
      <!-- 结果显示区域 -->
      <div id="urlResults" class="mt-4 p-4 bg-gray-50 rounded" v-if="urlResults">
        <h3 class="font-semibold mb-2">处理结果</h3>
        <p><span class="font-medium">文章网址:</span> <span id="websiteUrl">{{ urlResults.url }}</span></p>
        <p><span class="font-medium">工作目录:</span> <span id="workingDir">{{ urlResults.workDir }}</span></p>
        <p><span class="font-medium">公众号状态:</span> <span id="wxStatus">{{ urlResults.wxStatus }}</span></p>
      </div>
    </div>
    
    <!-- 视频内容编辑卡片 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4 flex items-center">
        <PencilIcon class="h-5 w-5 mr-2 text-blue-500" />
        视频内容编辑
      </h2>
      
      <!-- 朗诵文稿输入框 -->
      <div class="mb-4 relative">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="article">
          朗诵文稿
        </label>
        <textarea
          id="article"
          v-model="contentForm.article"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          rows="5"
          placeholder="在此输入或粘贴朗诵文稿..."
        ></textarea>
        <div class="absolute bottom-2 right-2 text-gray-500 text-sm">
          字数: {{ characterCount }}
        </div>
      </div>
      
      <!-- 生成标题按钮 -->
      <div class="mb-4">
        <button
          id="generateTitles"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center"
          @click="generateTitle"
          :disabled="isGeneratingTitle"
        >
          <SpinnerIcon v-if="isGeneratingTitle" />
          <SparklesIcon v-else class="h-5 w-5 mr-2" />
          {{ isGeneratingTitle ? '生成中...' : '生成标题' }}
        </button>
      </div>
      
      <!-- 视频标题输入框 -->
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="title">
          视频标题
        </label>
        <input
          id="title"
          v-model="contentForm.title"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          type="text"
          placeholder="视频标题"
        />
      </div>
      
      <!-- 封面描述输入框 -->
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="cover">
          封面描述
        </label>
        <input
          id="cover"
          v-model="contentForm.cover"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          type="text"
          placeholder="封面描述文字"
        />
      </div>
      
      <!-- 语音选择 -->
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="voice">
          语音选择
        </label>
        <select
          id="voice"
          v-model="contentForm.voice"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        >
          <option value="" disabled>请选择语音</option>
          <option 
            v-for="voice in voiceOptions" 
            :key="voice.id" 
            :value="voice.id"
          >
            {{ voice.name }}
          </option>
        </select>
      </div>
    </div>
    
    <!-- 视频生成卡片 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4 flex items-center">
        <VideoCameraIcon class="h-5 w-5 mr-2 text-blue-500" />
        视频生成
      </h2>
      
      <!-- 生成视频和上传平台按钮 -->
      <div class="flex space-x-4 mb-4">
        <button
          id="generateVideo"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center"
          @click="generateVideo"
          :disabled="isGeneratingVideo"
        >
          <SpinnerIcon v-if="isGeneratingVideo" />
          <VideoCameraIcon v-else class="h-5 w-5 mr-2" />
          {{ isGeneratingVideo ? '生成中...' : '生成视频' }}
        </button>
        <button
          id="uploadVideo"
          class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center"
          @click="uploadVideo"
          :disabled="!videoGenerated"
        >
          <SpinnerIcon v-if="isUploadingVideo" />
          <CloudArrowUpIcon v-else class="h-5 w-5 mr-2" />
          <span v-if="isUploadingVideo">上传中...</span>
          <span v-else>上传平台</span>
        </button>
      </div>
      
      <!-- 预览区域 -->
      <div class="mt-4">
        <h3 class="font-semibold mb-2">预览</h3>
        
        <!-- 封面预览和视频预览并列 -->
        <div class="flex flex-wrap gap-4 mb-4">
          <!-- 封面预览 -->
          <div v-if="preview.coverImage" class="flex-1 min-w-[300px]">
            <p class="font-medium mb-2">封面预览</p>
            <img 
              id="coverImage" 
              :src="preview.coverImage" 
              alt="封面预览" 
              class="w-full h-auto rounded max-h-[300px] object-contain"
            />
          </div>
          
          <!-- 视频预览 -->
          <div v-if="preview.videoUrl" class="flex-1 min-w-[300px]">
            <p class="font-medium mb-2">视频预览</p>
            <video 
              id="outputVideo" 
              :src="preview.videoUrl" 
              controls 
              class="w-full h-auto rounded max-h-[300px]"
            ></video>
          </div>
        </div>
        
        <!-- 下载链接 -->
        <div v-if="preview.downloadLink">
          <a 
            id="downloadLink" 
            :href="preview.downloadLink" 
            download="video.mp4" 
            class="text-blue-500 hover:text-blue-700 flex items-center"
          >
            <ArrowDownTrayIcon class="h-5 w-5 mr-2" />
            下载视频
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/services/api'
import longProcessApi from '@/services/longProcessApi'
import {
  SparklesIcon,
  LinkIcon,
  PencilIcon,
  VideoCameraIcon,
  CloudArrowUpIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'
import SpinnerIcon from '@/components/SpinnerIcon.vue'
import Switch from '@/components/Switch.vue'

// URL处理表单
const urlForm = ref({
  articleUrl: '',
  wordpressSwitch: false,
  wechatSwitch: false,
  contentMode: '朗诵'
})

// 内容编辑表单
const contentForm = ref({
  article: '',
  title: '',
  cover: '',
  voice: ''
})

// 字数统计
const characterCount = ref(0)

// 获取字数统计
const getCharacterCount = async (text) => {
  try {
    const response = await longProcessApi.post('/count-characters', { text })
    characterCount.value = response.data.count
  } catch (error) {
    console.error('获取字数统计失败:', error)
    characterCount.value = 0
  }
}

// 监听文章内容变化，实时更新字数统计
watch(() => contentForm.value.article, (newText) => {
  getCharacterCount(newText)
})

// 预览数据
const preview = ref({
  coverImage: '',
  videoUrl: '',
  downloadLink: ''
})

// 状态
const isProcessing = ref(false)
const isGeneratingTitle = ref(false)
const isGeneratingVideo = ref(false)
const isUploadingVideo = ref(false)
const videoGenerated = ref(false)
const urlResults = ref(null)

// 用户凭据状态
const hasWordPressSites = ref(false)
const hasWeChatAccounts = ref(false)
const voiceOptions = ref([
  { id: 'voice1', name: '语音1' },
  { id: 'voice2', name: '语音2' },
  { id: 'voice3', name: '语音3' }
])

// 处理URL
const processUrl = async () => {
  if (!urlForm.value.articleUrl) {
    alert('请输入文章网址')
    return
  }
  
  isProcessing.value = true
  
  try {
    // 调用后端API处理URL
    const response = await longProcessApi.post('/post-article', {
      url: urlForm.value.articleUrl,
      mode: urlForm.value.contentMode,
      wordpress_switch: urlForm.value.wordpressSwitch ? 'on' : 'off',
      wechat_switch: urlForm.value.wechatSwitch ? 'on' : 'off'
    })
    
    // 处理返回结果
    urlResults.value = {
      url: response.data.website_url,
      workDir: response.data.working_dir,
      wxStatus: response.data.wx_result
    }
    
    // 填充文稿内容
    contentForm.value.article = response.data.article_text
  } catch (error) {
    console.error('处理URL失败:', error)
    alert(`处理URL失败: ${error.response?.data?.error || error.message}`)
  } finally {
    isProcessing.value = false
  }
}

// 生成标题
const generateTitle = async () => {
  if (!contentForm.value.article) {
    alert('请先输入文稿内容')
    return
  }
  
  isGeneratingTitle.value = true
  
  try {
    // 调用后端API生成标题
    // 使用longProcessApi实例，不设置超时时间
    const response = await longProcessApi.post('/generate-title', {
      text: contentForm.value.article
    })
    
    // 将后端返回的title和cover字段分别填入视频标题和封面描述文本框
    contentForm.value.title = response.data.title
    contentForm.value.cover = response.data.cover
  } catch (error) {
    console.error('生成标题失败:', error)
    alert('生成标题失败，请重试')
  } finally {
    isGeneratingTitle.value = false
  }
}

// 生成视频
const generateVideo = async () => {
  if (!contentForm.value.article || !contentForm.value.title) {
    alert('请先输入文稿内容和视频标题')
    return
  }
  
  isGeneratingVideo.value = true
  
  try {
    // 调用后端API生成视频
    // 使用longProcessApi实例，不设置超时时间
    const response = await longProcessApi.post('/generate-video', {
      text: contentForm.value.article,
      title: contentForm.value.title,
      cover: contentForm.value.cover,
      voice: contentForm.value.voice
    })
    
    // 打印响应变量用于调试
    console.log('视频生成响应:', response)
    
    // 检查后端返回的成功状态
    if (response.data.success) {
      // 使用后端返回的cover_path和video_path字段更新预览数据
      preview.value = {
        coverImage: response.data.cover_path,
        videoUrl: response.data.video_path,
        downloadLink: response.data.video_path
      }
      
      videoGenerated.value = true
    } else {
      // 处理后端返回的错误消息
      throw new Error(response.data.message || '生成视频失败')
    }
  } catch (error) {
    console.error('生成视频失败:', error)
    alert(`生成视频失败: ${error.message || '请重试'}`)
  } finally {
    isGeneratingVideo.value = false
  }
}

// 上传视频
const uploadVideo = async () => {
  if (!videoGenerated.value) {
    alert('请先生成视频')
    return
  }
  
  isUploadingVideo.value = true
  
  try {
    // 调用后端API上传视频
    // 使用longProcessApi实例，不设置超时时间
    await longProcessApi.post('/upload-video', {
      // 添加上传视频所需的参数
    })
    
    alert('视频已上传到所选平台')
  } catch (error) {
    console.error('上传视频失败:', error)
    alert('上传视频失败，请重试')
  } finally {
    isUploadingVideo.value = false
  }
}

// 获取用户凭据信息
const fetchUserCredentials = async () => {
  try {
    // 获取WordPress站点列表
    const wpResponse = await api.get('/wordpress')
    hasWordPressSites.value = wpResponse.data.length > 0 && 
      wpResponse.data.some(site => site.site_url && site.username)
    
    // 获取微信公众号列表
    const wechatResponse = await api.get('/wechat')
    hasWeChatAccounts.value = wechatResponse.data.length > 0 && 
      wechatResponse.data.some(account => account.app_id && account.app_secret)
  } catch (error) {
    console.error('获取用户凭据信息失败:', error)
    // 出错时默认禁用开关
    hasWordPressSites.value = false
    hasWeChatAccounts.value = false
  }
}

// 获取语音选项
const fetchVoiceOptions = async () => {
  try {
    // 调用后端API获取语音选项
    const response = await longProcessApi.get('/voice-options')
    // 后端返回的数据格式是 { voice_names: [...], default_voice: '...' }
    // 需要将其转换为前端期望的格式 [{ id: '...', name: '...' }, ...]
    voiceOptions.value = response.data.voice_names.map(name => ({
      id: name,
      name: name
    }))
    
    // 设置默认语音选项
    if (response.data.default_voice) {
      contentForm.value.voice = response.data.default_voice
    }
  } catch (error) {
    console.error('获取语音选项失败:', error)
    // 如果获取失败，使用模拟数据
    voiceOptions.value = [
      { id: 'xiaoyan', name: '小燕' },
      { id: 'xiaofeng', name: '小峰' },
      { id: 'xiaomei', name: '小美' }
    ]
    
    // 设置默认语音选项
    contentForm.value.voice = 'xiaoyan'
  }
}

// 组件挂载时获取语音选项和用户凭据信息
onMounted(async () => {
  fetchVoiceOptions()
  await fetchUserCredentials()
})
</script>