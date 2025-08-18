// stores/taskMonitoring.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useTaskMonitoringStore = defineStore('taskMonitoring', {
  state: () => ({
    tasks: [],      // <-- array task monitoring dari backend
    loading: false,
    error: null,
  }),

  actions: {
    async fetchUncheckUnapproved() {
      this.loading = true
      this.error = null

      try {
        const response = await api.get('service/task-monitoring/')
        const data = response.data

        if (Array.isArray(data)) {
          this.tasks = data
        } else {
          this.tasks = []
          this.error = 'Format data tidak valid'
        }
      } catch (err) {
        this.handleError(err)
        this.tasks = []
      } finally {
        this.loading = false
      }
    },

    async updateTaskStatus(tmId, status) {
      this.loading = true
      this.error = null

      try {
        const response = await api.post('service/task/update-status/', {
          tm_id: tmId,
          status: status
        })

        // update status di tasks local store
        const index = this.tasks.findIndex(t => t.tm_id === tmId)
        if (index !== -1) {
          this.tasks[index].tm_status = status
        }

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
