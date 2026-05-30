<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { i18nState, t } from '../i18n.js'

const route = useRoute()
const router = useRouter()
const userId = route.params.id

const isEditMode = computed(() => !!userId)

const username = ref('')
const fullname = ref('')
const email = ref('')
const password = ref('')
const isStaff = ref(false)
const isSuperuser = ref(false)

const error = ref('')
const loading = ref(false)
const fetching = ref(false)

const locale = computed(() => i18nState.locale)

const fetchUserDetails = async () => {
  fetching.value = true
  try {
    const response = await axios.get(`/api/users/${userId}/`)
    username.value = response.data.username
    fullname.value = response.data.fullname || ''
    email.value = response.data.email || ''
    isStaff.value = response.data.is_staff
    isSuperuser.value = response.data.is_superuser
  } catch (err) {
    error.value = locale.value === 'ar' ? 'فشل تحميل بيانات المستخدم.' : 'Failed to load user details.'
  } finally {
    fetching.value = false
  }
}

const handleSubmit = async () => {
  error.value = ''
  if (!username.value) {
    error.value = locale.value === 'ar' ? 'اسم المستخدم مطلوب.' : 'Username is required.'
    return
  }
  if (!isEditMode.value && !password.value) {
    error.value = locale.value === 'ar' ? 'كلمة المرور مطلوبة.' : 'Password is required.'
    return
  }

  loading.value = true
  const payload = {
    username: username.value,
    fullname: fullname.value,
    email: email.value,
    is_staff: isStaff.value,
    is_superuser: isSuperuser.value
  }

  if (password.value) {
    payload.password = password.value
  }

  try {
    if (isEditMode.value) {
      await axios.put(`/api/users/${userId}/`, payload)
    } else {
      await axios.post('/api/users/', payload)
    }
    router.push('/users')
  } catch (err) {
    error.value = err.response?.data?.detail || err.response?.data?.username?.[0] || (locale.value === 'ar' ? 'فشل حفظ التعديلات.' : 'Failed to save changes.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (isEditMode.value) {
    fetchUserDetails()
  }
})
</script>

<template>
  <div style="max-width: 600px; margin: 0 auto;">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/users" style="font-weight: 500;">
        {{ locale === 'ar' ? 'المستخدمين' : 'Users' }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">{{ isEditMode ? (locale === 'ar' ? 'تعديل مستخدم' : 'Edit User') : (locale === 'ar' ? 'إضافة مستخدم' : 'New User') }}</span>
    </div>

    <div class="card">
      <div class="card-header">
        <span>{{ isEditMode ? (locale === 'ar' ? 'تعديل بيانات المستخدم' : 'Edit User Profile') : (locale === 'ar' ? 'إضافة مستخدم جديد' : 'Create New Account') }}</span>
      </div>
      <div class="card-body">
        <div v-if="fetching" style="text-align: center; padding: 2rem;">
          <p>{{ locale === 'ar' ? 'جاري تحميل البيانات...' : 'Loading...' }}</p>
        </div>

        <form v-else @submit.prevent="handleSubmit">
          <div v-if="error" class="alert alert-danger">
            <span>⚠️</span>
            <span>{{ t(error) || error }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">{{ locale === 'ar' ? 'اسم المستخدم' : 'Username' }}</label>
            <input type="text" v-model="username" class="form-control" required placeholder="username..." />
          </div>

          <div class="form-group">
            <label class="form-label">{{ locale === 'ar' ? 'الاسم الكامل' : 'Full Name' }}</label>
            <input type="text" v-model="fullname" class="form-control" placeholder="Full name..." />
          </div>

          <div class="form-group">
            <label class="form-label">{{ locale === 'ar' ? 'البريد الإلكتروني' : 'Email Address' }}</label>
            <input type="email" v-model="email" class="form-control" placeholder="user@example.com" />
          </div>

          <div class="form-group">
            <label class="form-label">{{ isEditMode ? (locale === 'ar' ? 'تعديل كلمة المرور (اختياري)' : 'Change Password (Optional)') : (locale === 'ar' ? 'كلمة المرور' : 'Password') }}</label>
            <input type="password" v-model="password" class="form-control" :required="!isEditMode" placeholder="••••••••" />
          </div>

          <div class="form-check">
            <input type="checkbox" id="isStaff" v-model="isStaff" />
            <label for="isStaff" class="form-label" style="display: inline; margin-bottom: 0; cursor: pointer;">
              {{ locale === 'ar' ? 'موظف دعم فني (Staff)' : 'Support Staff (is_staff)' }}
            </label>
          </div>

          <div class="form-check" style="margin-bottom: 2rem;">
            <input type="checkbox" id="isSuperuser" v-model="isSuperuser" />
            <label for="isSuperuser" class="form-label" style="display: inline; margin-bottom: 0; cursor: pointer;">
              {{ locale === 'ar' ? 'مدير نظام (Superuser)' : 'System Manager (is_superuser)' }}
            </label>
          </div>

          <div style="display: flex; gap: 1rem;">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? (locale === 'ar' ? 'جاري الحفظ...' : 'Saving...') : (locale === 'ar' ? 'حفظ التغييرات' : 'Save Changes') }}
            </button>
            <button type="button" @click="$router.push('/users')" class="btn btn-outline">
              {{ locale === 'ar' ? 'إلغاء' : 'Cancel' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
