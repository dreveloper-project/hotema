<script setup>
import { reactive } from 'vue'
import { computed } from 'vue'
const pic =  reactive(
   [
  // Morning
  { name: 'Thiago Silva', shift: 'morning', absent: 'no', role: 'staff' },      // Brazil
  { name: 'Mireia Costa', shift: 'morning', absent: 'no', role: 'staff' },      // Catalan
  { name: 'Gabriela Souza', shift: 'morning', absent: 'no', role: 'spv' },      // Brazil

  // Afternoon
  { name: 'João Pereira', shift: 'afternoon', absent: 'no', role: 'staff' },    // Brazil
  { name: 'Arnau Vidal', shift: 'afternoon', absent: 'yes', role: 'staff' },    // Catalan
  { name: 'Laia Rodríguez', shift: 'afternoon', absent: 'no', role: 'spv' },    // Catalan

  // Evening
  { name: 'Lucas Oliveira', shift: 'evening', absent: 'yes', role: 'staff' },   // Brazil
  { name: 'Carla Martí', shift: 'evening', absent: 'no', role: 'staff' },       // Catalan
  { name: 'Fernanda Lima', shift: 'evening', absent: 'no', role: 'spv' }        // Brazil
]

)


const groupedPic = computed(() => {
  const groups = {}
  pic.forEach(person => {
    if (!groups[person.shift]) {
      groups[person.shift] = []
    }
    groups[person.shift].push(person)
  })
  return groups
})
</script>

<template>

<div id="pic-table" class="font-poppins" >
   
    <h2>Yang Bertugas Hari Ini</h2>
    
    <hr class="border-t border-black my-2 w-[35%]">
    
    <table class="table-auto">
        <thead>
            <tr>
                <th >Nama</th>
                <th>Absen</th>
                <th>Jabatan</th>
            </tr>
        </thead>
    </table>
    <h3>Shift Pagi</h3>
    <table class="table-auto">
        <tbody>
            <tr v-for="(person, index) in groupedPic.morning" :key="index" >
                <td>
                    {{ person.name }}
                </td>
                <td>
                   {{ person.absent == 'yes' ? `Sudah ✔` : `Belum ❌ ` }}
                </td>
                <td>
                    {{ person.role }}
                </td>
            </tr>
        </tbody>
    </table>
    <h3>Shift Siang</h3>
    <table class="table-auto">
        <tbody>
            <tr v-for="(person, index) in groupedPic.afternoon" :key="index" >
                <td>
                    {{ person.name }}
                </td>
                <td>
                     {{ person.absent == 'yes' ? `Sudah ✔` : `Belum ❌ ` }}
                </td>
                <td>
                    {{ person.role }}
                </td>
            </tr>
        </tbody>
    </table>
    <h3>Shift Malam</h3>
    <table class="table-auto">
        <tbody>
            <tr v-for="(person, index) in groupedPic.evening" :key="index" >
                <td>
                    {{ person.name }}
                </td>
                <td>
                   {{ person.absent == 'yes' ? `Sudah ✔` : `Belum ❌ ` }}
                </td>
                <td>
                    {{ person.role }}
                </td>
            </tr>
        </tbody>
    </table>
   
</div>


</template>

<style scoped>
@reference "tailwindcss";

#pic-table {
 @apply bg-[#f8f8f8] rounded-lg bg-linear-to-r  rounded-lg shadow-lg w-[35rem] mt-5 
 px-3 py-3.5 text-[#0c0c0c];
}
#pic-table h2 {
    @apply font-medium text-[0.87rem];
}
#pic-table h3 {
    @apply font-bold text-[0.75rem];
}
#pic-table table {
    @apply ml-[4.7rem] divide-y divide-[#0c0c0c];
}
td {
    @apply px-5 py-2 text-[0.85rem];
}
th {
    @apply p-5 text-[0.85rem] italic font-bold;
}
/* rounded-lg  rounded-lg shadow-lg w-[35rem] mt-5   */
</style>
