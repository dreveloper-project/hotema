<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg bg-[#f4f4f6] min-h-screen flex-col items-center justify-between">
    <h1 class="mx-2 my-4 font-poppins text-2xl">Tugas Hari Ini</h1>
    <RouterLink to="/staff/dashboard" v-slot="{ navigate }">
      <button
        @click="navigate"
        class="bg-[#6b61ff] ml-2 py-1 px-2 font-poppins rounded-md text-[#f4f4f6] text-[0.87rem] mb-2 flex items-center cursor-pointer transition-all hover:scale-105"
      >
        Kembali
        <span class="ml-1"><IconIcBaselineKeyboardBackspace class="text-[1rem]" /></span>
      </button>
    </RouterLink>

    <table class="w-full font-poppins text-xs sm:text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase dark:text-gray-400">
        <tr>
          <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Kamar</th>
          <th class="px-4 sm:px-6 py-3">Tanggal</th>
          <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Waktu Mulai</th>
          <th class="px-4 sm:px-6 py-3">Waktu Selesai</th>
          <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">QC Status</th>
          <th class="px-4 sm:px-6 py-3">QC Oleh</th>
          <th class="px-4 sm:px-6 py-3 bg-gray-50 dark:bg-gray-800">Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr class="border-b border-gray-200 dark:border-gray-700">
          <td class="px-4 sm:px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">
            Kamar 101
          </td>
          <td class="px-4 sm:px-6 py-4">18-08-2025</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">08:00</td>
          <td class="px-4 sm:px-6 py-4">09:00</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">Pending</td>
          <td class="px-4 sm:px-6 py-4">-</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">
            <button class="text-blue-600 hover:underline cursor-pointer">Kerjakan</button>
          </td>
        </tr>

        <tr class="border-b border-gray-200 dark:border-gray-700">
          <td class="px-4 sm:px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">
            Kamar 102
          </td>
          <td class="px-4 sm:px-6 py-4">18-08-2025</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">09:15</td>
          <td class="px-4 sm:px-6 py-4">10:00</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">Approved</td>
          <td class="px-4 sm:px-6 py-4">Supervisor A</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">
            <button class="text-blue-600 hover:underline cursor-pointer">Kerjakan</button>
          </td>
        </tr>

        <tr class="border-b border-gray-200 dark:border-gray-700">
          <td class="px-4 sm:px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">
            Kamar 103
          </td>
          <td class="px-4 sm:px-6 py-4">18-08-2025</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">10:10</td>
          <td class="px-4 sm:px-6 py-4">11:00</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">Rejected</td>
          <td class="px-4 sm:px-6 py-4">Supervisor B</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">
            <button class="text-blue-600 hover:underline cursor-pointer">Kerjakan</button>
          </td>
        </tr>

        <tr>
          <td class="px-4 sm:px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50 dark:text-white dark:bg-gray-800">
            Kamar 104
          </td>
          <td class="px-4 sm:px-6 py-4">18-08-2025</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">11:10</td>
          <td class="px-4 sm:px-6 py-4">12:00</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">Pending</td>
          <td class="px-4 sm:px-6 py-4">-</td>
          <td class="px-4 sm:px-6 py-4 bg-gray-50 dark:bg-gray-800">
            <button class="text-blue-600 hover:underline cursor-pointer">Kerjakan</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
