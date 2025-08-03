<template>
  <div class="fixed font-poppins inset-0 z-50 flex items-center justify-center bg-black/60">
    <div class="bg-white rounded-2xl shadow-lg max-w-md w-full p-6 relative">
      <button @click="close" class="absolute top-3 right-3 text-gray-500 hover:text-black text-xl">&times;</button>
      <slot />
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close'])
function close() {
  emit('close')
}
</script>