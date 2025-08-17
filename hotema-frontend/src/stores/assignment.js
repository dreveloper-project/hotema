// stores/assignment.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useAssignmentStore = defineStore('assignment', {
  state: () => ({
    staff: [],
    rooms: [],
    selectedDate: null,
    loading: false,
    error: null,
    message: null,
  }),

  actions: {
    async fetchStaffByDate(date) {
      this.loading = true
      this.error = null
      this.message = null
      this.staff = []
      this.rooms = []
      this.selectedDate = date

      try {
        // convert date ke YYYY-MM-DD (tanpa jam)
        const formattedDate = new Date(date).toISOString().split("T")[0]

        const response = await api.post('service/staff-by-date/', {
          date: formattedDate
        })

        const data = response.data

        if (data.message) {
          this.message = data.message
          this.staff = []
          this.rooms = []
        } else {
          this.staff = Array.isArray(data.staff) ? data.staff : []
          this.rooms = Array.isArray(data.rooms) ? data.rooms : []
        }
      } catch (err) {
        this.handleError(err)
        this.staff = []
        this.rooms = []
      } finally {
        this.loading = false
      }
    },

    // 👉 function baru untuk membuat record
    async createRecord({ date, user_id, room_id }) {
      this.loading = true
      this.error = null
      this.message = null

      try {
        const formattedDate = new Date(date).toISOString().split("T")[0]

        const response = await api.post('service/create-record/', {
          date: formattedDate,
          user_id,
          room_id
        })

        this.message = response.data?.message || 'Record berhasil dibuat'
        return response.data  // supaya component bisa pakai data record_id dll
      } catch (err) {
        this.handleError(err)
        throw err // lempar error biar bisa ditangkap di component
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
