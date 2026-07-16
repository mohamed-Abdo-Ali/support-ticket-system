import { computed } from 'vue'
import { i18nState, i18n } from '../i18n.js'
import { TranslationService } from '../services/TranslationService.js'

export function useTranslationViewModel() {
  const locale = computed(() => i18nState.locale)
  const translations = computed(() => i18nState.translations)

  const setLocale = async (newLocale) => {
    i18nState.locale = newLocale
    localStorage.setItem('locale', newLocale)
    
    const html = document.documentElement
    html.setAttribute('lang', newLocale)
    if (newLocale === 'ar') {
      html.setAttribute('dir', 'rtl')
    } else {
      html.setAttribute('dir', 'ltr')
    }

    if (newLocale === 'ar') {
      try {
        const data = await TranslationService.getTranslations('ar')
        i18nState.translations = data
      } catch (err) {
        console.error('Failed to load Arabic translations', err)
        i18nState.translations = {}
      }
    } else {
      i18nState.translations = {}
    }
  }

  const t = (key) => {
    return i18n.t(key)
  }

  return {
    locale,
    translations,
    setLocale,
    t
  }
}
