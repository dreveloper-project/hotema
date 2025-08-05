<script setup>
import { format } from 'date-fns'
import Sidebar from '../components/Sidebar.vue'
import NotifCard from '@/components/NotifCard.vue';
import RoomStatus from '@/components/RoomStatus.vue';
import { onMounted, ref, watch} from 'vue';
import DatePicker from 'primevue/datepicker';

import { useRoomRecordStore } from '@/stores/roomRecord'

const roomStore = useRoomRecordStore()

const currentDate = ref(new Date());
onMounted(() => {
  roomStore.fetchTodayRecords()
  
})

watch(currentDate, (newDate) => {
  const formattedDate = format(newDate, 'yyyy-MM-dd')
  roomStore.fetchRecordsByDate(formattedDate)
})
</script>

<template>
  <Sidebar />
  <main class="bg-[#f4f4f6] min-w-[calc(21.145vw-100vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto " >
    <NotifCard v-if="roomStore.error" :notif-type="'error'" :notif-message="roomStore.error" />
    <DatePicker class="my-5 font-poppins" v-model="currentDate" />
    <RoomStatus :records="roomStore.records" />
  </main>
</template>

<style scoped>
@reference "tailwindcss";
</style>