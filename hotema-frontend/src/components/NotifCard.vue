<template>
  <main class="flex justify-center items-center gap-4 p-5 font-poppins bg-[#f4f4f6] w-[100vw] h-[100vh]">
    <div class="bg-white rounded-lg shadow-md px-6 py-8 w-[350px]">
      <h1 class="text-center font-bold mt-4">Tugaskan Staff !</h1>

      <!-- Notif -->
      <NotifCard 
        v-if="notifMessage" 
        :notifType="notifType" 
        :notifMessage="notifMessage" 
      />

      <!-- Date Picker -->
      <div class="mt-4">
        <label class="block mb-1 text-sm font-medium">Tanggal</label>
        <DatePicker 
          v-model="selectedDate" 
          dateFormat="yy-mm-dd" 
          showIcon 
          class="w-full" 
        />
      </div>

      <!-- Option Nama Kamar -->
      <div class="mt-4">
        <label class="block mb-1 text-sm font-medium">Nama Kamar</label>
        <Dropdown 
          v-model="selectedRoom" 
          :options="roomOptions" 
          optionLabel="label" 
          optionValue="value" 
          placeholder="Pilih kamar" 
          class="w-full"
          :disabled="!roomOptions.length"
        />
      </div>

      <!-- Option Nama Orang -->
      <div class="mt-4">
        <label class="block mb-1 text-sm font-medium">Nama Orang</label>
        <Dropdown 
          v-model="selectedPerson" 
          :options="staffOptions" 
          optionLabel="label" 
          optionValue="value" 
          placeholder="Pilih orang" 
          class="w-full"
          :disabled="!staffOptions.length"
        />
      </div>

      <!-- Tombol Simpan -->
      <Button 
        label="Tugaskan" 
        class="w-full bg-blue-500 text-white mt-4 hover:bg-blue-600 rounded-lg" 
        @click="saveData"
        :disabled="!selectedRoom || !selectedPerson"
      />
    </div>
  </main>
</template>

<script setup>
import { ref, watch } from 'vue'
import DatePicker from 'primevue/datepicker'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'

// Import store dan notif
import { useAssignmentStore } from '@/stores/assignment'
import NotifCard from '@/components/NotifCard.vue'

const assignmentStore = useAssignmentStore()

// State
const selectedDate = ref(null)
const selectedRoom = ref(null)
const selectedPerson = ref(null)

const roomOptions = ref([])
const staffOptions = ref([])

const notifMessage = ref(null)
const notifType = ref(null)

// Watch date → fetch data setiap kali date berubah
watch(selectedDate, async (newDate) => {
  if (newDate) {
    await assignmentStore.fetchStaffByDate(newDate)

    if (assignmentStore.message) {
      notifMessage.value = assignmentStore.message
      notifType.value = 'warning'

      // kosongkan dropdown
      roomOptions.value = []
      staffOptions.value = []
      selectedRoom.value = null
      selectedPerson.value = null
    } else {
      notifMessage.value = null
      notifType.value = null

      // Mapping rooms → option
      roomOptions.value = assignmentStore.rooms.map(r => ({
        label: r.room_name,
        value: r.room_id
      }))
      // Mapping staff → option
      staffOptions.value = assignmentStore.staff.map(s => ({
        label: s.full_name,
        value: s.user_id
      }))
    }
  }
})

// Simpan handler sementara
const saveData = () => {
  console.log({
    tanggal: selectedDate.value,
    kamar: selectedRoom.value,
    orang: selectedPerson.value
  })
}
</script>
