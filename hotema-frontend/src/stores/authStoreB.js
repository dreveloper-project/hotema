// src/stores/authStore.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
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
      } catch (err) {
        this.error = err.response?.data || { detail: 'Terjadi kesalahan koneksi ke server.' }
      }
    },

    async login(credentials) {
      try {
        this.error = null
        const res = await api.post('accounts/login/', credentials)

        const token = res.data.access
        this.token = token
        localStorage.setItem('token', token)

        this.user = res.data.user || { username: credentials.username }

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
    },
  },
})
