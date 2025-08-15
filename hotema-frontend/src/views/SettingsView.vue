<script setup>
import { ref, onMounted } from "vue";
import { storeToRefs } from "pinia";
import DatePicker from "primevue/datepicker";
import Sidebar from "@/components/Sidebar.vue";
import { useShiftSettings } from "@/stores/shiftSettings";

const open = ref(false);
const shiftStore = useShiftSettings();
const { shifts, loading, error } = storeToRefs(shiftStore);

// Fetch data saat komponen mount
onMounted(() => {
  shiftStore.fetchShifts();
});

const saveShift = async (shift) => {
  if (loading.value) return; // cegah spam klik
  await shiftStore.updateShift(shift);
  console.log("Shift berhasil diupdate:", shift);
};
</script>

<template>
  <Sidebar />
  <main
    class="bg-[#f4f4f6] min-w-[calc(21.145vw-100vw)] pl-[2rem] ml-[20.145vw] py-[calc(1.43*1.6rem)] min-h-screen h-auto relative font-poppins text-sm"
  >
    <div class="bg-white rounded-lg w-[70%] mt-[3rem]">
      <!-- Header Accordion -->
      <h2>
        <button
          type="button"
          class="flex items-center justify-between w-full p-5 font-medium text-gray-700 rounded-t-xl transition"
          @click="open = !open"
        >
          <span>Jadwal Shift</span>
          <svg
            class="w-3 h-3 shrink-0 transition-transform duration-200"
            :class="{ 'rotate-180': open }"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 10 6"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5 5 1 1 5"
            />
          </svg>
        </button>
      </h2>

      <!-- Body Accordion -->
      <div v-show="open" class="p-5 space-y-6">
        <!-- Loading/Error -->
        <div v-if="loading">Memuat shift...</div>
        <div v-else-if="error" class="text-red-500">{{ error }}</div>

        <!-- List Shifts -->
        <div
          v-for="(shift, index) in shifts"
          :key="shift.id || index"
          class="flex items-center gap-4"
        >
          <span class="w-20 font-semibold text-gray-700">
            {{ shift.name }}
          </span>

          <!-- Jam Mulai -->
          <DatePicker
            v-model="shift.start"
            timeOnly
            hourFormat="24"
            showSeconds
            class="w-32"
          />

          <span class="text-gray-500">-</span>

          <!-- Jam Selesai -->
          <DatePicker
            v-model="shift.stop"
            timeOnly
            hourFormat="24"
            showSeconds
            class="w-32"
          />

          <!-- Tombol Simpan -->
          <button
            class="ml-4 px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-xs"
            :disabled="loading"
            @click="saveShift(shift)"
          >
            {{ loading ? 'Menyimpan...' : 'Simpan' }}
          </button>
        </div>
      </div>
    </div>
  </main>
</template>
