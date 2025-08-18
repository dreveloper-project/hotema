// stores/staffTask.js
import { defineStore } from 'pinia'
import api from '@/lib/axios'

export const useStaffTaskStore = defineStore('staffTask', {
  state: () => ({
    tasks: [],      // list data record + task monitoring
    loading: false,
    error: null,
  }),

  actions: {
    async fetchStaffTasks(userId) {
      this.loading = true
      this.error = null
      this.tasks = []
      try {
        const response = await api.post('service/staff-task/', { user_id: userId })
        this.tasks = response.data || []
      } catch (err) {
        this.handleError(err)
      } finally {
        this.loading = false
      }
    },

    async startRecord(recordId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('service/start/', { record_id: recordId })
        // update record di tasks (optional)
        const updated = this.tasks.map(task =>
          task.record_id === recordId ? { ...task, record_start: response.data.record_start } : task
        )
        this.tasks = updated
      } catch (err) {
        this.handleError(err)
      } finally {
        this.loading = false
      }
    },

    async completeRecord(recordId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('service/complete/', { record_id: recordId })
        // update record di tasks (optional)
        const updated = this.tasks.map(task =>
          task.record_id === recordId ? { ...task, record_complete: response.data.record_complete } : task
        )
        this.tasks = updated
      } catch (err) {
        this.handleError(err)
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
