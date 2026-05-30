import { reactive } from 'vue'
import axios from 'axios'

export const i18nState = reactive({
  locale: localStorage.getItem('locale') || 'ar',
  translations: {},
})

export const i18n = {
  async setLocale(locale) {
    i18nState.locale = locale
    localStorage.setItem('locale', locale)
    
    const html = document.documentElement
    html.setAttribute('lang', locale)
    if (locale === 'ar') {
      html.setAttribute('dir', 'rtl')
    } else {
      html.setAttribute('dir', 'ltr')
    }

    if (locale === 'ar') {
      try {
        const response = await axios.get(`/api/translations/ar/`)
        i18nState.translations = response.data
      } catch (err) {
        console.error('Failed to load Arabic translations', err)
        i18nState.translations = {}
      }
    } else {
      i18nState.translations = {}
    }
  },

  t(key) {
    if (!key) return ''
    return i18nState.translations[key] || key
  }
}

export const t = (key) => i18n.t(key)
