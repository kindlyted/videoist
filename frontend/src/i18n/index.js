import { createI18n } from 'vue-i18n'

// 导入语言资源
import zhCN from '../locales/zh-CN.json'
import en from '../locales/en.json'

const messages = {
  'zh-CN': zhCN,
  'en': en
}

// 自动获取浏览器语言
const getLocale = () => {
  const locale = localStorage.getItem('locale') || navigator.language
  return locale.includes('zh') ? 'zh-CN' : 'en'
}

const i18n = createI18n({
  legacy: false, // 使用Composition API模式
  locale: getLocale(),
  fallbackLocale: 'en',
  messages
})

export default i18n