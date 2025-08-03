<script setup>
import Sidebar from '../components/Sidebar.vue'
import TodayStatistic from '@/components/TodayStatistic.vue';
import Pic from '@/components/Pic.vue';
import NotifCard from '@/components/NotifCard.vue';

import { ref } from 'vue';


</script>

<template>
  <Sidebar />
  <main class="bg-[#f4f4f6] w-[79vw]  relative pl-[2rem] ml-[20.145vw] py-[calc(1.43*3rem)] min-h-screen h-auto " >
   
    <TodayStatistic  :today-statistic-value="{ occupancy: 15, dirtyRoom: 8 }" />
    <Pic />
  </main>
     
</template>
