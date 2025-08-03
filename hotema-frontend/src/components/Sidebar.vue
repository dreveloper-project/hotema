<script setup>
import { useAuthStore } from '@/stores/authStoreB'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push({
      name: "login",}) 
}
</script>

<template>
  <div id="sidebar" class="font-poppins">
    <img src="@/assets/logo.png" alt="Logo" class="logo-image" />

    <ul class=" ">

      <router-link to="/" custom v-slot="{ navigate, isActive }">
        <li @click="navigate" :class="{ 'active-menu': isActive }">
          <span>
            <IconMdiHome />
          </span>
          Menu Utama
        </li>
      </router-link>

      <router-link
        to="/assignment"
        custom
        v-slot="{ navigate, isActive }"
      >
      <li @click="navigate" :class="{ 'active-menu': isActive }">
        <span>
          <IconIcBaselineAssignment />
        </span>
        Penugasan
      </li>
       </router-link>

      <router-link
        to="/occupancy-management"
        custom
        v-slot="{ navigate, isActive }"
      >
        <li @click="navigate" :class="{ 'active-menu': isActive }">
          <span>
            <IconIcBaselineLocalHotel />
          </span>
          Manajemen Okupansi
        </li>
      </router-link>

       <router-link
        to="/team-management"
        custom
        v-slot="{ navigate, isActive }"
      >
      <li @click="navigate" :class="{ 'active-menu': isActive }">
        <span>
          <IconIcBaselinePerson />
        </span>
        Manajemen Pegawai
      </li>
       </router-link>

      <router-link
        to="/settings"
        custom
        v-slot="{ navigate, isActive }"
      >
      <li @click="navigate" :class="{ 'active-menu': isActive }">
        <span>
          <IconIcBaselineSettings />
        </span>
        Pengaturan
      </li>
      </router-link>
    </ul>
    <ul class="">
      <li class=" cursor-pointer "  @click="handleLogout">
        <span>
          <IconMdiAccountArrowRightOutline />
        </span>
        Log Out
      </li>
    </ul>
  </div>
</template>

<style>
@reference "tailwindcss";

#sidebar {
  @apply fixed h-[100vh] w-[21.145vw] bg-[#f4f4f6] flex flex-col;
}

#sidebar ul {
  @apply flex flex-col items-center gap-[1rem] ml-[-1rem] mt-[4rem];
}

li {
  @apply text-[#333] text-[0.75rem] font-medium py-[0.28rem] px-2.5  w-[72.333%]  flex gap-1.5 items-center cursor-pointer transition-all duration-200;
}

li:hover {
  @apply text-[#910a67] shadow-md rounded-lg scale-105;
}
li span {
  @apply p-[0.35rem] bg-[#f4f4f6] rounded-md shadow-md text-[0.87rem];
}

li.active-menu {
  @apply rounded-lg shadow-xl;
}

li.active-menu span {
  @apply bg-[#910a67] text-[#f4f4f6];
}

#sidebar .logo-image {
  @apply w-[130px] ml-[13%] mt-[1.22rem];
}
</style>
