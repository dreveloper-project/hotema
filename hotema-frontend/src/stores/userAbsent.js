// stores/userAbsent.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useUserAbsentStore = defineStore('userAbsent', {
  state: () => ({
    status: null,   
    loading: false,
    error: null,
  }),

  actions: {
    async fetchAbsentStatus(userId) {
  this.loading = true
  this.error = null
  this.status = null
  try {
    const response = await api.post('absent/status/', { user_id: userId })
    this.status = response.data?.status || null
  } catch (err) {
    this.handleError(err)
  } finally {
    this.loading = false
  }
},
async absentIn(userId) {
  try {
    await api.post('absent/create/', { user_id: userId })
    console.log(userId)
    this.status = 'Absen Pulang'   // set manual
  } catch (err) {
    this.handleError(err)
    console.log(err)
  }
},

async absentOut(userId) {
  try {
    await api.post('absent/out/', { user_id: userId })
    this.status = 'Pekerjaan Sudah Selesai'   // set manual
  } catch (err) {
    this.handleError(err)
  }
},

    handleError(err) {
      if (err.response) {
        this.error = err.response.data?.error || 'Terjadi kesalahan dari server.'
      } else if (err.request) {
        this.error = 'Tidak ada respon dari server.'
      } else {
        this.error = 'Kesalahan tidak terduga: ' + err.message
      }
    }
  }
})
