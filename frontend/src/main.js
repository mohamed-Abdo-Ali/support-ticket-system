import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import './style.css'
import { i18n } from './i18n.js'

const locale = localStorage.getItem('locale') || 'ar'
i18n.setLocale(locale).finally(() => {
  createApp(App).use(router).mount('#app')
})
