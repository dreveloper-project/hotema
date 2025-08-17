// src/stores/authStoreB.js (atau sesuai pathmu)
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    error: null,
    token: localStorage.getItem('token') || null,
  }),

  actions: {
    async register(formData) {
      try {
        this.error = null
        const res = await api.post('accounts/register/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        this.user = res.data
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (err) {
        this.error = err.response?.data || { detail: 'Terjadi kesalahan koneksi ke server.' }
      }
    },

    async login(credentials) {
      try {
        this.error = null
        const res = await api.post('accounts/login/', credentials)

        const accessToken = res.data.access
        const refreshToken = res.data.refresh

        this.token = accessToken
        localStorage.setItem('token', accessToken)
        localStorage.setItem('refresh_token', refreshToken)

        // Simpan user ke localStorage agar tidak hilang saat refresh
        this.user = res.data.user || { username: credentials.username }
        localStorage.setItem('user', JSON.stringify(this.user))

        return true
      } catch (err) {
        this.error = err.response?.data || { detail: 'Terjadi kesalahan saat login.' }
        return false
      }
    },

   

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },
  },
})
