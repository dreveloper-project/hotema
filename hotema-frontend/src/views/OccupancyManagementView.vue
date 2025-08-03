<script setup>
import Sidebar from '../components/Sidebar.vue'
import OccupancyTable from '@/components/OccupancyTable.vue'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'

// Data dan kontrol form
const addMenu = ref(false)
const roomOptions = [101, 102, 103, 105, 106, 108]
const selectedRoom = ref(null)
const checkInDate = ref(null)
const checkOutDate = ref(null)

// Tutup form jika klik di luar area
const formRef = ref(null)
function handleClickOutside(event) {
  if (formRef.value && !formRef.value.contains(event.target)) {
    addMenu.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))

// Submit
function submitForm() {
  alert(`Kamar: ${selectedRoom.value}, Check-in: ${checkInDate.value}, Check-out: ${checkOutDate.value}`)
  addMenu.value = false
  selectedRoom.value = null
  checkInDate.value = null
  checkOutDate.value = null
}
</script>

<template>
  <Sidebar />

  <main class="bg-[#f4f4f6] min-w-[calc(21.145vw-100vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto relative font-poppins">
    <!-- Tombol + Form -->
    <div class="relative inline-block">
      <button
        @click.stop="addMenu = !addMenu"
        class="bg-[#46b389] py-2 px-3  rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
      >
        Tambahkan Data
        <span class="ml-1"><IconMaterialSymbolsLightAdd class="text-[1rem]" /></span>
      </button>

      <!-- Form Tambah Data -->
      <form
        ref="formRef"
        v-if="addMenu"
        @submit.prevent="submitForm"
        class="absolute top-full left-0 mt-2 w-[300px] bg-white border border-gray-300 shadow-lg rounded-md p-4 z-50"
      >
        <!-- Dropdown Kamar -->
        <label class="block text-sm text-gray-600 mb-1">Pilih Kamar</label>
        <Dropdown
          v-model="selectedRoom"
          :options="roomOptions"
          placeholder="Pilih kamar"
          class="w-full mb-3"
        />

        <!-- Tanggal Check-in -->
        <label class="block text-sm text-gray-600 mb-1">Tanggal Check-in</label>
        <Calendar
          v-model="checkInDate"
          dateFormat="dd M yy"
          placeholder="Pilih tanggal"
          showIcon
          class="w-full mb-3"
        />

        <!-- Tanggal Check-out -->
        <label class="block text-sm text-gray-600 mb-1">Tanggal Check-out</label>
        <Calendar
          v-model="checkOutDate"
          dateFormat="dd M yy"
          placeholder="Pilih tanggal"
          showIcon
          class="w-full mb-4"
        />

        <!-- Tombol Simpan -->
        <div class="flex justify-end">
          <button type="submit" class="bg-[#46b389] text-white px-4 py-2 rounded hover:bg-[#3ca477] text-sm">
            Simpan
          </button>
        </div>
      </form>
    </div>

    <!-- Komponen Tabel -->
    <OccupancyTable />
  </main>
</template>

<style scoped>
/* Tidak ada tambahan, semua pakai tailwind */
</style>
