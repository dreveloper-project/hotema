import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// PrimeVue
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'

// ✅ Impor komponen yang dibutuhkan
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'
import ToastService from 'primevue/toastservice'
import Toast from 'primevue/toast'


const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
})

app.use(ToastService)
app.component('Toast', Toast)

// ✅ Daftarkan komponen PrimeVue secara global
app.component('Calendar', Calendar)
app.component('Dropdown', Dropdown)

app.mount('#app')
