<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import PopUp from '@/components/PopUp.vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStoreB'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const isMobile = ref(false)
const message = ref('')
const isOpen = ref(false)

const username = ref('')
const password = ref('')

function checkIsMobile() {
  isMobile.value = window.matchMedia('(max-width: 768px)').matches
}

onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', checkIsMobile)

  if (route.query.message) {
    message.value = route.query.message
    isOpen.value = true
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', checkIsMobile)
})

watch(
  () => route.query.message,
  (newVal) => {
    if (newVal) {
      message.value = newVal
      isOpen.value = true
    }
  }
)

async function handleLogin(e) {
  e.preventDefault()
  const success = await auth.login({
    username: username.value,
    password: password.value,
  })
  if (success) {
     router.push({ name: 'home' }) // Ganti dengan route tujuan setelah login
  } else {
    message.value =
      auth.error?.error || auth.error?.detail || 'Login gagal. Cek username/password.'
    isOpen.value = true
  }
}
</script>

<template>
  <!-- POPUP PESAN -->
  <PopUp v-if="isOpen" @close="isOpen = false" class="font-poppins">
    <h2 class="text-xl font-semibold mb-4">Pesan</h2>
    <p class="mb-4">{{ message }}</p>
    <button
      @click="isOpen = false"
      class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
    >
      Tutup
    </button>
  </PopUp>

  <!-- HALAMAN LOGIN -->
  <div class="flex font-poppins w-[100vw]">
    <!-- SIDE PANEL DESKTOP -->
    <aside
      v-if="!isMobile"
      class="w-[60%] bg-[#f4f4f6] h-[100vh] relative flex justify-center p-[4rem] flex-col text-[#333]"
    >
      <img src="@/assets/logo.png" alt="Logo" class="w-[50%]" />
      <div class="pl-2">
        <h1 class="text-2xl">Hotel Team Management ©</h1>
        <h2>Aplikasi Berbasis Web Privat, Untuk Manajemen Tim Housekeeping!</h2>
      </div>
    </aside>

    <!-- FORM LOGIN -->
    <div
      class="w-full lg:w-[40%] sticky bg-[#910a67] h-[100vh] flex flex-col items-center justify-center p-3"
    >
      <div class="flex flex-col items-center justify-center bg-gray-100 rounded-md shadow-md py-5 px-2">
        <div v-if="isMobile" class="flex flex-col relative items-center">
          <img src="@/assets/logo.png" alt="Logo" class="w-[60%]" />
          <div class="pl-2">
            <h1 class="text-[0.89rem]">Hotel Team Management ©</h1>
          </div>
        </div>

        <form @submit="handleLogin" class="w-80 rounded-lg p-6 flex flex-col gap-4">
          <h2 class="text-xl font-semibold">Masuk Ke Sistem..</h2>

          <div class="flex flex-col">
            <label for="username" class="text-sm mb-1">Username:</label>
            <input
              v-model="username"
              type="text"
              id="username"
              class="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#910a67]"
            />
          </div>

          <div class="flex flex-col">
            <label for="password" class="text-sm mb-1">Password:</label>
            <input
              v-model="password"
              type="password"
              id="password"
              class="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#910a67]"
            />
          </div>

          <button
            type="submit"
            class="bg-[#910a67] hover:bg-[#3b2434] text-white font-semibold py-2 rounded cursor-pointer"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
