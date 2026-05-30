<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../auth.js'
import { i18nState, t } from '../i18n.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const locale = computed(() => i18nState.locale)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = locale.value === 'ar' ? 'فشل تسجيل الدخول. يرجى التحقق من البيانات.' : 'Login failed. Please check credentials.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="auth-title">{{ locale === 'ar' ? 'تسجيل الدخول' : 'Sign In' }}</h2>
      
      <div v-if="error" class="alert alert-danger">
        <span>⚠️</span>
        <span>{{ t(error) || error }}</span>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">{{ t('Username') || (locale === 'ar' ? 'اسم المستخدم' : 'Username') }}</label>
          <input type="text" v-model="username" class="form-control" required placeholder="..." />
        </div>

        <div class="form-group">
          <label class="form-label">{{ locale === 'ar' ? 'كلمة المرور' : 'Password' }}</label>
          <input type="password" v-model="password" class="form-control" required placeholder="..." />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;" :disabled="loading">
          {{ loading ? (locale === 'ar' ? 'جاري التحميل...' : 'Signing in...') : (locale === 'ar' ? 'تسجيل الدخول' : 'Sign In') }}
        </button>
      </form>

      <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem;">
        <span>{{ locale === 'ar' ? 'ليس لديك حساب؟' : "Don't have an account?" }}</span>
        <router-link to="/register" style="margin-inline-start: 0.5rem; font-weight: 600;">
          {{ locale === 'ar' ? 'إنشاء حساب جديد' : 'Register here' }}
        </router-link>
      </div>
    </div>
  </div>
</template>
