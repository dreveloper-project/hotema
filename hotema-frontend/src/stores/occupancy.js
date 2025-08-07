// stores/occupancy.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useOccupancyStore = defineStore('occupancy', {
  state: () => ({
    headers: [],   // <-- tanggal-tanggal
    rows: [],      // <-- data kamar dan status hariannya
    loading: false,
    error: null,
  }),

  actions: {
    async fetchOccupancy(startDate, endDate) {
      this.loading = true
      this.error = null

      try {
        const response = await api.get('room/occupancy-table/view/', {
          params: {
            start_date: startDate,
            end_date: endDate,
          },
        })

        const data = response.data?.tableData

        if (data && Array.isArray(data.headers) && Array.isArray(data.rows)) {
          this.headers = data.headers
          this.rows = data.rows
        } else {
          this.headers = []
          this.rows = []
          this.error = 'Format data tidak valid'
        }
      } catch (err) {
        this.handleError(err)
        this.headers = []
        this.rows = []
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
