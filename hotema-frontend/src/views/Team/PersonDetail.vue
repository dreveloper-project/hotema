<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import { useTeamManagementStore } from '@/stores/teamManagement';

const store = useTeamManagementStore();
const route = useRoute();
const router = useRouter();

const selectedRole = ref('');
const userId = Number(route.params.id); // pastikan number

onMounted(async () => {
  try {
    await store.fetchUserDetail(userId);
    selectedRole.value = store.userDetail?.role || '';
  } catch (err) {
    console.error(err);
  }
});

const saveRole = async () => {
  if (!selectedRole.value) return;
  try {
    await store.updateUserRoleById(userId, selectedRole.value);

    alert('Role berhasil diperbarui!');
  } catch (err) {
    console.error('Gagal update role:', err);
  }
};

const deleteUser = async () => {
  if (!confirm('Yakin ingin menghapus user ini?')) return;
  try {
    const success = await store.deleteUser(userId);
    if (success) {
      alert('User berhasil dihapus!');
      router.push('/team-management');
    }
  } catch (err) {
    console.error('Gagal hapus user:', err);
  }
};
</script>

<template>
  <Sidebar />
  <main
    class="bg-[#f4f4f6] pl-[2rem] ml-[20.145vw] py-10 min-h-screen h-auto relative font-poppins"
  >
    <div class="flex">
      <RouterLink to="/team-management" v-slot="{ navigate }">
        <button
          @click="navigate"
          class="bg-[#6b61ff] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
        >
          Kembali
          <span class="ml-1"><IconIcBaselineKeyboardBackspace class="text-[1rem]" /></span>
        </button>
      </RouterLink>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex justify-center items-center h-full">
      <span class="text-gray-500">Loading...</span>
    </div>

    <!-- User Detail Card -->
    <div
      v-else-if="store.userDetail"
      class="max-w-3xl w-full bg-white shadow-xl rounded-2xl p-8 space-y-6 mx-auto"
    >
      <div class="flex items-center space-x-6">
        <img
          v-if="store.userDetail.pictures"
          :src="store.userDetail.pictures"
          alt="User Photo"
          class="w-24 h-24 rounded-full object-cover border"
        />
        <div>
          <h2 class="text-2xl font-semibold text-gray-800">
            {{ store.userDetail.fullname }}
          </h2>
          <p class="text-base text-gray-500">@{{ store.userDetail.username }}</p>
        </div>
      </div>

      <div class="space-y-4 text-gray-700">
        <p><span class="font-medium">Email:</span> {{ store.userDetail.email }}</p>

        <!-- Role -->
        <div class="flex items-center space-x-3">
          <label class="font-medium">Role:</label>
          <select
            v-model="selectedRole"
            class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
          >
            <option disabled value="">-- Pilih Role --</option>
            <option value="staff">Staff</option>
            <option value="supervisor">Supervisor</option>
          </select>
          <button
            @click="saveRole"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm cursor-pointer hover:bg-blue-700"
          >
            Simpan
          </button>
        </div>

       
      </div>

      <!-- Tombol hapus -->
      <div class="pt-6 border-t flex justify-end">
        <button
          @click="deleteUser"
          class="bg-red-600 text-white px-5 py-2 rounded-lg text-sm cursor-pointer hover:bg-red-700"
        >
          Hapus User
        </button>
      </div>
    </div>

    <div v-else class="text-center text-gray-500">Tidak ada data user.</div>
  </main>
</template>
