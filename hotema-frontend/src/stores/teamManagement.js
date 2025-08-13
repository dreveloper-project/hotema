import { defineStore } from 'pinia';
import api from '@/lib/axios';

export const useTeamManagementStore = defineStore('teamManagement', {
  state: () => ({
    usersWithoutRole: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchUsersWithoutRole() {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.get('team-management/users-without-role/');
        this.usersWithoutRole = response.data; // langsung simpan array user
        console.log(response.data)
      } catch (err) {
        console.error('Gagal mengambil daftar user tanpa role:', err);
        this.error = err.response?.data?.detail || 'Gagal memuat data';
      } finally {
        this.loading = false;
      }
    },
  },
});
