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
   <div class="my-5 flex items-center justify-center w-[75%] font-poppins gap-4">
  <h3 class="text-[#333] flex-1 text-center">Ubah Hari :</h3>

  <DatePicker class="font-medium flex-1" v-model="currentDate" />

  <RouterLink to="/assignment/add/room" v-slot="{ navigate, isActive }" class="flex-1">
    <button
      @click="navigate"
      :class="[ 
        'bg-[#46b355] py-2 px-2 rounded-md text-[#f4f4f6] text-[0.87rem] font-light mb-2 flex items-center justify-center cursor-pointer transition-all hover:scale-105 w-full',
        isActive ? 'ring-2 ring-white' : ''
      ]"
    >
      Tambahkan Kamar
      <span class="ml-1">
        <IconMaterialSymbolsLightAdd />
      </span>
    </button>
  </RouterLink>

  <RouterLink to="/task-log" v-slot="{ navigate, isActive }" class="flex-1">
    <button
      @click="navigate"
      :class="[ 
        'bg-[#eea00f] py-2 px-2 rounded-md text-[#f4f4f6] text-[0.87rem] font-light mb-2 flex items-center justify-center cursor-pointer transition-all hover:scale-105 w-full',
        isActive ? 'ring-2 ring-white' : ''
      ]"
    >
      Log Tugas
      <span class="ml-1">
        <IconMaterialSymbolsLightAdd />
      </span>
    </button>
  </RouterLink>
</div>

    <RoomStatus v-if="!roomStore.error" :records="roomStore.records" />
  </main>
</template>

<style scoped>
@reference "tailwindcss";
</style>