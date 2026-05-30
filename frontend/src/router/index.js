import { createRouter, createWebHistory } from 'vue-router'
import { authState } from '../auth.js'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import TicketList from '../views/TicketList.vue'
import TicketDetail from '../views/TicketDetail.vue'
import TicketForm from '../views/TicketForm.vue'
import Profile from '../views/Profile.vue'
import UserList from '../views/UserList.vue'
import UserForm from '../views/UserForm.vue'
import UserDetail from '../views/UserDetail.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
  { path: '/register', name: 'Register', component: Register, meta: { guest: true } },
  { path: '/', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/tickets', name: 'TicketList', component: TicketList, meta: { requiresAuth: true } },
  { path: '/tickets/new', name: 'TicketForm', component: TicketForm, meta: { requiresAuth: true, clientOnly: true } },
  { path: '/tickets/:id', name: 'TicketDetail', component: TicketDetail, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/users', name: 'UserList', component: UserList, meta: { requiresAuth: true, superuserOnly: true } },
  { path: '/users/new', name: 'UserCreate', component: UserForm, meta: { requiresAuth: true, superuserOnly: true } },
  { path: '/users/:id/edit', name: 'UserEdit', component: UserForm, meta: { requiresAuth: true, superuserOnly: true } },
  { path: '/users/:id', name: 'UserDetail', component: UserDetail, meta: { requiresAuth: true, superuserOnly: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = authState.isAuthenticated
  const user = authState.user

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && isAuthenticated) {
    next('/')
  } else if (to.meta.superuserOnly && (!user || !user.is_superuser)) {
    next('/')
  } else if (to.meta.clientOnly && user && user.is_staff) {
    next('/')
  } else {
    next()
  }
})

export default router
