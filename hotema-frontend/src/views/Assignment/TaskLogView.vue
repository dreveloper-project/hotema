<script setup>

</script>

<template>
  <div class="flex pl-5 font-poppins bg-[#f4f4f6] pt-4 justify-between">
      <RouterLink to="/Assignment" v-slot="{ navigate }">
        <button
          @click="navigate"
          class="bg-[#6b61ff] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
        >
          Kembali
          <span class="ml-1"><IconIcBaselineKeyboardBackspace class="text-[1rem]" /></span>
        </button>
      </RouterLink>
      <RouterLink to="/create-assignment" v-slot="{ navigate }">
        <button
          @click="navigate"
          class="bg-[#680e6b] py-2 px-3 rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105 mr-25"
        >
          Tugaskan Seseorang
          <span class="ml-1"><IconIcOutlineAssignment class="text-[1.5rem]" /></span>
        </button>
      </RouterLink>

    </div>
  <div class="min-h-screen flex justify-center bg-[#f4f4f6] px-4 font-poppins">
    <div class="w-full max-w-6xl bg-white rounded-lg shadow">
      <table class="w-full text-sm text-left text-gray-600">
        <thead class="text-xs uppercase text-gray-100 bg-[#680e6b]">
          <tr>
            <th class="px-6 py-3">Kamar</th>
            <th class="px-6 py-3">Tanggal</th>
            <th class="px-6 py-3">Waktu Mulai</th>
            <th class="px-6 py-3">Waktu Selesai</th>
            <th class="px-6 py-3">Dikerjakan Oleh</th>
            <th class="px-6 py-3">Quality Check Oleh</th>
            <th class="px-6 py-3">Status QC</th>
            <th class="px-6 py-3 text-right">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr class="border-b hover:bg-gray-50">
            <td class="px-6 py-3">Kamar 101</td>
            <td class="px-6 py-3">2025-08-17</td>
            <td class="px-6 py-3">08:00</td>
            <td class="px-6 py-3">09:30</td>
            <td class="px-6 py-3">Bastian</td>
            <td class="px-6 py-3">Sarah</td>
            <td class="px-6 py-3 text-green-600 font-medium">Approved</td>
            <td class="px-6 py-3 text-right">
              <button class="text-blue-600 hover:underline">Edit</button>
            </td>
          </tr>
          <tr class="border-b hover:bg-gray-50">
            <td class="px-6 py-3">Kamar 102</td>
            <td class="px-6 py-3">2025-08-17</td>
            <td class="px-6 py-3">10:00</td>
            <td class="px-6 py-3">11:15</td>
            <td class="px-6 py-3">Dina</td>
            <td class="px-6 py-3">Andi</td>
            <td class="px-6 py-3 text-yellow-600 font-medium">Pending</td>
            <td class="px-6 py-3 text-right">
              <button class="text-blue-600 hover:underline">Edit</button>
            </td>
          </tr>
          <tr class="hover:bg-gray-50">
            <td class="px-6 py-3">Kamar 103</td>
            <td class="px-6 py-3">2025-08-17</td>
            <td class="px-6 py-3">13:00</td>
            <td class="px-6 py-3">14:00</td>
            <td class="px-6 py-3">Rudi</td>
            <td class="px-6 py-3">Sarah</td>
            <td class="px-6 py-3 text-red-600 font-medium">Rejected</td>
            <td class="px-6 py-3 text-right">
              <button class="text-blue-600 hover:underline">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";
button {
  @apply cursor-pointer;
}
</style>
