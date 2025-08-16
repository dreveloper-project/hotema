// stores/setPresence.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useSetPresenceStore = defineStore('setPresence', {
  state: () => ({
    dates: [],       // <-- array tanggal dari backend
    infoByDate: [],  // <-- isi shift atau "Libur"
    loading: false,
    error: null,
  }),

  actions: {
    async fetchPresence(userId, month, year) {
      this.loading = true
      this.error = null

      try {
        const response = await api.post('presence/user-schedule/', {
          user_id: userId,
          month: month,
          year: year
        })

        const data = response.data

        if (data && Array.isArray(data.date) && Array.isArray(data.infobydate)) {
          this.dates = data.date
          this.infoByDate = data.infobydate
        } else {
          this.dates = []
          this.infoByDate = []
          this.error = 'Format data tidak valid'
        }
      } catch (err) {
        this.handleError(err)
        this.dates = []
        this.infoByDate = []
      } finally {
        this.loading = false
      }
    },
    async setShift(userId, date, shiftId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('presence/set-shift/', {
          user_id: userId,
          date: date,
          shift_id: shiftId
        })
        // Setelah update, refresh data bulan yang sama
        const d = new Date(date)
        await this.fetchPresence(userId, d.getMonth() + 1, d.getFullYear())
        return response.data
      } catch (err) {
        this.handleError(err)
        throw err
      } finally {
        this.loading = false
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
