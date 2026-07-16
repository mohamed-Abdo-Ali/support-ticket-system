<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../auth.js'
import { i18nState, t } from '../i18n.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
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
      error.value = t('Login failed. Please check credentials.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="auth-title">{{ $t('Sign In') }}</h2>
      
      <div v-if="error" class="alert alert-danger">
        <span>⚠️</span>
        <span>{{ t(error) || error }}</span>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">{{ $t('Username') }}</label>
          <input type="text" v-model="username" class="form-control" required placeholder="..." />
        </div>

        <div class="form-group">
          <label class="form-label">{{ $t('Password') }}</label>
          <div style="position: relative; display: flex; align-items: center;">
            <input :type="showPassword ? 'text' : 'password'" v-model="password" class="form-control" required placeholder="..." style="padding-inline-end: 2.5rem;" />
            <button type="button" @click="showPassword = !showPassword" style="position: absolute; inset-inline-end: 10px; background: none; border: none; cursor: pointer; color: inherit; opacity: 0.7; display: flex; padding: 0; outline: none;">
              <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
                <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                <path d="m10.79 12.912-1.614-1.615a3.5 3.5 0 0 1-4.474-4.474l-2.06-2.06C.938 6.278 0 8 0 8s3 5.5 8 5.5a7 7 0 0 0 2.79-.588M5.21 3.088A7 7 0 0 1 8 2.5c5 0 8 5.5 8 5.5s-.939 1.721-2.641 3.238l-2.062-2.062a3.5 3.5 0 0 0-4.474-4.474z"/>
                <path d="M5.525 7.646a2.5 2.5 0 0 0 2.829 2.829zm4.95.708-2.829-2.83a2.5 2.5 0 0 1 2.829 2.829zm3.171 6-12-12 .708-.708 12 12z"/>
              </svg>
            </button>
          </div>
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;" :disabled="loading">
          {{ loading ? $t('Signing in...') : $t('Sign In') }}
        </button>
      </form>

      <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem;">
        <span>{{ locale === 'ar' ? 'ليس لديك حساب؟' : "Don't have an account?" }}</span>
        <router-link to="/register" style="margin-inline-start: 0.5rem; font-weight: 600;">
          {{ $t('Register here') }}
        </router-link>
      </div>
    </div>
  </div>
</template>
