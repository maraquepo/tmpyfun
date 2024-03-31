<script setup lang="ts">
defineProps<{
  msg: string;
}>();

import PeopleTable from "./UsersTable.vue";
</script>

<template>
  <div class="py-3 px-5">
    <h1 class="text-green-400">{{ msg }}</h1>
  </div>
  <div class="min-h-screen">
    <PeopleTable />
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
