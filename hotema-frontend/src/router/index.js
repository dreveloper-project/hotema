// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import TeamManagementView from '@/views/TeamManagementView.vue'
import OccupancyManagementView from '@/views/OccupancyManagementView.vue'
import SettingsView from '@/views/SettingsView.vue'
import AssignmentView from '@/views/AssignmentView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: DashboardView,
    meta: {
      requiresAuth: true,
      title: 'Dasbor | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/team-management',
    name: 'team_management',
    component: TeamManagementView,
    meta: {
      requiresAuth: true,
      title: 'Manajemen Tim | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/occupancy-management',
    name: 'occupancy_management',
    component: OccupancyManagementView,
    meta: {
      requiresAuth: true,
      title: 'Manajemen Hunian | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: {
      requiresAuth: true,
      title: 'Pengaturan | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/assignment',
    name: 'assignment',
    component: AssignmentView,
    meta: {
      requiresAuth: true,
      title: 'Penugasan | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      title: 'Daftar Akun | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
    meta: {
      title: 'Tentang Aplikasi | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      title: 'Masuk | Sistem Manajemen Tim Housekeeping'
    },
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// ✅ Route Guard dan Title Setter
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token')

  // Set judul halaman (tab browser)
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = 'Sistem Manajemen Tim Housekeeping'
  }

  // Autentikasi
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
