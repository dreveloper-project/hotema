import { defineStore } from 'pinia'
import api from '@/lib/axios' // axios instance milikmu

export const useRoomRecordStore = defineStore('roomRecord', {
  state: () => ({
    records: [],        // ✅ selalu array
    loading: false,
    error: null,
  }),

  actions: {
    async fetchTodayRecords() {
      this.loading = true
      this.error = null

      try {
        const response = await api.get('room/room-records/today/')
        this.records = Array.isArray(response.data) ? response.data : []
      } catch (err) {
        this.handleError(err)
        this.records = []
      } finally {
        this.loading = false
      }
    },

    async fetchRecordsByDate(date) {
      this.loading = true
      this.error = null

      try {
        const response = await api.get('room/room-records/by-date/', {
          params: { date }
        })

        // ✅ Cek jika response mengandung error dalam objek JSON
        if (
          response.data &&
          typeof response.data === 'object' &&
          !Array.isArray(response.data) &&
          response.data.error
        ) {
          this.error = response.data.error
          this.records = []
        } else {
          this.records = Array.isArray(response.data) ? response.data : []
        }
      } catch (err) {
        this.handleError(err)
        this.records = []
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
