// stores/attendance.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useSetPresence = defineStore('setPresence', {
  state: () => ({
    infoByDate: {},   // { 1: "Shift Pagi", 2: "Libur", ... }
    loading: false,
    error: null,
  }),

  actions: {
    async fetchAttendance(userId, month, year) {
      this.loading = true
      this.error = null

      try {
        const res = await api.get(`presence/${userId}/`, {
          params: { month, year }
        })

        // Pastikan respons berupa object (misalnya { 1: "Shift Pagi", 2: "Libur" })
        if (res.data && typeof res.data === 'object') {
          this.infoByDate = res.data
        } else {
          this.infoByDate = {}
          this.error = 'Format data tidak valid'
        }
      } catch (err) {
        this.handleError(err)
        this.infoByDate = {}
      } finally {
        this.loading = false
      }
    },

    async setAttendance(userId, day, month, year, shiftType) {
      this.loading = true
      this.error = null

      try {
        const payload = { user_id: userId, day, month, year, shift: shiftType }
        const res = await api.post(`presence/set/`, payload)

        // Update state lokal supaya langsung kelihatan
        this.infoByDate[day] = shiftType
        return res.data
      } catch (err) {
        this.handleError(err)
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteAttendance(userId, day, month, year) {
      this.loading = true
      this.error = null

      try {
        const res = await api.post(`presence/delete/`, {
          user_id: userId,
          day,
          month,
          year
        })

        // Update state lokal → biar jadi "Libur"
        this.infoByDate[day] = "Libur"
        return res.data
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
