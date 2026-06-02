<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authState, auth } from './auth.js'
import { i18nState, i18n } from './i18n.js'

const router = useRouter()

const user = computed(() => authState.user)
const isAuthenticated = computed(() => authState.isAuthenticated)
const locale = computed(() => i18nState.locale)

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}

const toggleTheme = () => {
  const currentTheme = document.documentElement.getAttribute('data-theme')
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark'
  document.documentElement.setAttribute('data-theme', newTheme)
  localStorage.setItem('theme', newTheme)
}

const handleLangChange = (event) => {
  const newLocale = event.target.value
  i18n.setLocale(newLocale)
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'light'
  document.documentElement.setAttribute('data-theme', savedTheme)
})
</script>

<template>
  <div>
    <nav class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="navbar-brand">
          <span>🎧</span>
           <span>{{ $t('SUPPORT CORE') }}</span>
        </router-link>

        <ul class="navbar-links" v-if="isAuthenticated">
          <li>
            <router-link to="/" class="nav-item" active-class="active">
              {{ $t('Dashboard') }}
            </router-link>
          </li>
          <li>
            <router-link to="/tickets" class="nav-item" active-class="active">
              {{ $t('Tickets') }}
            </router-link>
          </li>
          <li v-if="user && user.is_superuser">
            <router-link to="/users" class="nav-item" active-class="active">
              {{ $t('User Management') }}
            </router-link>
          </li>
        </ul>

        <div class="nav-actions">
          <!-- Theme Toggle -->
          <button class="theme-toggle" @click="toggleTheme" title="Toggle Theme">
            🌓
          </button>

          <!-- Language Selector -->
          <select :value="locale" @change="handleLangChange" class="lang-selector">
            <option value="en">En</option>
            <option value="ar">Ar</option>
          </select>

          <!-- Auth Actions -->
          <div v-if="isAuthenticated" class="nav-actions" style="margin-inline-start: 1rem;">
            <router-link to="/profile" style="color: #ffffff; font-size: 0.9rem; font-weight: 500; margin-right: 0.5rem; margin-left: 0.5rem;">
              {{ $t('My Profile') }}
            </router-link>
            <button @click="handleLogout" class="btn btn-danger btn-sm" style="padding: 0.3rem 0.8rem;">
              {{ $t('Logout') }}
            </button>
          </div>
          <div v-else class="nav-actions">
            <router-link to="/login" class="nav-item" style="color: #fff;">{{ $t('Login') }}</router-link>
            <router-link to="/register" class="btn btn-primary btn-sm" style="border-radius: 20px;">
              {{ $t('Get Started') }}
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="content-wrapper">
      <router-view />
    </main>

    <footer class="footer">
      <div class="container">
        <span>© 2026 {{ $t('Support Ticket System') }}</span>
      </div>
    </footer>
  </div>
</template>
