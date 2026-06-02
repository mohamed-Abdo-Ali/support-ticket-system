import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import './style.css'
import { i18n, t } from './i18n.js'

const locale = localStorage.getItem('locale') || 'ar'
i18n.setLocale(locale).finally(() => {
  const app = createApp(App)
  app.config.globalProperties.$t = t
  app.use(router).mount('#app')
})
