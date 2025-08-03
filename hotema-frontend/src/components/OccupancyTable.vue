<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const occupancyWrap = {
  requestedDate: ['19 Juli', '20 Juli', '21 Juli', '22 Juli', '23 Juli'],
  requestedRoom: {
    101: { '19 Juli': '', '20 Juli': '', '21 Juli': 'IN', '22 Juli': 'IN', '23 Juli': 'OUT' },
    102: { '19 Juli': 'IN', '20 Juli': 'OUT', '21 Juli': '', '22 Juli': '', '23 Juli': '' },
    103: { '19 Juli': '', '20 Juli': '', '21 Juli': 'IN', '22 Juli': 'IN', '23 Juli': 'OUT' },
    105: { '19 Juli': '', '20 Juli': '', '21 Juli': 'IN', '22 Juli': 'IN', '23 Juli': 'IN' },
    106: { '19 Juli': 'OUT', '20 Juli': '', '21 Juli': '', '22 Juli': '', '23 Juli': '' },
    108: { '19 Juli': 'OUT', '20 Juli': '', '21 Juli': 'IN', '22 Juli': 'IN', '23 Juli': 'IN' },
  }
};

function readRequestedDate() {
  return [''].concat(occupancyWrap.requestedDate);
}

function readRequestedRoom() {
  return occupancyWrap.requestedRoom;
}

const activeCell = ref({ row: null, col: null });
const tableContainer = ref(null);

function toggleDropdown(row, col) {
  if (activeCell.value.row === row && activeCell.value.col === col) {
    activeCell.value = { row: null, col: null };
  } else {
    activeCell.value = { row, col };
  }
}

function editAction() {
  alert(`Edit: Room ${activeCell.value.row}, Date ${activeCell.value.col}`);
  activeCell.value = { row: null, col: null };
}

function deleteAction() {
  alert(`Delete: Room ${activeCell.value.row}, Date ${activeCell.value.col}`);
  activeCell.value = { row: null, col: null };
}

// Hide dropdown on click outside
function handleClickOutside(event) {
  if (tableContainer.value && !tableContainer.value.contains(event.target)) {
    activeCell.value = { row: null, col: null };
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div ref="tableContainer" class="">
    <table class="shadow-md font-poppins  text-center border border-gray-600 border-collapse w-[60%] rounded-md">
      <thead>
        <tr>
          <th class="border border-solid border-red-500" v-for="(date, index) in readRequestedDate()" :key="index">
            {{ date }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in Object.keys(readRequestedRoom())" :key="r">
          <td>{{ r }}</td>
          <td
            v-for="(i, value) in readRequestedRoom()[r]"
            :key="value"
            class="relative cursor-pointer"
            @click.stop="toggleDropdown(r, value)"
          >
            <span v-if="i === 'IN'" class="text-[#29ffad]">{{ i }}</span>
            <span v-else-if="i === 'OUT'" class="text-[#ff3737]">{{ i }}</span>
            <span v-else>{{ i }}</span>

            <!-- Dropdown muncul tepat di bawah sel -->
            <div
              v-if="activeCell.row === r && activeCell.col === value"
              class="absolute left-0 top-full mt-1 z-10 bg-white border p-2 border-gray-400 rounded-md shadow-md w-[100px]"
            >
              <button class="w-full text-left px-2 py-1 hover:bg-gray-100 cursor-pointer" @click="editAction">Edit</button>
              <button class="w-full text-left px-2 py-1 hover:bg-gray-100 cursor-pointer" @click="deleteAction">Hapus</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex justify-between w-[60%] px-2 my-2 font-poppins">
      <button class="button-control">
        <IconMaterialSymbolsLightSkipPreviousRounded class="text-[1rem]" />
        Sebelumnya
      </button>
      <button class="button-control">
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
  border-radius: 8px;
  @apply px-5 py-3;
}
</style>
