<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { auth } from '../auth.js'
import { i18nState, t } from '../i18n.js'

const fullname = ref('')
const email = ref('')
const password = ref('')

const error = ref('')
const message = ref('')
const loading = ref(false)
const fetching = ref(true)

const locale = computed(() => i18nState.locale)

const fetchProfile = async () => {
  fetching.value = true
  try {
    const data = await auth.fetchProfile()
    fullname.value = data.fullname || ''
    email.value = data.email || ''
  } catch (err) {
    error.value = locale.value === 'ar' ? 'فشل تحميل بيانات الملف الشخصي.' : 'Failed to load profile.'
  } finally {
    fetching.value = false
  }
}

const handleUpdate = async () => {
  error.value = ''
  message.value = ''
  loading.value = true
  try {
    await axios.post('/api/profile/', {
      fullname: fullname.value,
      email: email.value,
      password: password.value || undefined
    })
    password.value = ''
    await auth.fetchProfile()
    message.value = locale.value === 'ar' ? 'تم تحديث الملف الشخصي بنجاح.' : 'Profile updated successfully.'
  } catch (err) {
    error.value = err.response?.data?.detail || (locale.value === 'ar' ? 'فشل تحديث البيانات.' : 'Failed to update profile.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<template>
  <div style="max-width: 600px; margin: 0 auto;">
    <div class="card">
      <div class="card-header">
        <span>{{ locale === 'ar' ? 'ملفي الشخصي' : 'My Profile' }}</span>
      </div>
      <div class="card-body">
        <div v-if="fetching" style="text-align: center; padding: 2rem;">
          <p>{{ locale === 'ar' ? 'جاري التحميل...' : 'Loading...' }}</p>
        </div>

        <div v-else>
          <div v-if="error" class="alert alert-danger">
            <span>⚠️</span>
            <span>{{ t(error) || error }}</span>
          </div>

          <div v-if="message" class="alert alert-success">
            <span>✅</span>
            <span>{{ message }}</span>
          </div>

          <form @submit.prevent="handleUpdate">
            <div class="form-group">
              <label class="form-label">{{ locale === 'ar' ? 'الاسم الكامل' : 'Full Name' }}</label>
              <input type="text" v-model="fullname" class="form-control" required placeholder="Ahmed Ali..." />
            </div>

            <div class="form-group">
              <label class="form-label">{{ locale === 'ar' ? 'البريد الإلكتروني' : 'Email Address' }}</label>
              <input type="email" v-model="email" class="form-control" required placeholder="ahmed@example.com" />
            </div>

            <div class="form-group">
              <label class="form-label">{{ locale === 'ar' ? 'تعديل كلمة المرور (اختياري)' : 'Change Password (Optional)' }}</label>
              <input type="password" v-model="password" class="form-control" placeholder="••••••••" />
              <p class="text-muted" style="font-size: 0.8rem; margin-top: 0.25rem;">
                {{ locale === 'ar' ? 'اتركه فارغاً إذا كنت لا ترغب في التغيير.' : 'Leave blank if you do not want to change it.' }}
              </p>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;" :disabled="loading">
              {{ loading ? (locale === 'ar' ? 'جاري الحفظ...' : 'Saving...') : (locale === 'ar' ? 'حفظ التغييرات' : 'Save Changes') }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
