
<script setup>

import { ref } from 'vue';

const notifVisibility = ref(true)

const props = defineProps({
  notifType: String,
  notifMessage: String
})
</script>


<template>

    <div class="notif-card font-poppins transition-all duration-150" :class="props.notifType" v-if="notifVisibility" >
    <div class="flex gap-3 self-start">
        <div class="flex items-center justify-center  ">
            <span class=" bg-neutral-100 rounded-lg shadow-sm">

                <IconIcOutlineInfo v-if="props.notifType == 'info'" class="notif-icon" />
                <IconIcBaselineLibraryAddCheck v-if="props.notifType == 'success'" class="notif-icon" />
                <IconIcRoundWarning v-if="props.notifType == 'warning'" class="notif-icon" />
                <IconIcBaselineBugReport v-if="props.notifType == 'error'" class="notif-icon" />

            </span>
        </div>
        <div class="flex flex-col gap-1">
            <h3>{{ props.notifType.toLocaleUpperCase() }}</h3>
            <p>{{ props.notifMessage }}</p>
        </div>
    </div>
         <div class="flex items-center justify-center ">
            <IconIcSharpClose @click="notifVisibility = false" class=" text-2xl hover:scale-150 cursor-pointer transition-all duration-150 " />
         </div>
    </div>

</template>


<style scoped>
@reference "tailwindcss";

.notif-card {
    @apply hover:scale-105 transition-all duration-75  p-2 py-2 w-[42vw] border border-solid flex justify-between min-h-[4vh] text-white rounded-lg shadow-md my-5 gap-3;
}
.notif-icon {
    @apply text-[1.4rem] p-1;
}
.notif-card h3 {
    @apply text-[0.97rem] font-bold ;
}

.notif-card p {
    @apply text-[0.69rem]  ;
}

.error {
    @apply text-[#ff3300] border-[#ff3300] ;
}

.warning {
    @apply text-[#1d1c1c]  border-[#ffd519]   bg-[#ffd519];
}


.success {
    @apply bg-gradient-to-r from-[#99ffe5] border-[#99ffe5] to-[#d6faf4] text-[#027558];
}



.info {
    @apply bg-gradient-to-r from-[#d1f6f8] to-[#ecfffd] text-[#32aec4];
}

</style>