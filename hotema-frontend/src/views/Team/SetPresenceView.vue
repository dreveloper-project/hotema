<script setup>
import { ref, computed, watch } from 'vue'
import { useSetPresence } from '@/stores/setPresence'
import { storeToRefs } from 'pinia'
import { useRoute } from 'vue-router'

const route = useRoute()
const userId = Number(route.params.id)

const selectedDate = ref(null)
const currentMonth = ref(new Date().getMonth()) // 0-based
const currentYear = ref(new Date().getFullYear())

// Store Pinia (sudah konek ke endpoint di store)
const attendanceStore = useSetPresence()
const { infoByDate, loading, error } = storeToRefs(attendanceStore)

// Fetch data absensi tiap kali bulan/tahun berubah
watch([currentMonth, currentYear], () => {
  attendanceStore.fetchAttendance(userId, currentMonth.value + 1, currentYear.value)
}, { immediate: true })

// Helper tanggal
const daysInMonth = (year, month) => new Date(year, month + 1, 0).getDate()
const firstDayOfMonth = (year, month) => new Date(year, month, 1).getDay()

// Buat daftar tanggal dengan data dari backend
const days = computed(() => {
  const total = daysInMonth(currentYear.value, currentMonth.value)
  const firstDay = firstDayOfMonth(currentYear.value, currentMonth.value)

  let dates = []
  // Kosong sebelum tanggal 1
  for (let i = 0; i < (firstDay === 0 ? 6 : firstDay - 1); i++) {
    dates.push(null)
  }
  // Isi tanggal dengan info dari API
  for (let i = 1; i <= total; i++) {
    dates.push({
      day: i,
      info: infoByDate.value[i] || 'Libur'
    })
  }
  return dates
})

// Pilih tanggal
const selectDate = (day) => {
  if (!day) return
  selectedDate.value = day
}

// Set shift ke backend via store
const setShift = async (shiftType) => {
  if (!selectedDate.value) return
  await attendanceStore.setAttendance(
    userId,
    selectedDate.value.day,
    currentMonth.value + 1,
    currentYear.value,
    shiftType
  )
}

// Hapus shift → jadi Libur
const deleteShift = async () => {
  if (!selectedDate.value) return
  await attendanceStore.deleteAttendance(
    userId,
    selectedDate.value.day,
    currentMonth.value + 1,
    currentYear.value
  )
}
</script>

<template>
  <main class="bg-[#f4f4f6] h-[100vh] pt-8">
    <div class="p-6 bg-white rounded-lg shadow-md max-w-2xl mx-auto font-poppins">
      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold">
          Set Absensi - User {{ userId }}
        </h2>
        <div>
          <select v-model="currentMonth" class="border rounded p-1 mr-2">
            <option v-for="m in 12" :key="m-1" :value="m-1">
              {{ new Date(2000, m-1).toLocaleString('id-ID', { month: 'long' }) }}
            </option>
          </select>
          <select v-model="currentYear" class="border rounded p-1">
            <option v-for="y in 5" :key="y" :value="2023+y">{{ 2023+y }}</option>
          </select>
        </div>
      </div>

      <!-- Error & Loading -->
      <div v-if="loading" class="text-blue-500 mb-2">Memuat data...</div>
      <div v-if="error" class="text-red-500 mb-2">{{ error }}</div>

      <!-- Nama Hari -->
      <div class="grid grid-cols-7 gap-2 text-center font-semibold text-gray-600">
        <div>Senin</div>
        <div>Selasa</div>
        <div>Rabu</div>
        <div>Kamis</div>
        <div>Jumat</div>
        <div>Sabtu</div>
        <div>Minggu</div>
      </div>

      <!-- Kalender -->
      <div class="grid grid-cols-7 gap-2 text-center mt-2">
        <div
          v-for="(day, index) in days"
          :key="index"
          @click="selectDate(day)"
          :class="[ 
            'p-2 rounded cursor-pointer h-16 flex flex-col justify-center items-center',
            day && selectedDate?.day === day.day ? 'bg-blue-200' : 'hover:bg-gray-200',
            !day ? 'bg-transparent cursor-default' : 'bg-white'
          ]"
        >
          <span v-if="day" class="font-bold">{{ day.day }}</span>
          <span v-if="day" class="text-xs text-gray-500">{{ day.info }}</span>
        </div>
      </div>

      <!-- Menu shift -->
      <div v-if="selectedDate" class="mt-4 p-4 bg-gray-100 rounded shadow">
        <p class="font-semibold mb-2">
          Tanggal {{ selectedDate.day }} - {{ selectedDate.info }}
        </p>
        <div class="flex gap-2 flex-wrap">
          <button @click="setShift('Shift Pagi')" class="px-3 py-1 bg-green-500 text-white rounded">Set Shift Pagi</button>
          <button @click="setShift('Shift Siang')" class="px-3 py-1 bg-yellow-500 text-white rounded">Set Shift Siang</button>
          <button @click="setShift('Shift Malam')" class="px-3 py-1 bg-purple-500 text-white rounded">Set Shift Malam</button>
          <button @click="deleteShift" class="px-3 py-1 bg-red-500 text-white rounded">Hapus Shift (Libur)</button>
        </div>
      </div>
    </div>
  </main>
</template>
