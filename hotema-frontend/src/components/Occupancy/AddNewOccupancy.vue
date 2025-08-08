<script setup>
import { ref } from 'vue';
import { useOccupancyStore } from '@/stores/occupancy'
import { onMounted } from 'vue';
import api from '@/lib/axios';

const addMenu = ref(false)
const occupancyStore = useOccupancyStore()

const roomOptions = ref([])
const selectedRoom = ref(null)
const checkInDate = ref(null)
const checkOutDate = ref(null)
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  await occupancyStore.fetchRoomNames()
  roomOptions.value = occupancyStore.roomNames
})

const submitForm = async () => {
  if (!selectedRoom.value || !checkInDate.value || !checkOutDate.value) {
    error.value = 'Semua field harus diisi';
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    const formattedCheckIn = checkInDate.value.toISOString().split('T')[0];
    const formattedCheckOut = checkOutDate.value.toISOString().split('T')[0];

    const response = await api.post('room/add-occupancy/', {
      room_name: selectedRoom.value,
      check_in_date: formattedCheckIn,
      check_out_date: formattedCheckOut
    });

    // Reset form and close menu
    selectedRoom.value = null;
    checkInDate.value = null;
    checkOutDate.value = null;
    addMenu.value = false;
    
    // Refresh occupancy data
    await occupancyStore.fetchOccupancy(
      formattedCheckIn,
      formattedCheckOut
    );

    // Show success message
    console.log('Occupancy data added successfully:', response.data);
    
  } catch (err) {
    error.value = err.response?.data?.error || 'Gagal menambahkan data occupancy';
    console.error('Error adding occupancy:', err);
  } finally {
    loading.value = false;
  }
};

const closeMenu = () => {
  addMenu.value = false;
  error.value = null;
};
</script>
<template>
  <div class="relative inline-block">
    <button
      @click.stop="addMenu = !addMenu"
      class="bg-[#46b389] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
    >
      Tambahkan Data
      <span class="ml-1"><IconMaterialSymbolsLightAdd class="text-[1rem]" /></span>
    </button>

    <!-- Form Tambah Data -->
    <form
      v-if="addMenu"
      @submit.prevent="submitForm"
      class="absolute top-full left-0 mt-2 w-[300px] bg-white border border-gray-300 shadow-lg rounded-md p-4 z-50"
      @click.stop
    >
      <!-- Error Message -->
      <div v-if="error" class="mb-3 p-2 bg-red-100 text-red-700 rounded text-sm">
        {{ error }}
      </div>

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
        dateFormat="yy-mm-dd"
        placeholder="Pilih tanggal"
        showIcon
        class="w-full mb-3"
      />

      <!-- Tanggal Check-out -->
      <label class="block text-sm text-gray-600 mb-1">Tanggal Check-out</label>
      <Calendar
        v-model="checkOutDate"
        dateFormat="yy-mm-dd"
        placeholder="Pilih tanggal"
        showIcon
        class="w-full mb-4"
      />

      <!-- Loading State -->
      <div v-if="loading" class="text-center text-sm text-gray-600 mb-3">
        Menyimpan data...
      </div>

      <!-- Tombol Simpan -->
      <div class="flex justify-end space-x-2">
        <button 
          type="button" 
          @click="closeMenu"
          class="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400 text-sm"
        >
          Batal
        </button>
        <button 
          type="submit" 
          :disabled="loading"
          class="bg-[#46b389] text-white px-4 py-2 rounded hover:bg-[#3ca477] text-sm disabled:opacity-50"
        >
          {{ loading ? 'Menyimpan...' : 'Simpan' }}
        </button>
      </div>
    </form>
  </div>
</template>
