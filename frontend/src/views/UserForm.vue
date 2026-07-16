<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { t } from '../i18n.js'
import { useUserViewModel } from '../viewmodels/useUserViewModel.js'

const route = useRoute()
const router = useRouter()
const userId = route.params.id

const isEditMode = computed(() => !!userId)

const {
  username,
  fullname,
  email,
  password,
  showPassword,
  isStaff,
  isSuperuser,
  error,
  loading,
  fetching,
  fetchUserDetails,
  handleSubmit
} = useUserViewModel()

const saveUser = () => {
  handleSubmit(userId, t, () => {
    router.push('/users')
  })
}

onMounted(() => {
  if (isEditMode.value) {
    fetchUserDetails(userId, t)
  }
})
</script>

<template>
  <div style="max-width: 600px; margin: 0 auto;">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/users" style="font-weight: 500;">
        {{ $t('Users') }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">
        {{ isEditMode ? $t('Edit User') : $t('New User') }}
      </span>
    </div>

    <div class="card">
      <div class="card-header">
        <span>
          {{ isEditMode ? $t('Edit User Profile') : $t('Create New Account') }}
        </span>
      </div>
      <div class="card-body">
        <div v-if="fetching" style="text-align: center; padding: 2rem;">
          <p>{{ $t('Loading...') }}</p>
        </div>

        <form v-else @submit.prevent="saveUser">
          <div v-if="error" class="alert alert-danger">
            <span>⚠️</span>
            <span>{{ t(error) || error }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('Username') }}</label>
            <input type="text" v-model="username" class="form-control" required placeholder="username..." />
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('Full Name') }}</label>
            <input type="text" v-model="fullname" class="form-control" placeholder="Full name..." />
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('Email Address') }}</label>
            <input type="email" v-model="email" class="form-control" placeholder="user@example.com" />
          </div>

          <div class="form-group">
            <label class="form-label">
              {{ isEditMode ? $t('Change Password (Optional)') : $t('Password') }}
            </label>
            <div style="position: relative; display: flex; align-items: center;">
              <input :type="showPassword ? 'text' : 'password'" v-model="password" class="form-control" :required="!isEditMode" placeholder="••••••••" style="padding-inline-end: 2.5rem;" />
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

          <div class="form-check">
            <input type="checkbox" id="isStaff" v-model="isStaff" />
            <label for="isStaff" class="form-label" style="display: inline; margin-bottom: 0; cursor: pointer;">
              {{ $t('Support Staff (is_staff)') }}
            </label>
          </div>

          <div class="form-check" style="margin-bottom: 2rem;">
            <input type="checkbox" id="isSuperuser" v-model="isSuperuser" />
            <label for="isSuperuser" class="form-label" style="display: inline; margin-bottom: 0; cursor: pointer;">
              {{ $t('System Manager (is_superuser)') }}
            </label>
          </div>

          <div style="display: flex; gap: 1rem;">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? $t('Saving...') : $t('Save Changes') }}
            </button>
            <button type="button" @click="$router.push('/users')" class="btn btn-outline">
              {{ $t('Cancel') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>