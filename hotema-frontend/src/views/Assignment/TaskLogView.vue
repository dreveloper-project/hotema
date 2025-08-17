<script setup>
import { onMounted } from 'vue'
import { useFetchRecordStore } from '@/stores/fetchRecord'
import { storeToRefs } from 'pinia'

// pakai store
const recordStore = useFetchRecordStore()
const { records, loading, error, message } = storeToRefs(recordStore)

// fetch saat komponen mount
onMounted(() => {
  recordStore.fetchRecords()
})

// fungsi helper warna status
const getStatusClass = (status) => {
  if (status === 'Approved') return 'text-green-600 font-medium'
  if (status === 'Pending') return 'text-yellow-600 font-medium'
  if (status === 'Rejected') return 'text-red-600 font-medium'
  return 'text-gray-500'
}

// hapus dengan konfirmasi
const handleDelete = async (recordId) => {
  if (confirm('Yakin ingin menghapus record ini?')) {
    await recordStore.deleteRecord(recordId)
  }
}
</script>

<template>
  <div class="flex pl-5 font-poppins bg-[#f4f4f6] pt-4 justify-between">
    <RouterLink to="/Assignment" v-slot="{ navigate }">
      <button
        @click="navigate"
        class="bg-[#6b61ff] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
      >
        Kembali
        <span class="ml-1"><IconIcBaselineKeyboardBackspace class="text-[1rem]" /></span>
      </button>
    </RouterLink>
    <RouterLink to="/create-assignment" v-slot="{ navigate }">
      <button
        @click="navigate"
        class="bg-[#680e6b] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105 mr-25"
      >
        Tugaskan Seseorang
        <span class="ml-1"><IconIcOutlineAssignment class="text-[1.5rem]" /></span>
      </button>
    </RouterLink>
  </div>

  <div class="min-h-screen flex justify-center bg-[#f4f4f6] px-4 font-poppins">
    <div class="w-full max-w-6xl bg-white rounded-lg shadow">
      <!-- Loading -->
      <div v-if="loading" class="p-4 text-center text-gray-500">Loading data...</div>

      <!-- Error -->
      <div v-else-if="error" class="p-4 text-center text-red-600">{{ error }}</div>

      <!-- Message (kosong) -->
      <div v-else-if="message" class="p-4 text-center text-gray-500">{{ message }}</div>

      <!-- Tabel -->
      <table v-else class="w-full text-sm text-left text-gray-600">
        <thead class="text-xs uppercase text-gray-100 bg-[#680e6b]">
          <tr>
            <th class="px-6 py-3">Kamar</th>
            <th class="px-6 py-3">Tanggal</th>
            <th class="px-6 py-3">Waktu Mulai</th>
            <th class="px-6 py-3">Waktu Selesai</th>
            <th class="px-6 py-3">Dikerjakan Oleh</th>
            <th class="px-6 py-3">Quality Check Oleh</th>
            <th class="px-6 py-3">Status QC</th>
            <th class="px-6 py-3 text-right">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(record, index) in records"
            :key="index"
            class="border-b hover:bg-gray-50"
          >
            <td class="px-6 py-3">{{ record.kamar }}</td>
            <td class="px-6 py-3">{{ record.jadwal }}</td>
            <td class="px-6 py-3">{{ record.waktu_mulai || '-' }}</td>
            <td class="px-6 py-3">{{ record.waktu_selesai || '-' }}</td>
            <td class="px-6 py-3">{{ record.staff }}</td>
            <td class="px-6 py-3">{{ record.supervisor || '-' }}</td>
            <td class="px-6 py-3" :class="getStatusClass(record.qc_status)">
              {{ record.qc_status || 'Belum dicek' }}
            </td>
            <td class="px-6 py-3 text-right">
              <button
                class="text-red-500 hover:underline"
                @click="handleDelete(record.record_id)"
              >
                Hapus
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<style scoped>
@reference "tailwindcss";
button {
  @apply cursor-pointer;
}
</style>