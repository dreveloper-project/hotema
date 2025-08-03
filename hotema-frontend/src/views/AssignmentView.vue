<script setup>
import Sidebar from '../components/Sidebar.vue'
import NotifCard from '@/components/NotifCard.vue';
import RoomStatus from '@/components/RoomStatus.vue';
import { ref } from 'vue';
import DatePicker from 'primevue/datepicker';


const date = ref(new Date());
const messageOne = ref('Secara Default Sistem Akan Menunjuk Staff Yang Hadir Di Saat Yang Sama Dengan Waktu Pada Saat Kamar Kotor Untuk Membersihkan Kamar !')
</script>

<template>
  <Sidebar />
  <main class="bg-[#f4f4f6] min-w-[calc(21.145vw-100vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto " >
    <NotifCard :notif-type="'info'" :notif-message="messageOne" />
    <DatePicker class=" my-5 font-poppins" v-model="date" />
   
    <RoomStatus  />
  </main>
  
</template>

<style scoped>
@reference "tailwindcss";


</style>