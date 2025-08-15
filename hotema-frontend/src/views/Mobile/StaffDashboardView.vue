<script setup>

import router from '@/router'
import { useAuthStore } from '@/stores/authStoreB'
import { storeToRefs } from 'pinia'


const auth = useAuthStore()
const { user } = storeToRefs(auth)
const handleLogout = () => {
  auth.logout()
   router.push({
    name: 'login', // atau path: '/dashboard'
    query: { message: 'Logout Berhasil' }
  })
}
</script>
<template>
  <div
    class="flex min-h-screen bg-gradient-to-br from-[#910a67] to-[#ee4dbb] py-4 items-center justify-center px-4"
  >
    <div
      class="flex flex-col items-center text-[#f5f5f5] w-full max-w-md font-poppins py-6 px-4"
    >
      <h1 class="font-bold text-2xl sm:text-3xl text-center">
        Selamat Datang!
      </h1>
      <h2 class="text-lg sm:text-xl mt-1">{{ user.fullname }}</h2>

      <div
        class="button-container flex flex-col items-center my-6 gap-4 w-full"
      >
        <router-link to="/staff/task" custom v-slot="{ navigate }">
          <button @click="navigate">
            <span><IconMaterialSymbolsCleaningServicesSharp class="" /></span
            >Pekerjaan Hari Ini
          </button>
        </router-link>
        <button>
          <span><IconMaterialSymbolsBookmarkCheckRounded /></span>Absensi
        </button>
        <button>
          <span><IconMaterialSymbolsSettingsAccountBox /> </span>Pengaturan
        </button>
        <button @click="handleLogout" class="mt-6">
          <span><IconMaterialSymbolsLogoutRounded /></span>Logout
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

.button-container button {
  @apply outline-[#fff] outline-2 outline-solid text-[#fff] rounded-lg cursor-pointer py-3 w-[80%] max-w-xs transition duration-200 hover:bg-[#f5f5f5] hover:text-[#333] flex pl-2 items-center gap-2;
}
.button-container button span {
  @apply bg-[#fff] rounded-sm p-1 text-[#910a67];
}
</style>
