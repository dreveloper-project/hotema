<script setup>
import Sidebar from '../components/Sidebar.vue'
import OccupancyTable from '@/components/OccupancyTable.vue'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'
import { useOccupancyStore } from '@/stores/occupancy'
import AddNewOccupancy from '@/components/Occupancy/AddNewOccupancy.vue'

const occupancyStore = useOccupancyStore()

// Definisikan tanggalnya di komponen
const startDate = ref('2025-08-04')
const endDate = ref('2025-08-09')

// Panggil saat tombol diklik atau saat mounted
const loadOccupancy = () => {
  occupancyStore.fetchOccupancy(startDate.value, endDate.value)
}

onMounted(loadOccupancy)






// Submit

</script>

<template>
  <Sidebar />

  <main class="bg-[#f4f4f6] min-w-[calc(21.145vw-100vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto relative font-poppins">
    <!-- Tombol + Form -->
   
    <AddNewOccupancy />
    <!-- Komponen Tabel -->
    <OccupancyTable />



    <!--  -->

    <!--  -->

 

    <!--  -->

    <!--  -->
  </main>
</template>

<style scoped>

</style>

