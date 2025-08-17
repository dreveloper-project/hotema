// stores/fetchRecord.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useFetchRecordStore = defineStore('fetchRecord', {
  state: () => ({
    records: [],
    loading: false,
    error: null,
    message: null,
  }),

  actions: {
    // 👉 ambil semua data record + task monitoring
    async fetchRecords() {
      this.loading = true
      this.error = null
      this.message = null
      this.records = []

      try {
        const response = await api.get('service/records-with-task/')
        const data = response.data

        if (!Array.isArray(data) || data.length === 0) {
          this.message = 'Belum ada record'
        } else {
          this.records = data
        }
      } catch (err) {
        this.handleError(err)
      } finally {
        this.loading = false
      }
    },

    // 👉 hapus record berdasarkan record_id
    async deleteRecord(record_id) {
      this.loading = true
      this.error = null
      this.message = null

      try {
        const response = await api.post('service/delete-record/', {
          record_id
        })

        this.message = response.data?.message || 'Record berhasil dihapus'

        // update state records agar langsung hilang di frontend
        this.records = this.records.filter(r => r.record_id !== record_id)

        return response.data
      } catch (err) {
        this.handleError(err)
        throw err // biar bisa ditangkap di komponen
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
