import axios from 'axios'

export const TranslationService = {
  async getTranslations(lang) {
    const response = await axios.get(`/api/translations/${lang}/`)
    return response.data
  }
}
