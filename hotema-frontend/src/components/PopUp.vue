<template>
  <div class="fixed font-poppins inset-0 z-50 flex items-center justify-center bg-black/60">
    <div class="bg-white rounded-2xl shadow-lg max-w-md w-full p-6 relative">
      <!-- Tombol X di pojok kanan atas -->
      <button
        @click="close"
        class="absolute top-3 right-3 text-gray-500 hover:text-black text-xl"
      >
        &times;
      </button>

      <!-- Isi popup -->
      <div class="mb-4">
        <slot />
      </div>

      <!-- Tombol tutup di bawah -->
      <div class="flex justify-end">
        <button
          @click="close"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Tutup
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close'])
function close() {
  emit('close')
}
</script>
