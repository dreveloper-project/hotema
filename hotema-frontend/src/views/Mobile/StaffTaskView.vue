<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useStaffTaskStore } from '@/stores/staffTask'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStoreB'

const auth = useAuthStore()
const { user } = storeToRefs(auth)

const staffTaskStore = useStaffTaskStore()
const { tasks, loading, error } = storeToRefs(staffTaskStore)

const userId = user.value.user_id 

onMounted(() => {
  staffTaskStore.fetchStaffTasks(userId)
})

function getActionButton(task) {
  if (task.record_start && !task.record_complete) {
    return 'Selesai'
  }
  if (!task.record_start && !task.record_complete) {
    return 'Mulai'
  }
  return null
}

function handleAction(task) {
  if (task.record_start && !task.record_complete) {
    staffTaskStore.completeRecord(task.record_id)
  } else if (!task.record_start && !task.record_complete) {
    staffTaskStore.startRecord(task.record_id)
  }
}
</script>

<template>
  <div class="relative shadow-md sm:rounded-lg bg-[#f4f4f6] min-h-screen flex-col items-center justify-between">
    <h1 class="mx-2 my-4 font-poppins text-2xl">Tugas Hari Ini</h1>

    <RouterLink to="/staff/dashboard" v-slot="{ navigate }">
      <button
        @click="navigate"
        class="bg-[#6b61ff] ml-2 py-1 px-2 font-poppins rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
      >
        Kembali
        <span class="ml-1">
          <IconIcBaselineKeyboardBackspace class="text-[1rem]" />
        </span>
      </button>
    </RouterLink>

    <div v-if="loading" class="p-4">Loading...</div>
    <div v-else-if="error" class="p-4 text-red-500">{{ error }}</div>

    <!-- Tambahkan wrapper overflow-x-auto -->
    <div v-else class="overflow-x-auto">
      <table
        class="w-full font-poppins text-xs sm:text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400"
      >
        <thead class="text-xs text-gray-700 uppercase dark:text-gray-400">
          <tr>
            <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Kamar</th>
            <th class="px-4 sm:px-6 py-3">Tanggal</th>
            <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Waktu Mulai</th>
            <th class="px-4 sm:px-6 py-3">Waktu Selesai</th>
            <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">QC Status</th>
            <th class="px-4 sm:px-6 py-3">QC Oleh</th>
            <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="task in tasks"
            :key="task.record_id"
            class="border-b border-gray-200 dark:border-gray-700"
          >
            <td class="px-4 sm:px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">
              {{ task.room_name }}
            </td>
            <td class="px-4 sm:px-6 py-4">{{ task.date || '-' }}</td>
            <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">
              {{ task.record_start || '-' }}
            </td>
            <td class="px-4 sm:px-6 py-4">{{ task.record_complete || '-' }}</td>
            <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">
              {{ task.tm_status || '-' }}
            </td>
            <td class="px-4 sm:px-6 py-4">
              {{ task.tm_user || '-' }}
            </td>
            <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">
              <button
                v-if="getActionButton(task)"
                @click="handleAction(task)"
                class="text-blue-600 hover:underline cursor-pointer"
              >
                {{ getActionButton(task) }}
              </button>
              <span v-else>-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
