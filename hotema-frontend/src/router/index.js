// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import TeamManagementView from '@/views/TeamManagementView.vue'
import OccupancyManagementView from '@/views/OccupancyManagementView.vue'
import SettingsView from '@/views/SettingsView.vue'
import AssignmentView from '@/views/AssignmentView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import AddRoomView from '@/views/Assignment/AddRoomView.vue'
import AcceptNewTeamView from '@/views/Team/AcceptNewTeamView.vue'
import PersonDetail from '@/views/Team/PersonDetail.vue'
import StaffDashboardView from '@/views/Mobile/StaffDashboardView.vue'
import SpvDashboardView from '@/views/Mobile/SpvDashboardView.vue'
import StaffTaskView from '@/views/Mobile/StaffTaskView.vue'
import SpvTaskView from '@/views/Mobile/SpvTaskView.vue'
import SetPresenceView from '@/views/Team/SetPresenceView.vue'
import TaskLogView from '@/views/Assignment/TaskLogView.vue'
import CreateAssignment from '@/views/Assignment/CreateAssignment.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: DashboardView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Dasbor | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/team-management',
    name: 'team_management',
    component: TeamManagementView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Manajemen Tim | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/team-management/accept-new-team',
    name: 'accept-new-team',
    component: AcceptNewTeamView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Setujui Pegawai Baru | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/team-management/user/detail/:id',
    name: 'user-detail',
    component: PersonDetail,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Detail Pegawai | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/team-management/set-presence/:id',
    name: 'set-presence',
    component: SetPresenceView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Buat & Ubah Jadwal | Sistem Manajemen Tim Housekeeping'
      
    },
  },
  {
    path: '/occupancy-management',
    name: 'occupancy_management',
    component: OccupancyManagementView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Manajemen Hunian | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Pengaturan | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/assignment',
    name: 'assignment',
    component: AssignmentView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Penugasan | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/create-assignment',
    name: 'create-assignment',
    component: CreateAssignment,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Tugaskan Seorang Staff | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/task-log',
    name: 'task-log',
    component: TaskLogView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Log Tugas | Sistem Manajemen Tim Housekeeping'
    },
  },
  {
    path: '/assignment/add/room',
    name: 'assignment-add-room',
    component: AddRoomView,
    meta: {
      requiresAuth: true,
      roles: ['admin'],
      title: 'Penugasan | Tambah Data Kamar Baru'
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
  },

  // Mobile user
  {
    path: '/staff/dashboard',
    name: 'staff-dashboard',
    component: StaffDashboardView,
    meta: {
      title: 'Dashboard Staff | Sistem Manajemen Tim Housekeeping',
      requiresAuth: true,
      roles: ['staff'],
    },
  },
   {
    path: '/staff/task',
    name: 'staff-task',
    component: StaffTaskView,
    meta: {
      title: 'Daftar Pekerjaan Hari Ini | Sistem Manajemen Tim Housekeeping',
      requiresAuth: true,
      roles: ['staff'],
    },
  },
  {
    path: '/spv/dashboard',
    name: 'spv-dashboard',
    component: SpvDashboardView,
    meta: {
      title: 'Dashboard Supervisor | Sistem Manajemen Tim Housekeeping',
      requiresAuth: true,
      roles: ['supervisor'],
    },
  },
  {
    path: '/spv/task-monitoring',
    name: 'spv-monitoring',
    component: SpvTaskView,
    meta: {
      title: 'Daftar Pekerjaan Hari Ini | Sistem Manajemen Tim Housekeeping',
      requiresAuth: true,
      roles: ['supervisor'],
    },
  },

  

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
