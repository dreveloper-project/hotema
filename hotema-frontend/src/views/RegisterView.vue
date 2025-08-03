<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#910a67] to-[#ee4dbb] p-4"
  >
    <div
      class="w-full max-w-2xl bg-white rounded-xl shadow-xl p-6 sm:p-8 font-poppins"
    >
      <h2 class="text-2xl font-bold text-[#910a67] mb-6 border-b pb-2">
        Formulir Pendaftaran
      </h2>

      <form
        @submit.prevent="handleSubmit"
        class="grid grid-cols-1 md:grid-cols-2 gap-4"
      >
        <!-- Nama Lengkap -->
        <div>
          <label class="block text-sm font-medium text-[#333] mb-1">Nama Lengkap</label>
          <input
            type="text"
            placeholder="Masukkan nama lengkap"
            v-model="form.fullname"
            class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#910a67]"
          />
        </div>

        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-[#333] mb-1">Username</label>
          <input
            type="text"
            placeholder="Masukkan username"
            v-model="form.username"
            class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#910a67]"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-[#333] mb-1">Email</label>
          <input
            type="email"
            placeholder="Masukkan email"
            v-model="form.email"
            class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#910a67]"
          />
        </div>

        <!-- Password dan Konfirmasi Password -->
        <div class="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-[#333] mb-1">Kata Sandi</label>
            <div class="relative">
              <input
                :type="showPassword ? 'text' : 'password'"
                placeholder="Masukkan password"
                v-model="form.password"
                class="w-full border border-gray-300 rounded-md px-4 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-[#910a67]"
              />
              <button
                type="button"
                class="absolute right-3 top-2 text-[#910a67]"
                @click="showPassword = !showPassword"
              >
                <component
                  :is="showPassword ? IconMaterialSymbolsLightVisibilityOffRounded : IconMaterialSymbolsLightVisibilityRounded"
                  class="w-5 h-5"
                />
              </button>
            </div>
            <p
              v-if="form.password && form.password.length < 8"
              class="text-sm text-red-500 mt-1"
            >
              Kata sandi minimal 8 karakter!
            </p>
          </div>

          <!-- Konfirmasi Password -->
          <div>
            <label class="block text-sm font-medium text-[#333] mb-1">Konfirmasi Kata Sandi</label>
            <div class="relative">
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Ulangi kata sandi"
                v-model="form.confirmPassword"
                class="w-full border border-gray-300 rounded-md px-4 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-[#910a67]"
              />
              <button
                type="button"
                class="absolute right-3 top-2 text-[#910a67]"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <component
                  :is="showConfirmPassword ? IconMaterialSymbolsLightVisibilityOffRounded : IconMaterialSymbolsLightVisibilityRounded"
                  class="w-5 h-5"
                />
              </button>
            </div>
            <p
              v-if="form.confirmPassword && form.confirmPassword !== form.password"
              class="text-sm text-red-500 mt-1"
            >
              Kata sandi tidak cocok!
            </p>
          </div>
        </div>

        <!-- Foto Profil -->
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-[#333] mb-1">Foto Profil</label>
          <input
            type="file"
            @change="handleImageUpload"
            class="w-full text-sm text-[#333] file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-[#f4f4f6] file:text-[#910a67] hover:file:bg-[#e9e9ec]"
          />
          <div v-if="previewImage" class="mt-4">
            <p class="text-sm text-[#333] mb-1">Pratinjau:</p>
            <img
              :src="previewImage"
              alt="Preview"
              class="h-24 w-24 object-cover rounded-full border"
            />
          </div>
        </div>

        <!-- Tombol Submit -->
        <div class="md:col-span-2">
          <button
            type="submit"
            class="w-full py-2 text-white font-semibold rounded-md bg-gradient-to-r from-[#910a67] to-[#68319c] hover:opacity-90 transition"
          >
            Daftar Sekarang
          </button>
        </div>
      </form>
    </div>
  </div>

  <PopUp v-if="showPopUp">
    {{ errorMessages }}
  </PopUp>
</template>

<script setup>
import IconMaterialSymbolsLightVisibilityRounded from "~icons/material-symbols-light/visibility-rounded";
import IconMaterialSymbolsLightVisibilityOffRounded from "~icons/material-symbols-light/visibility-off-rounded";
import { ref, watch } from "vue";
import { useAuthStore } from "@/stores/authStoreB";
import PopUp from "@/components/PopUp.vue";
import { useRouter } from "vue-router";

const showPopUp = ref(false);
const errorMessages = ref([]);

const authStore = useAuthStore();

const showPassword = ref(false); // untuk password
const showConfirmPassword = ref(false); // untuk konfirmasi password
const previewImage = ref(null);

const form = ref({
  fullname: "",
  username: "",
  email: "",
  phone: "",
  password: "",
  confirmPassword: "",
  profilePicture: null,
});

watch(
  () => authStore.error,
  (val) => {
    if (val) {
      showPopUp.value = true;
      if (typeof val === "string") {
        errorMessages.value = [val];
      } else if (val.detail) {
        errorMessages.value = [val.detail];
      } else {
        errorMessages.value = Object.entries(val).map(
          ([key, val]) => `${key}: ${val}`
        );
      }
    }
  }
);

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (file) {
    form.value.profilePicture = file;
    previewImage.value = URL.createObjectURL(file);
  }
}

const router = useRouter();

async function handleSubmit(e) {
  e.preventDefault();

  if (form.value.password !== form.value.confirmPassword) {
    alert("Password tidak cocok!");
    return;
  }

  if (form.value.profilePicture) {
    const allowedTypes = ["image/jpeg", "image/png", "image/jpg"];
    if (!allowedTypes.includes(form.value.profilePicture.type)) {
      alert("Format gambar tidak valid.");
      return;
    }

    const maxSize = 2 * 1024 * 1024;
    if (form.value.profilePicture.size > maxSize) {
      alert("Ukuran gambar tidak boleh lebih dari 2MB.");
      return;
    }
  }

  const formData = new FormData();
  formData.append("fullname", form.value.fullname);
  formData.append("username", form.value.username);
  formData.append("email", form.value.email);
  formData.append("password", form.value.password);
  formData.append("password2", form.value.confirmPassword);

  if (form.value.profilePicture) {
    formData.append("pictures", form.value.profilePicture);
  }

  await authStore.register(formData);

  if (!authStore.error) {
    router.push({
      name: "login",
      query: { message: "Registrasi berhasil! Silakan login." },
    });
  } else {
    const errorMsg = authStore.error?.detail || "Registrasi gagal.";
    alert(errorMsg);
  }
}
</script>
