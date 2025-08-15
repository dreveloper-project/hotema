<template>
  <div class="flex min-h-screen bg-gradient-to-br from-[#910a67] to-[#ee4dbb] py-4 items-center justify-center px-4">
    <div class="flex flex-col items-center text-[#f5f5f5] w-full max-w-md font-poppins py-6 px-4">
      
      <h1 class="font-bold text-2xl sm:text-3xl text-center">Selamat Datang!</h1>
      <h2 class="text-lg sm:text-xl mt-1">Rapinha</h2>

      <div class="button-container flex flex-col items-center my-6 gap-4 w-full">
        <button>
            <span><IconMaterialSymbolsCleaningServicesSharp class="" /></span>Pekerjaan Hari Ini</button>
            <button><span><IconMaterialSymbolsBookmarkCheckRounded  /></span>Absensi</button>
            <button><span><IconMaterialSymbolsSettingsAccountBox  />
    </span>Pengaturan</button>
        <button class="mt-6"> <span><IconMaterialSymbolsLogoutRounded  /></span>Logout</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

.button-container button {
  @apply outline-[#fff] outline-2 outline-solid text-[#fff] rounded-lg cursor-pointer py-3 w-[60%] max-w-xs transition duration-200 hover:bg-[#f5f5f5] hover:text-[#333] flex pl-2 items-center gap-2;
}
.button-container button span {
    @apply bg-[#fff] rounded-sm p-1 text-[#910a67];
}
</style>
