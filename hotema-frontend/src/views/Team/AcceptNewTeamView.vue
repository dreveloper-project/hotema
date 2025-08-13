<script setup>
import Sidebar from '@/components/Sidebar.vue'
import OccupancyTable from '@/components/OccupancyTable.vue'
import { ref, computed, onMounted } from 'vue'
import { useTeamManagementStore } from '@/stores/teamManagement'
import ProgressSpinner from 'primevue/progressspinner'

const selectedRole = ref('staff')
const teamStore = useTeamManagementStore()

onMounted(() => {
  teamStore.fetchUsersWithoutRole()
})

const filteredData = computed(() =>
  Array.isArray(teamStore.usersWithoutRole)
    ? teamStore.usersWithoutRole.filter(
        (item) => item.role === selectedRole.value
      )
    : []
)

function showDetail(person) {
  alert(`Detail untuk ${person.fullname}`)
}
</script>

<template>
  <Sidebar />
  <main
    class="bg-[#f4f4f6] min-w-[calc(21.145vw-98vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto relative font-poppins"
  >
    <div class="bg-white rounded-lg p-6 w-[97%] text-[0.82rem]">
      <div class="overflow-x-auto">
        
        <!-- Table -->
        <table
          class="w-full border-collapse"
          v-if="!teamStore.loading && !teamStore.error"
        >
          <thead>
            <tr class="bg-gray-100 text-gray-700">
              <th class="text-left px-4 py-2">Nama Lengkap</th>
              <th class="text-left px-4 py-2">Posisi</th>
              <th class="px-4 py-2 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="person in filteredData"
              :key="person.user_id || person.fullname"
              class="border-b hover:bg-gray-50"
            >
              <td class="px-4 py-2 flex items-center gap-3">
                <img
                  :src="person.pictures || '/default-avatar.png'"
                  alt="Foto Profil"
                  class="w-8 h-8 rounded-full object-cover"
                />
                <span>{{ person.fullname }}</span>
              </td>
              <td class="px-4 py-2">{{ person.role || 'Tidak ada' }}</td>
              <td class="px-4 py-2 text-center">
                <button
                  class="bg-blue-500 text-white px-4 py-1 rounded-lg hover:bg-blue-600 transition"
                  @click="showDetail(person)"
                >
                  Detail
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
  </main>
</template>
