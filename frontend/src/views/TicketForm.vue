<script setup>
import { useRouter } from 'vue-router'
import { t } from '../i18n.js'
import { useTicketFormViewModel } from '../viewmodels/useTicketFormViewModel.js'

const router = useRouter()

const {
  subject,
  description,
  priority,
  category,
  file,
  error,
  loading,
  handleFileChange,
  handleSubmit
} = useTicketFormViewModel()

const submitForm = () => {
  handleSubmit(t, () => {
    router.push('/tickets')
  })
}
</script>

<template>
  <div style="max-width: 800px; margin: 0 auto;">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/tickets" style="font-weight: 500;">
        {{ $t('Tickets') }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">{{ $t('New Ticket') }}</span>
    </div>

    <div class="card">
      <div class="card-header">
        <span>{{ $t('New Support Request') }}</span>
      </div>
      <div class="card-body">
        <div v-if="error" class="alert alert-danger">
          <span>⚠️</span>
          <span>{{ t(error) || error }}</span>
        </div>

        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label class="form-label">{{ $t('Subject') }}</label>
            <input type="text" v-model="subject" class="form-control" required :placeholder="$t('Enter subject detail...')" />
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('Detailed Description') }}</label>
            <textarea v-model="description" class="form-control" rows="6" required :placeholder="$t('Describe your problem in detail...')"></textarea>
          </div>

          <div class="filters-grid" style="margin-bottom: 1.25rem;">
            <div class="form-group" style="margin-bottom: 0;">
              <label class="form-label">{{ $t('Priority') }}</label>
              <select v-model="priority" class="form-select">
                <option value="Low">{{ $t('Low') }}</option>
                <option value="Medium">{{ $t('Medium') }}</option>
                <option value="High">{{ $t('High') }}</option>
              </select>
            </div>

            <div class="form-group" style="margin-bottom: 0;">
              <label class="form-label">{{ $t('Category') }}</label>
              <select v-model="category" class="form-select">
                <option value="General">{{ $t('General') }}</option>
                <option value="Technical">{{ $t('Technical') }}</option>
                <option value="Billing">{{ $t('Billing') }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">{{ $t('Attachment (Image)') }}</label>
            <input type="file" @change="handleFileChange" accept="image/*" class="form-control" />
          </div>

          <div style="display: flex; gap: 1rem; margin-top: 2rem;">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? $t('Submitting...') : $t('Submit Ticket') }}
            </button>
            <button type="button" @click="$router.push('/tickets')" class="btn btn-outline">
              {{ $t('Cancel') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
