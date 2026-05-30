<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../auth.js'
import { i18nState, t } from '../i18n.js'

const router = useRouter()
const username = ref('')
const fullname = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

const locale = computed(() => i18nState.locale)

const handleRegister = async () => {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await auth.register(username.value, fullname.value, email.value, password.value)
    success.value = locale.value === 'ar' ? 'تم إنشاء الحساب بنجاح! سيتم تحويلك لصفحة الدخول.' : 'Registration successful! Redirecting to login...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = locale.value === 'ar' ? 'فشل التسجيل. يرجى التحقق من المدخلات.' : 'Registration failed. Please check inputs.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="auth-title">{{ locale === 'ar' ? 'إنشاء حساب جديد' : 'Sign Up' }}</h2>
      
      <div v-if="error" class="alert alert-danger">
        <span>⚠️</span>
        <span>{{ t(error) || error }}</span>
      </div>

      <div v-if="success" class="alert alert-success">
        <span>✅</span>
        <span>{{ success }}</span>
      </div>

      <form @submit.prevent="handleRegister" v-if="!success">
        <div class="form-group">
          <label class="form-label">{{ locale === 'ar' ? 'الاسم الكامل' : 'Full Name' }}</label>
          <input type="text" v-model="fullname" class="form-control" required placeholder="Ahmed Ali..." />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('Username') || (locale === 'ar' ? 'اسم المستخدم' : 'Username') }}</label>
          <input type="text" v-model="username" class="form-control" required placeholder="ahmed12..." />
        </div>

        <div class="form-group">
          <label class="form-label">{{ locale === 'ar' ? 'البريد الإلكتروني' : 'Email Address' }}</label>
          <input type="email" v-model="email" class="form-control" required placeholder="ahmed@example.com" />
        </div>

        <div class="form-group">
          <label class="form-label">{{ locale === 'ar' ? 'كلمة المرور' : 'Password' }}</label>
          <input type="password" v-model="password" class="form-control" required placeholder="..." />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;" :disabled="loading">
          {{ loading ? (locale === 'ar' ? 'جاري التسجيل...' : 'Creating account...') : (locale === 'ar' ? 'إنشاء حساب' : 'Register') }}
        </button>
      </form>

      <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem;">
        <span>{{ locale === 'ar' ? 'لديك حساب بالفعل؟' : 'Already have an account?' }}</span>
        <router-link to="/login" style="margin-inline-start: 0.5rem; font-weight: 600;">
          {{ locale === 'ar' ? 'سجل الدخول هنا' : 'Login here' }}
        </router-link>
      </div>
    </div>
  </div>
</template>
