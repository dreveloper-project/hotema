<script setup>
import Sidebar from '../components/Sidebar.vue'
import OccupancyTable from '@/components/OccupancyTable.vue';

import { ref, computed } from 'vue';

const selectedRole = ref('staff')

const data = ref([
  { name: 'Peter Onana',  role: 'staff' },
  { name: 'Todd Steven',  role: 'supervisor' },
  { name: 'Adam Levine',  role: 'staff' },
  { name: 'Lisa Martinez',  role: 'supervisor' },
])

const filteredData = computed(() =>
  data.value.filter((item) => item.role === selectedRole.value)
)

function showDetail(person) {
  alert(`Detail untuk ${person.name}`)
}
</script>

<template>
  <Sidebar />
  <main
    class="bg-[#f4f4f6] min-w-[calc(21.145vw-98vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto relative font-poppins"
  >
  <div class="flex justify-end  w-[97%] gap-2 ">
    <button
    
      class="bg-[#46b389] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
    >
      Set Absensi
      <span class="ml-1"><IconMaterialSymbolsLightAdd class="text-[1rem]" /></span>
    </button>
    <RouterLink to="/team-management/accept-new-team" v-slot="{ navigate, isActive }">
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
      <!-- Select di atas tabel -->
      <div class="mb-4">
        <select
          v-model="selectedRole"
          class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="staff">Staff</option>
          <option value="supervisor">Supervisor</option>
        </select>
      </div>

      <!-- Tabel -->
      <div class="overflow-x-auto">
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-100 text-gray-700">
              <th class="text-left px-4 py-2">Nama Lengkap</th>
              <th class="text-left px-4 py-2">Posisi</th>
              <th class="px-4 py-2 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(person, index) in filteredData"
              :key="index"
              class="border-b hover:bg-gray-50"
            >
              <td class="px-4 py-2">{{ person.name }}</td>
              <td class="px-4 py-2">{{ person.role }}</td>
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
      </div>
    </div>
  </main>
</template>
