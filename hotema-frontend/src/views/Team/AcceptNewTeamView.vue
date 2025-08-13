<script setup>
import Sidebar from '@/components/Sidebar.vue'
import { computed, onMounted, ref } from 'vue'
import { useTeamManagementStore } from '@/stores/teamManagement'
import ProgressSpinner from 'primevue/progressspinner'
import PopUp from '@/components/PopUp.vue'

const teamStore = useTeamManagementStore()

// State untuk popup
const showPopup = ref(false)
const popupMessage = ref('')
const popupType = ref('success') // success | error

onMounted(() => {
  teamStore.fetchUsersWithoutRole()
})

const usersData = computed(() =>
  Array.isArray(teamStore.usersWithoutRole) ? teamStore.usersWithoutRole : []
)

async function approveUser(person) {
  if (!person.role) {
    popupMessage.value = 'Silakan pilih posisi sebelum menyetujui.'
    popupType.value = 'error'
    showPopup.value = true
    return
  }

  try {
    await teamStore.updateUserRole(person.user_id, person.role)
    popupMessage.value = `Berhasil menyetujui ${person.fullname} sebagai ${person.role}`
    popupType.value = 'success'
    showPopup.value = true
  } catch (error) {
    popupMessage.value = 'Terjadi kesalahan saat memperbarui role pengguna.'
    popupType.value = 'error'
    showPopup.value = true
  }
}

function updateRole(person, newRole) {
  person.role = newRole
}
</script>

<template>
  <Sidebar />
  <main
    class="bg-[#f4f4f6] min-w-[calc(21.145vw-98vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto relative font-poppins"
  > 
  <div class="flex">
    <RouterLink to="/team-management" v-slot="{ navigate, isActive }">
    <button
      @click="navigate"
      class="bg-[#6b61ff] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
    >
      Kembali
      <span class="ml-1"><IconIcBaselineKeyboardBackspace class="text-[1rem]" />
</span>
    </button>
    </RouterLink>
  </div>
    <div class="bg-white rounded-lg p-6 w-[97%] text-[0.82rem]">
      <div class="overflow-x-auto">
        
        <!-- Table -->
        <table
          class="w-full border-collapse"
          v-if="!teamStore.loading && !teamStore.error"
        >
          <thead>
            <tr class="bg-gray-100 text-gray-700">
              <th class="px-4 py-2 text-center">Foto Profil</th>
              <th class="text-left px-4 py-2">Nama Lengkap</th>
              <th class="text-left px-4 py-2">Posisi</th>
              <th class="px-4 py-2 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="person in usersData"
              :key="person.user_id"
              class="border-b hover:bg-gray-50"
            >
              <!-- Foto profil -->
              <td class="px-4 py-2 text-center">
                <img
                  :src="person.pictures || 'https://via.placeholder.com/100'"
                  alt="Foto Profil"
                  class="w-16 h-16 rounded-full object-cover mx-auto"
                />
              </td>

              <!-- Nama -->
              <td class="px-4 py-2">{{ person.fullname }}</td>

              <!-- Dropdown Role -->
              <td class="px-4 py-2">
                <select
                  v-model="person.role"
                  @change="updateRole(person, $event.target.value)"
                  class="border border-gray-300 rounded-lg px-2 py-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                >
                  <option value="">Pilih Posisi</option>
                  <option value="staff">Staff</option>
                  <option value="supervisor">Supervisor</option>
                </select>
              </td>

              <!-- Tombol Setujui -->
              <td class="px-4 py-2 text-center">
                <button
                  class="bg-green-500 text-white px-4 py-1 cursor-pointer rounded-lg hover:bg-green-600 transition"
                  @click="approveUser(person)"
                >
                  Setujui
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Loading -->
        <div v-if="teamStore.loading" class="flex justify-center py-10">
          <ProgressSpinner
            style="width: 50px; height: 50px"
            strokeWidth="4"
            fill="var(--surface-ground)"
            animationDuration=".5s"
          />
        </div>

        <!-- Error -->
        <div v-if="teamStore.error" class="p-4 text-red-500">
          {{ teamStore.error }}
        </div>
      </div>
    </div>

    <!-- Popup untuk pesan sukses atau error -->
    <PopUp v-if="showPopup" @close="showPopup = false">
      <div :class="popupType === 'success' ? 'text-green-600' : 'text-red-600'">
        {{ popupMessage }}
      </div>
    </PopUp>
  </main>
</template>
