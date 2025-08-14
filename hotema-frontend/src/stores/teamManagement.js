import { defineStore } from 'pinia';
import api from '@/lib/axios';

export const useTeamManagementStore = defineStore('teamManagement', {
  state: () => ({
    usersWithoutRole: [],
    usersByRole: [],
    userDetail: null,   // 🔹 detail user
    loading: false,
    error: null,
  }),

  actions: {
    async fetchUsersWithoutRole() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get('team-management/users-without-role/');
        this.usersWithoutRole = response.data;
        console.log('Users without role:', response.data);
      } catch (err) {
        console.error('Gagal mengambil daftar user tanpa role:', err);
        this.error = err.response?.data?.detail || 'Gagal memuat data';
      } finally {
        this.loading = false;
      }
    },

    async fetchUsersByRole(role) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`team-management/users-by-role/`, {
          params: { role }
        });
        this.usersByRole = response.data;
        console.log('Users by role:', response.data);
      } catch (err) {
        console.error('Gagal mengambil daftar user by role:', err);
        this.error = err.response?.data?.error || 'Gagal memuat data';
      } finally {
        this.loading = false;
      }
    },

    async fetchUserDetail(userId) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`team-management/users/${userId}/`);
        this.userDetail = response.data;   // 🔹 simpan ke state
        console.log('User detail:', response.data);
        return response.data;              // bisa dipakai langsung
      } catch (err) {
        console.error('Gagal mengambil detail user:', err);
        this.error = err.response?.data?.error || 'Gagal memuat detail user';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async updateUserRole(userId, role) {
      this.loading = true;
      this.error = null;

      try {
        await api.patch('team-management/update-role/', {
          user_id: userId,
          role: role
        });
        // Refresh data setelah update
        await this.fetchUsersWithoutRole();
      } catch (err) {
        console.error('Gagal memperbarui role user:', err);
        this.error = err.response?.data?.error || 'Gagal memperbarui role';
      } finally {
        this.loading = false;
      }
    },

    // 🔹 Tambahan: Delete user
    async deleteUser(userId) {
      this.loading = true;
      this.error = null;
      try {
        await api.delete(`team-management/users/${userId}/delete/`);
        console.log(`User ${userId} berhasil dihapus`);

        // Hapus dari state juga biar konsisten
        this.usersWithoutRole = this.usersWithoutRole.filter(u => u.user_id !== userId);
        this.usersByRole = this.usersByRole.filter(u => u.user_id !== userId);

        // Reset detail kalau yang sedang dibuka dihapus
        if (this.userDetail?.user_id === userId) {
          this.userDetail = null;
        }

        return true;
      } catch (err) {
        console.error('Gagal menghapus user:', err);
        this.error = err.response?.data?.error || 'Gagal menghapus user';
        return false;
      } finally {
        this.loading = false;
      }
    },
     async updateUserRoleById(userId, newRole) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.patch(`team-management/users/${userId}/update-role/`, {
  role: newRole
});

        // update state userDetail kalau yang sedang dibuka sama
        if (this.userDetail?.user_id === userId) {
          this.userDetail = {
            ...this.userDetail,
            role: newRole
          };
        }

        // update juga list agar konsisten
        this.usersWithoutRole = this.usersWithoutRole.map(u =>
          u.user_id === userId ? { ...u, role: newRole } : u
        );
        this.usersByRole = this.usersByRole.map(u =>
          u.user_id === userId ? { ...u, role: newRole } : u
        );

        return response.data;
      } catch (err) {
        console.error('Gagal update role user:', err);
        this.error = err.response?.data?.error || 'Gagal memperbarui role';
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
