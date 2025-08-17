<script setup>
import router from '@/router'
import { useAuthStore } from '@/stores/authStoreB'
import { useUserAbsentStore } from '@/stores/userAbsent'
import { storeToRefs } from 'pinia'
import { computed, watch } from 'vue'
import { useToast } from 'primevue/usetoast'

const toast = useToast()

const auth = useAuthStore()
const { user, token } = storeToRefs(auth)

const absentStore = useUserAbsentStore()
const { status, loading } = storeToRefs(absentStore)

const displayName = computed(() => user.value?.fullname || user.value?.username || 'Guest')

// 🔔 Toast ketika status berubah
watch(status, (newStatus, oldStatus) => {
  if (newStatus && newStatus !== oldStatus) {
    if (newStatus === 'Absen Pulang') {
      toast.add({
        severity: 'success',
        summary: 'Absen Masuk',
        detail: 'Absen masuk berhasil dicatat!',
        life: 3000
      })
    } else if (newStatus === 'Pekerjaan Sudah Selesai') {
      toast.add({
        severity: 'info',
        summary: 'Absen Pulang',
        detail: 'Absen pulang berhasil, pekerjaan selesai!',
        life: 3000
      })
    }
  }
})

const handleLogout = () => {
  auth.logout()
  router.push({ name: 'login', query: { message: 'Logout Berhasil' } })
}

const handleAbsentClick = async () => {
  if (!user.value?.user_id) return

  if (status.value === null || status.value === 'Absen Masuk') {
    await absentStore.absentIn(user.value.user_id)
  } else if (status.value === 'Absen Pulang') {
    await absentStore.absentOut(user.value.user_id)
  }
}

// 🔒 Cek akses ke task monitoring
const handleTaskMonitoring = (navigate) => {
  if (status.value === null || status.value === 'Absen Masuk') {
    toast.add({
      severity: 'warn',
      summary: 'Akses Ditolak',
      detail: 'Silakan absen masuk terlebih dahulu sebelum memantau pekerjaan.',
      life: 3000
    })
  } else {
    navigate() // lanjut ke halaman monitoring
  }
}
</script>

<template>
  <div class="flex min-h-screen bg-gradient-to-br from-[#910a67] to-[#ee4dbb] py-4 items-center justify-center px-4">
    <div class="flex flex-col items-center text-[#f5f5f5] w-full max-w-md font-poppins py-6 px-4">
      <!-- ✅ Toast component -->
      <Toast />

      <h1 class="font-bold text-2xl sm:text-3xl text-center">Selamat Datang!</h1>
      <h2 class="text-lg sm:text-xl mt-1">{{ displayName }}</h2>

      <div class="button-container flex flex-col items-center my-6 gap-4 w-full">
        <!-- Pantau Pekerjaan (blokir jika belum absen masuk) -->
        <router-link to="/staff/task" custom v-slot="{ navigate }">
          <button @click="handleTaskMonitoring(navigate)">
            <span><IconMaterialSymbolsCleaningServicesSharp /></span>
            Tugas Hari Ini
          </button>
        </router-link>

        <!-- Tombol Absensi -->
        <button
          :disabled="status === 'Pekerjaan Sudah Selesai'"
          @click="handleAbsentClick"
        >
          <span><IconMaterialSymbolsBookmarkCheckRounded /></span>
          <template v-if="loading">Loading...</template>
          <template v-else-if="status === 'Absen Pulang'">Absen Pulang</template>
          <template v-else-if="status === 'Pekerjaan Sudah Selesai'">Selesai</template>
          <template v-else>Absen Masuk</template>
        </button>

        <button>
          <span><IconMaterialSymbolsSettingsAccountBox /> </span>Pengaturan
        </button>
        <button class="mt-6" @click="handleLogout">
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