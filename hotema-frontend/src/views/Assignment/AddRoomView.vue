<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/lib/axios'
import NotifCard from '@/components/NotifCard.vue'
import PopUp from '@/components/PopUp.vue'

const namaKamar = ref('')
const tipeKamar = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const router = useRouter()

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const kamarBaru = {
      nama_kamar: namaKamar.value,
      tipe_kamar: tipeKamar.value,
    }

    const response = await api.post('room/create/', kamarBaru)

    successMessage.value = 'Kamar berhasil ditambahkan.'

    // Tunggu beberapa detik sebelum redirect
    setTimeout(() => {
      router.push('/assignment')
    }, 1500)
  } catch (error) {
    console.error('Gagal mengirim data:', error)

    if (error.response && error.response.data?.error) {
      errorMessage.value = error.response.data.error
    } else {
      errorMessage.value = 'Terjadi kesalahan saat mengirim data.'
    }
  }
}

const handleCancel = () => {
  router.push('/assignment')
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 font-poppins">
    <div class="bg-white rounded-xl shadow-lg p-8 w-full max-w-md">
      
      <!-- Notifikasi -->
      <NotifCard v-if="errorMessage" :notif-type="'error'" :notif-message="errorMessage" />
      <PopUp v-if="successMessage" @close="isOpen = false" class="font-poppins">
    <h2 class="text-xl font-semibold mb-4">Pesan</h2>
    <p class="mb-4">{{ successMessage }}</p>
    
    
  </PopUp>

      <h2 class="text-2xl font-semibold text-center mb-6 text-gray-800">Form Tambah Kamar</h2>

      <form @submit.prevent="handleSubmit">
        <!-- Input Nama Kamar -->
        <div class="mb-4">
          <label for="namaKamar" class="block text-sm font-medium text-gray-700 mb-1">Nama Kamar</label>
          <input
            type="text"
            id="namaKamar"
            v-model="namaKamar"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#46b389]"
            placeholder="Masukkan nama kamar"
          />
        </div>

        <!-- Input Tipe Kamar -->
        <div class="mb-6">
          <label for="tipeKamar" class="block text-sm font-medium text-gray-700 mb-1">Tipe Kamar</label>
          <input
            type="text"
            id="tipeKamar"
            v-model="tipeKamar"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#46b389]"
            placeholder="Contoh: Deluxe, Suite, dll."
          />
        </div>

        <!-- Tombol Aksi -->
        <div class="flex justify-between">
          <button
            type="submit"
            class="bg-[#46b389] text-white px-4 py-2 rounded-md hover:scale-105 transition-all"
          >
            Kirim
          </button>

          <button
            type="button"
            @click="handleCancel"
            class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:scale-105 transition-all"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

body {
  @apply bg-[#f4f4f6];
}

button {
  @apply cursor-pointer;
}
</style>
