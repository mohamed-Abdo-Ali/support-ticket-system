import { ref, computed } from 'vue'
import { UserService } from '../services/UserService.js'
import { TicketService } from '../services/TicketService.js'
import { i18nState } from '../i18n.js'

export function useUserViewModel() {
  const users = ref([])
  const targetUser = ref(null)
  const userTickets = ref([])
  
  const loading = ref(false)
  const fetching = ref(false)
  const ticketsLoading = ref(false)
  const error = ref('')

  // Form fields
  const username = ref('')
  const fullname = ref('')
  const email = ref('')
  const password = ref('')
  const showPassword = ref(false)
  const isStaff = ref(false)
  const isSuperuser = ref(false)

  const locale = computed(() => i18nState.locale)

  const fetchUsers = async (translateFn) => {
    loading.value = true
    try {
      const data = await UserService.getUsers()
      users.value = data
      error.value = ''
    } catch (err) {
      error.value = translateFn ? translateFn('Failed to load user list.') : 'Failed to load user list.'
    } finally {
      loading.value = false
    }
  }

  const handleDeleteUser = async (id, name, translateFn) => {
    const confirmMsg = translateFn 
      ? translateFn('Are you sure you want to delete user {username}?').replace('{username}', name) 
      : `Are you sure you want to delete user ${name}?`
    if (!confirm(confirmMsg)) return false
    
    try {
      await UserService.deleteUser(id)
      users.value = users.value.filter(u => u.id !== id)
      return true
    } catch (err) {
      alert(err.response?.data?.detail || (translateFn ? translateFn('Failed to delete user.') : 'Failed to delete user.'))
      return false
    }
  }

  const fetchUserDetails = async (userId, translateFn) => {
    loading.value = true
    try {
      const data = await UserService.getUser(userId)
      targetUser.value = data
      
      // Populate form fields for edit mode
      username.value = data.username
      fullname.value = data.fullname || ''
      email.value = data.email || ''
      isStaff.value = data.is_staff
      isSuperuser.value = data.is_superuser
      
      error.value = ''
    } catch (err) {
      error.value = translateFn ? translateFn('Failed to load user details.') : 'Failed to load user details.'
    } finally {
      loading.value = false
    }
  }

  const fetchUserTickets = async (userId) => {
    ticketsLoading.value = true
    try {
      const data = await TicketService.getTickets({ created_by: userId })
      userTickets.value = data.results
    } catch (err) {
      console.error('Failed to load user tickets', err)
    } finally {
      ticketsLoading.value = false
    }
  }

  const handleSubmit = async (userId, translateFn, callback) => {
    error.value = ''
    if (!username.value) {
      error.value = translateFn ? translateFn('Username is required.') : 'Username is required.'
      return
    }
    const isEditMode = !!userId
    if (!isEditMode && !password.value) {
      error.value = translateFn ? translateFn('Password is required.') : 'Password is required.'
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
      if (isEditMode) {
        await UserService.updateUser(userId, payload)
      } else {
        await UserService.createUser(payload)
      }
      if (callback) callback()
    } catch (err) {
      error.value = err.response?.data?.detail || err.response?.data?.username?.[0] || (translateFn ? translateFn('Failed to save changes.') : 'Failed to save changes.')
    } finally {
      loading.value = false
    }
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleDateString(locale.value === 'ar' ? 'ar-EG' : 'en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  return {
    users,
    targetUser,
    userTickets,
    loading,
    fetching,
    ticketsLoading,
    error,
    username,
    fullname,
    email,
    password,
    showPassword,
    isStaff,
    isSuperuser,
    locale,
    fetchUsers,
    handleDeleteUser,
    fetchUserDetails,
    fetchUserTickets,
    handleSubmit,
    formatDate
  }
}
