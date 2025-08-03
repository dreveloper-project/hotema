
<script setup>
import { ref } from 'vue';
const rooms = ref([
  { room_name: '101', cleanlines_status: 'In Progress', occuppation_status: 'OCC' },
  { room_name: '102', cleanlines_status: 'Clean', occuppation_status: 'OO' },
  { room_name: '103', cleanlines_status: 'Dirty', occuppation_status: 'VR' },
  { room_name: '104', cleanlines_status: 'In Progress', occuppation_status: 'CO' },
  { room_name: '105', cleanlines_status: 'Clean', occuppation_status: 'VD' },
  { room_name: '106', cleanlines_status: 'Dirty', occuppation_status: 'OCC' },
  { room_name: '107', cleanlines_status: 'Clean', occuppation_status: 'OO' },
  { room_name: '108', cleanlines_status: 'In Progress', occuppation_status: 'VR' },
  { room_name: '109', cleanlines_status: 'Dirty', occuppation_status: 'CO' },
  { room_name: '110', cleanlines_status: 'Clean', occuppation_status: 'VD' },
  { room_name: '111', cleanlines_status: 'In Progress', occuppation_status: 'OCC' },
  { room_name: '112', cleanlines_status: 'Clean', occuppation_status: 'OO' },
  { room_name: '113', cleanlines_status: 'Dirty', occuppation_status: 'VR' },
  { room_name: '114', cleanlines_status: 'In Progress', occuppation_status: 'CO' },
  { room_name: '115', cleanlines_status: 'Clean', occuppation_status: 'VD' },
  { room_name: '116', cleanlines_status: 'Dirty', occuppation_status: 'OO' },
  { room_name: '117', cleanlines_status: 'In Progress', occuppation_status: 'VR' },
  { room_name: '118', cleanlines_status: 'Clean', occuppation_status: 'CO' }
])

</script>

<template>

<div id="room-status" class="font-poppins" >
    <div v-for="room in rooms" :key="room.room_name"  class="room-card">
        <h3>{{ room.room_name }}</h3>
        <p>{{ room.cleanlines_status }}</p>
        <h4>
            {{ room.occuppation_status }}
        </h4>
        
    </div>
    
   
</div>

</template>

<style scoped>

@reference "tailwindcss";

#room-status {
    @apply w-[60vw] mt-3  gap-2 flex flex-wrap  ;
}
.room-card {
    @apply bg-[#f8f8f8] relative rounded-lg shadow-md p-4 w-[20%] h-[8rem] text-[0.87rem] border border-[#333] text-[#333] cursor-pointer transition-all duration-75 hover:scale-105;
}
.room-card p {
    @apply italic;
}
.room-card h3 {
    @apply font-bold;
}
.room-card h4 {
    @apply block absolute top-[80%] left-[72%];
}
</style>