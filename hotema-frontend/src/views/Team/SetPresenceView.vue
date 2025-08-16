<!-- SetPresenceView.vue -->
<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSetPresenceStore } from '@/stores/setPresence'

const route = useRoute()
const presenceStore = useSetPresenceStore()

const selectedDate = ref(null)
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const userId = Number(route.params.id)

const fetchData = () => {
  presenceStore.fetchPresence(userId, currentMonth.value + 1, currentYear.value)
}

const infoByDate = computed(() => {
  let map = {}
  presenceStore.dates.forEach((d, i) => {
    const day = new Date(d).getDate()
    map[day] = presenceStore.infoByDate[i]
  })
  return map
})

const daysInMonth = (year, month) => new Date(year, month + 1, 0).getDate()
const firstDayOfMonth = (year, month) => new Date(year, month, 1).getDay()

const days = computed(() => {
  const total = daysInMonth(currentYear.value, currentMonth.value)
  const firstDay = firstDayOfMonth(currentYear.value, currentMonth.value)
  let dates = []
  for (let i = 0; i < (firstDay === 0 ? 6 : firstDay - 1); i++) {
    dates.push(null)
  }
  for (let i = 1; i <= total; i++) {
    dates.push({
      day: i,
      info: infoByDate.value[i] || 'Libur'
    })
  }
  return dates
})

const selectDate = (day) => {
  if (!day) return
  selectedDate.value = day
}

const setShift = async (shiftId) => {
  if (!selectedDate.value) return
  const dateStr = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(selectedDate.value.day).padStart(2, '0')}`
  await presenceStore.setShift(userId, dateStr, shiftId)
  selectedDate.value.info = presenceStore.infoByDate[selectedDate.value.day] // update tampilan
}

onMounted(fetchData)
watch([currentMonth, currentYear], fetchData)
</script>

<template>
  <main class="h-[100vh] bg-[#f4f4f6] font-poppins pt-8">
    <div class="flex ml-8">
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
    <div class="p-6 bg-white rounded-lg shadow-md max-w-2xl mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold">Set Absensi - {{ userId }}</h2>
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

      <!-- Grid hari -->
      <div class="grid grid-cols-7 gap-2 text-center font-semibold text-gray-600">
        <div>Senin</div><div>Selasa</div><div>Rabu</div><div>Kamis</div>
        <div>Jumat</div><div>Sabtu</div><div>Minggu</div>
      </div>

      <div v-if="presenceStore.loading" class="text-center py-4">Loading...</div>
      <div v-else-if="presenceStore.error" class="text-center py-4 text-red-500">
        {{ presenceStore.error }}
      </div>

      <!-- Tanggal -->
      <div v-else class="grid grid-cols-7 gap-2 text-center mt-2">
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

      <!-- Menu -->
      <div v-if="selectedDate" class="mt-4 p-4 bg-gray-100 rounded shadow">
        <p class="font-semibold mb-2">
          Tanggal {{ selectedDate.day }} - {{ selectedDate.info }}
        </p>
        <div class="flex gap-2">
          <button @click="setShift(1)" class="px-3 py-1 bg-green-500 text-white rounded">Set Shift Pagi</button>
          <button @click="setShift(2)" class="px-3 py-1 bg-yellow-500 text-white rounded">Set Shift Siang</button>
          <button @click="setShift(3)" class="px-3 py-1 bg-purple-500 text-white rounded">Set Shift Malam</button>
          <button @click="setShift('libur')" class="px-3 py-1 bg-red-500 text-white rounded">Set Libur</button>

        </div>
      </div>
    </div>
  </main>
</template>
