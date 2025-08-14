<script setup>
import { computed } from 'vue'
import ProgressSpinner from 'primevue/progressspinner';
const props = defineProps({
  records: {
    type: Array,
    required: true,
    default: () => []
  }
})


const rooms = computed(() =>
  props.records.map(record => ({
    room_name: record.room_name,
    cleanlines_status: record.cleanliness_status,
    occuppation_status: record.guest_status ?? 'Vacant',
  }))
)
</script>

<template>
  <div id="room-status" class="font-poppins " >
    <!-- Loading -->
    <template v-if="records === null">
      <ProgressSpinner />
    </template>

    <!-- Data -->
    <template v-else>
      <div v-for="room in rooms" :key="room.room_name" class="room-card">
        <h3>{{ room.room_name }}</h3>
        <p>{{ room.cleanlines_status }}</p>
        <h4>{{ room.occuppation_status }}</h4>
      </div>
    </template>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

#room-status {
  @apply w-[70vw] mt-3 gap-1 flex flex-wrap px-4 py-4 bg-[#ffffff] rounded-lg shadow-md justify-around;
}

.room-card {
  @apply bg-[#910a67]  relative rounded-lg shadow-md p-4 my-3 w-[24%] h-[8rem] text-[0.87rem] border border-[#fff] text-[#fff] cursor-pointer transition-all duration-75 hover:scale-105;
}

.room-card p {
  @apply italic;
}

.room-card h3 {
  @apply font-bold;
}

.room-card h4 {
  @apply block absolute top-[75%] left-[43%] text-[0.73rem] text-right;
}

</style>