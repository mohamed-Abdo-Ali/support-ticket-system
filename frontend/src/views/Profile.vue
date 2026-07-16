<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { auth } from '../auth.js'
import { i18nState, t } from '../i18n.js'

const fullname = ref('')
const email = ref('')
const password = ref('')
const showPassword = ref(false)

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
    error.value = t('Failed to load profile.')
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
    message.value = t('Profile updated successfully.')
  } catch (err) {
    error.value = err.response?.data?.detail || t('Failed to update profile.')
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
        <span>{{ $t('My Profile') }}</span>
      </div>
      <div class="card-body">
        <div v-if="fetching" style="text-align: center; padding: 2rem;">
          <p>{{ $t('Loading...') }}</p>
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
              <label class="form-label">{{ $t('Full Name') }}</label>
              <input type="text" v-model="fullname" class="form-control" required placeholder="Ahmed Ali..." />
            </div>

            <div class="form-group">
              <label class="form-label">{{ $t('Email Address') }}</label>
              <input type="email" v-model="email" class="form-control" required placeholder="ahmed@example.com" />
            </div>

            <div class="form-group">
              <label class="form-label">{{ $t('Change Password (Optional)') }}</label>
              <div style="position: relative; display: flex; align-items: center;">
                <input :type="showPassword ? 'text' : 'password'" v-model="password" class="form-control" placeholder="••••••••" style="padding-inline-end: 2.5rem;" />
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
              <p class="text-muted" style="font-size: 0.8rem; margin-top: 0.25rem;">
                {{ $t('Leave blank if you do not want to change it.') }}
              </p>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;" :disabled="loading">
              {{ loading ? $t('Saving...') : $t('Save Changes') }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
