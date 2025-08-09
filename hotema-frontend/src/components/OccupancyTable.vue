<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useOccupancyStore } from "@/stores/occupancy";
import { storeToRefs } from "pinia";
import ProgressSpinner from "primevue/progressspinner";
import PopUp from "./PopUp.vue";
// Store Pinia
const store = useOccupancyStore();
const { headers, rows, loading, error } = storeToRefs(store);

const activeCell = ref({ row: null, col: null });
const tableContainer = ref(null);
const showPopup = ref(false);
const popupMessage = ref("");
const popupType = ref("success");

// Navigasi tanggal
const currentStartDate = ref(new Date());
const rangeDays = 5;

// Format tanggal untuk request ke server: YYYY-MM-DD
function formatForAPI(date) {
  return date.toISOString().split("T")[0]; // e.g. "2025-08-07"
}

// Format tanggal untuk ditampilkan di header: "03 Agustus"
function formatForDisplay(date) {
  return date.toLocaleDateString("id-ID", {
    day: "2-digit",
    month: "long",
  });
}

// Ambil array 5 hari dari start date
function getDateRange(startDate) {
  const displayDates = [];
  let start = new Date(startDate);
  for (let i = 0; i < rangeDays; i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);
    displayDates.push({
      raw: formatForAPI(date),
      label: formatForDisplay(date),
    });
  }
  return displayDates;
}

// Fetch data
function loadData() {
  const range = getDateRange(currentStartDate.value);
  const start = range[0].raw;
  const end = range[range.length - 1].raw;
  store.fetchOccupancy(start, end);
}

// Navigasi tombol
function goPrevious() {
  currentStartDate.value.setDate(currentStartDate.value.getDate() - rangeDays);
  loadData();
}

function goNext() {
  currentStartDate.value.setDate(currentStartDate.value.getDate() + rangeDays);
  loadData();
}

// Dropdown cell
function toggleDropdown(row, col) {
  if (activeCell.value.row === row && activeCell.value.col === col) {
    activeCell.value = { row: null, col: null };
  } else {
    activeCell.value = { row, col };
  }
}

async function deleteAction(roomName, date) {
  try {
    await store.deleteOccupancy(roomName, date);

    // Jika sukses
    popupMessage.value = "Data occupancy berhasil dihapus!";
    popupType.value = "success";
    showPopup.value = true;

  } catch (error) {
    // Jika gagal
    popupMessage.value =
      "Gagal menghapus data: " + (error.response?.data?.error || error.message);
    popupType.value = "error";
    showPopup.value = true;
  } finally {
    activeCell.value = { row: null, col: null };

    // Refresh data tabel
    loadData();
  }
}

function closePopup() {
  showPopup.value = false;
}

function handleClickOutside(event) {
  if (tableContainer.value && !tableContainer.value.contains(event.target)) {
    activeCell.value = { row: null, col: null };
  }
}

onMounted(() => {
  window.addEventListener("click", handleClickOutside);
  loadData();
});

onBeforeUnmount(() => {
  window.removeEventListener("click", handleClickOutside);
});
</script>

<template>
  <div
    ref="tableContainer"
    class="bg-[#fff] rounded-lg shadow-md py-5 px-5 w-[68vw] flex justify-center flex-col"
  >
    <div v-if="loading" class="flex justify-center"><ProgressSpinner /></div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <PopUp v-if="showPopup" @close="closePopup">
  <div :class="popupType === 'success' ? 'text-green-600' : 'text-red-600'">
    {{ popupMessage }}
  </div>
</PopUp>

    <table
      v-else
      class="shadow-md font-poppins bg-white rounded-lg text-center border border-gray-600 border-collapse"
    >
      <thead>
        <tr>
          <th class="bg-[#333] text-white">Kamar</th>
          <th
            class="bg-[#333] text-white"
            v-for="(date, index) in headers"
            :key="index"
          >
            {{ date }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in rows" :key="row.id">
          <td>{{ row.id }}</td>
          <td
            v-for="(day, colIndex) in row.days"
            :key="colIndex"
            class="relative cursor-pointer"
            @click.stop="toggleDropdown(row.id, headers[colIndex])"
          >
            <span v-if="day.status === 'IN'" class="text-[#29ffad]">{{
              day.status
            }}</span>
            <span v-else-if="day.status === 'OUT'" class="text-[#ff3737]">{{
              day.status
            }}</span>
            <span v-else>{{ day.status }}</span>

            <div
              v-if="
                activeCell.row === row.id &&
                activeCell.col === headers[colIndex]
              "
              class="absolute left-0 top-full mt-1 z-10 bg-white border p-2 border-gray-400 shadow-md w-[100px]"
            >
              <button
                class="w-full text-left px-2 py-1 hover:bg-gray-100 cursor-pointer"
                @click="deleteAction(row.id, day.date)"
              >
                Hapus
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex justify-between px-2 my-2 font-poppins">
      <button class="button-control" @click="goPrevious">
        <IconMaterialSymbolsLightSkipPreviousRounded class="text-[1rem]" />
        Sebelumnya
      </button>
      <button class="button-control" @click="goNext">
        Berikutnya
        <IconMaterialSymbolsLightSkipNextRounded />
      </button>
    </div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

.button-control {
  @apply bg-[#246aec] text-white py-2 px-4 justify-around rounded-md shadow-lg text-[0.85rem] flex items-center cursor-pointer hover:scale-105;
}

td,
th {
  border: 1.5px groove #949494;
  @apply px-5 py-3;
}
</style>
