<script setup>
import { onMounted } from 'vue'
import { useTaskMonitoringStore } from '@/stores/taskMonitoring'
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'


const taskStore = useTaskMonitoringStore()
const { tasks, loading, error } = storeToRefs(taskStore)

// fetch data saat komponen mount
onMounted(() => {
  taskStore.fetchUncheckUnapproved()
})

// format tanggal dd-mm-yyyy
const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return `${d.getDate().toString().padStart(2,'0')}-${(d.getMonth()+1).toString().padStart(2,'0')}-${d.getFullYear()}`
}

// aksi tombol approve
const approveTask = async (taskId) => {
  try {
    await taskStore.updateTaskStatus(taskId, 'Approved')
  } catch (err) {
    console.error('Gagal approve task', err)
  }
}

// aksi tombol unapprove
const unapproveTask = async (taskId) => {
  try {
    await taskStore.updateTaskStatus(taskId, 'Unapproved')
  } catch (err) {
    console.error('Gagal unapprove task', err)
  }
}
</script>


<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg bg-[#f4f4f6] min-h-screen flex-col items-center justify-between">
    <h1 class="mx-2 my-4 font-poppins text-2xl">Tugas Hari Ini</h1>
    <RouterLink to="/spv/dashboard" v-slot="{ navigate }">
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

    <table class="w-full font-poppins text-xs sm:text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase dark:text-gray-400">
        <tr>
          <th scope="col" class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Kamar</th>
          <th scope="col" class="px-4 sm:px-6 py-3">Tanggal</th>
          <th scope="col" class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Nama yang Membersihkan</th>
          <th scope="col" class="px-4 sm:px-6 py-3">QC Status</th>
          <th scope="col" class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.tm_id" class="border-b border-gray-200 dark:border-gray-700">
          <td class="px-4 sm:px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">{{ task.room_name }}</td>
          <td class="px-4 sm:px-6 py-4">{{ formatDate(task.date) }}</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">{{ task.username }}</td>
          <td class="px-4 sm:px-6 py-4">{{ task.tm_status }}</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800 flex gap-2">
            <button 
              class="bg-green-500 text-white px-2 py-1 rounded-md hover:bg-green-600" 
              @click="approveTask(task.tm_id)"
            >
              Approved
            </button>
            <button 
              class="bg-red-500 text-white px-2 py-1 rounded-md hover:bg-red-600" 
              @click="unapproveTask(task.tm_id)"
            >
              Unapproved
            </button>
          </td>
        </tr>

        <tr v-if="tasks.length === 0" class="border-b border-gray-200 dark:border-gray-700">
          <td colspan="5" class="px-4 sm:px-6 py-4 text-center text-gray-500 dark:text-gray-400">
            Tidak ada tugas hari ini
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="loading" class="mt-4 text-center text-gray-500">Loading...</div>
    <div v-if="error" class="mt-4 text-center text-red-500">{{ error }}</div>
  </div>
</template>
