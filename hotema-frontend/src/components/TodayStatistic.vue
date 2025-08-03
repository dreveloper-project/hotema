<script setup>
const props = defineProps({
  todayStatisticValue: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div id="today-statistic" class="font-poppins flex gap-5">
    <div id="statistic-ocupancy" class="statistic-card">
      <div>
        <h2>Okupansi</h2>
        <h3>
          {{ props.todayStatisticValue.occupancy }}
        </h3>
        <h2>
          Dari 24 Kamar =
          {{ ((props.todayStatisticValue.occupancy / 24) * 100).toFixed(2) }} %
        </h2>
      </div>
      <span>
        <IconIcBaselineLocalHotel />
      </span>
    </div>

    <div id="statistic-dirty-room" class="statistic-card">
      <div>
        <h2>Kotor</h2>
        <h3>
          {{ props.todayStatisticValue.dirtyRoom }}
        </h3>
        <h2>
          Dari 24 Kamar =
          {{ ((props.todayStatisticValue.dirtyRoom / 24) * 100).toFixed(2) }} %
        </h2>
      </div>
      <span>
        <IconIcRoundFmdBad />
      </span>
    </div>

  </div>
</template>

<style scoped>
@reference "tailwindcss";

#statistic-ocupancy {
  @apply bg-[#191919];
}
#statistic-dirty-room {
  @apply bg-[#FFB823];
}
.statistic-card {
  @apply w-[14.77rem]  text-amber-50 rounded-lg   flex;
}
.statistic-card div {
  @apply flex flex-col gap-2.5 py-3 px-3; 
}
.statistic-card span {
    @apply text-[1.43rem] block mt-4;
}

.statistic-card div h2 {
  @apply text-[0.79rem] font-medium;
}
.statistic-card div h3 {
  @apply text-2xl font-bold;
}
</style>
