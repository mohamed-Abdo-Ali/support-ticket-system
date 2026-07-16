import { ref, computed } from 'vue'
import { authState } from '../auth.js'
import { AuthService } from '../services/AuthService.js'
import axios from 'axios'

export function useAuthViewModel() {
  const loading = ref(false)
  const error = ref('')

  const isAuthenticated = computed(() => authState.isAuthenticated)
  const user = computed(() => authState.user)

  const login = async (username, password) => {
    loading.value = true
    error.value = ''
    try {
      const data = await AuthService.login(username, password)
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
      
      const userProfile = await AuthService.fetchProfile()
      localStorage.setItem('user', JSON.stringify(userProfile))
      
      authState.isAuthenticated = true
      authState.user = userProfile
      return userProfile
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const register = async (username, fullname, email, password) => {
    loading.value = true
    error.value = ''
    try {
      await AuthService.register(username, fullname, email, password)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    authState.isAuthenticated = false
    authState.user = null
    delete axios.defaults.headers.common['Authorization']
  }

  const fetchProfile = async () => {
    loading.value = true
    try {
      const data = await AuthService.fetchProfile()
      localStorage.setItem('user', JSON.stringify(data))
      authState.user = data
      return data
    } catch (err) {
      logout()
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateProfile = async (profileData) => {
    loading.value = true
    error.value = ''
    try {
      const data = await AuthService.updateProfile(profileData)
      localStorage.setItem('user', JSON.stringify(data))
      authState.user = data
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Update profile failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    isAuthenticated,
    user,
    loading,
    error,
    login,
    register,
    logout,
    fetchProfile,
    updateProfile
  }
}
