<script setup>
import Sidebar from '../components/Sidebar.vue'
import { ref, watch, onMounted } from 'vue';
import { useTeamManagementStore } from '@/stores/teamManagement';
import { useRouter } from 'vue-router'; 

const router = useRouter();

const selectedRole = ref('staff');
const store = useTeamManagementStore();

// Ambil data pertama kali
onMounted(() => {
  store.fetchUsersByRole(selectedRole.value);
});

// Pantau perubahan role
watch(selectedRole, (newRole) => {
  store.fetchUsersByRole(newRole);
});

// Fungsi detail
function showDetail(id) {
  router.push(`/team-management/user/detail/${id}`); 
}
</script>

<template>
  <Sidebar />
  <main
    class="bg-[#f4f4f6] min-w-[calc(21.145vw-98vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto relative font-poppins"
  >
    <div class="flex justify-end w-[97%] gap-2">
      <button
        class="bg-[#46b389] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
      >
        Set Absensi
        <span class="ml-1"><IconMaterialSymbolsLightAdd class="text-[1rem]" /></span>
      </button>
      <RouterLink to="/team-management/accept-new-team" v-slot="{ navigate }">
        <button
          @click="navigate"
          class="bg-[#FF9B00] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
        >
          Setujui Pegawai Baru
          <span class="ml-1"><IconIcBaselineCheckBox class="text-[1rem]" /></span>
        </button>
      </RouterLink>
    </div>

    <div class="bg-white rounded-lg p-6 w-[97%] text-[0.82rem]">
      <div class="mb-4">
        <select
          v-model="selectedRole"
          class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="staff">Staff</option>
          <option value="supervisor">Supervisor</option>
        </select>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-100 text-gray-700 text-center">
              <th class="text-left px-4 py-2">Nama Lengkap</th>
              <th class="text-left px-4 py-2">Posisi</th>
              <th class="px-4 py-2 ">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(person, index) in store.usersByRole || []"
              :key="index"
              class="border-b hover:bg-gray-50 "
            >
              <!-- Foto + Nama -->
              <td class="px-4 py-2 flex items-center gap-3">
                <template v-if="person.pictures">
                  <img
                    :src="person.pictures"
                    alt="Foto Profil"
                    style="width: 60px; height: 60px;"
                    class="rounded-full object-cover"
                  />
                </template>
                <template v-else>
                  <div
                    class="rounded-full bg-gray-300 flex items-center justify-center text-gray-600"
                    style="width: 60px; height: 60px;"
                  >
                    <span class="text-lg font-bold">
                      {{ person.fullname?.charAt(0).toUpperCase() }}
                    </span>
                  </div>
                </template>
                {{ person.fullname }}
              </td>

              <!-- Role -->
              <td class="px-4 py-2">{{ person.role }}</td>

              <!-- Tombol -->
              <td class="px-4 py-2 text-center">
                <button
                  class="bg-blue-500 text-white px-4 py-1 rounded-sm cursor-pointer hover:bg-blue-600 transition"
                  @click="showDetail(person.user_id)"
                >
                  Detail
                </button>
              </td>
            </tr>

            <!-- Jika tidak ada data -->
            <tr v-if="!store.loading && (store.usersByRole?.length === 0)">
              <td colspan="3" class="text-center py-4 text-gray-500">
                Data tidak ada
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Loading -->
        <div v-if="store.loading" class="text-center py-4 text-gray-500">
          Loading...
        </div>
      </div>
    </div>
  </main>
</template>
