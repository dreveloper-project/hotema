<script setup>
import { ref, watch } from 'vue'
import DatePicker from 'primevue/datepicker'
import Select from 'primevue/select'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'

// Import store
import { useAssignmentStore } from '@/stores/assignment'

const assignmentStore = useAssignmentStore()
const toast = useToast()

// State
const selectedDate = ref(null)
const selectedRoom = ref(null)
const selectedPerson = ref(null)

const roomOptions = ref([])
const staffOptions = ref([])

// Watch date → fetch data setiap kali date berubah
watch(selectedDate, async (newDate) => {
  if (newDate) {
    await assignmentStore.fetchStaffByDate(newDate)

    if (assignmentStore.message) {
      // Tidak ada staff → popup
      toast.add({
        severity: 'warn',
        summary: 'Peringatan',
        detail: assignmentStore.message,
        life: 3000
      })
      // kosongkan dropdown
      roomOptions.value = []
      staffOptions.value = []
    } else {
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

// 🔹 Simpan handler
const saveData = async () => {
  try {
    const result = await assignmentStore.createRecord({
      date: selectedDate.value,
      user_id: selectedPerson.value,
      room_id: selectedRoom.value
    })

    toast.add({
      severity: 'success',
      summary: 'Berhasil',
      detail: assignmentStore.message || 'Tugas berhasil ditambahkan',
      life: 3000
    })

    // reset form
    selectedRoom.value = null
    selectedPerson.value = null

  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Gagal',
      detail: assignmentStore.error || 'Gagal menyimpan data',
      life: 3000
    })
  }
}
</script>

<template>
   
  <main class="flex justify-center items-center gap-4 p-5 font-poppins bg-[#f4f4f6] relative h-[100vh] ">
    <div class="absolute z-3 left-[4rem] top-[2rem]">
         <RouterLink to="/task-log" v-slot="{ navigate }">
        <button
          @click="navigate"
          class="bg-[#6b61ff] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
        >
          Kembali
          <span class="ml-1"><IconIcBaselineKeyboardBackspace class="text-[1rem]" /></span>
        </button>
      </RouterLink>
    </div>
    
    <div class="bg-white rounded-lg shadow-md px-6 py-8 w-[350px]">
      <h1 class="text-center font-bold mt-4">Tugaskan Staff !</h1>

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
        <Select 
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
        <Select 
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

    <Toast />
  </main>
</template>


<style scoped>
body {
    background-color: #f4f4f6 !important;
}
</style>