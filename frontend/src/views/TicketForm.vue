<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { i18nState, t } from '../i18n.js'

const router = useRouter()

const subject = ref('')
const description = ref('')
const priority = ref('Medium')
const category = ref('General')
const file = ref(null)

const error = ref('')
const loading = ref(false)

const locale = computed(() => i18nState.locale)

const handleFileChange = (e) => {
  file.value = e.target.files[0]
}

const handleSubmit = async () => {
  error.value = ''
  if (!subject.value || subject.value.length < 5) {
    error.value = locale.value === 'ar' ? 'يجب أن يكون الموضوع 5 أحرف على الأقل.' : 'Subject must be at least 5 characters.'
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    formData.append('subject', subject.value)
    formData.append('description', description.value)
    formData.append('priority', priority.value)
    formData.append('category', category.value)
    if (file.value) {
      formData.append('attachment', file.value)
    }

    await axios.post('/api/tickets/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    router.push('/tickets')
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else if (err.response && err.response.data && err.response.data.subject) {
      error.value = err.response.data.subject[0]
    } else {
      error.value = locale.value === 'ar' ? 'فشل إنشاء التذكرة.' : 'Failed to create ticket.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div style="max-width: 800px; margin: 0 auto;">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/tickets" style="font-weight: 500;">
        {{ locale === 'ar' ? 'التذاكر' : 'Tickets' }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">{{ locale === 'ar' ? 'إنشاء تذكرة' : 'New Ticket' }}</span>
    </div>

    <div class="card">
      <div class="card-header">
        <span>{{ locale === 'ar' ? 'طلب دعم جديد' : 'New Support Request' }}</span>
      </div>
      <div class="card-body">
        <div v-if="error" class="alert alert-danger">
          <span>⚠️</span>
          <span>{{ t(error) || error }}</span>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label class="form-label">{{ locale === 'ar' ? 'الموضوع' : 'Subject' }}</label>
            <input type="text" v-model="subject" class="form-control" required :placeholder="locale === 'ar' ? 'أدخل موضوع المشكلة المحددة...' : 'Enter subject detail...'" />
          </div>

          <div class="form-group">
            <label class="form-label">{{ locale === 'ar' ? 'الوصف التفصيلي' : 'Detailed Description' }}</label>
            <textarea v-model="description" class="form-control" rows="6" required :placeholder="locale === 'ar' ? 'صف المشكلة التي تواجهها بالتفصيل...' : 'Describe your problem in detail...'"></textarea>
          </div>

          <div class="filters-grid" style="margin-bottom: 1.25rem;">
            <div class="form-group" style="margin-bottom: 0;">
              <label class="form-label">{{ locale === 'ar' ? 'الأولوية' : 'Priority' }}</label>
              <select v-model="priority" class="form-select">
                <option value="Low">{{ locale === 'ar' ? 'منخفضة' : 'Low' }}</option>
                <option value="Medium">{{ locale === 'ar' ? 'متوسطة' : 'Medium' }}</option>
                <option value="High">{{ locale === 'ar' ? 'عالية' : 'High' }}</option>
              </select>
            </div>

            <div class="form-group" style="margin-bottom: 0;">
              <label class="form-label">{{ locale === 'ar' ? 'التصنيف' : 'Category' }}</label>
              <select v-model="category" class="form-select">
                <option value="General">{{ locale === 'ar' ? 'عام' : 'General' }}</option>
                <option value="Technical">{{ locale === 'ar' ? 'تقني' : 'Technical' }}</option>
                <option value="Billing">{{ locale === 'ar' ? 'فواتير' : 'Billing' }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">{{ locale === 'ar' ? 'المرفقات (صورة)' : 'Attachment (Image)' }}</label>
            <input type="file" @change="handleFileChange" accept="image/*" class="form-control" />
          </div>

          <div style="display: flex; gap: 1rem; margin-top: 2rem;">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? (locale === 'ar' ? 'جاري الإرسال...' : 'Submitting...') : (locale === 'ar' ? 'إرسال الطلب' : 'Submit Ticket') }}
            </button>
            <button type="button" @click="$router.push('/tickets')" class="btn btn-outline">
              {{ locale === 'ar' ? 'إلغاء' : 'Cancel' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
