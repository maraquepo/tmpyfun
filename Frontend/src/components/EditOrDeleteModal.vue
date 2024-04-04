import { defineProps } from 'vue';
<script setup lang="ts">
import { ref, defineProps } from "vue";

const isModalOpen = ref(false);

const openModal = () => {
  isModalOpen.value = true;
};

const handleClick = () => {
  openModal();
};

const closeModal = () => {
  isModalOpen.value = false;
};
</script>

<template>
  <div>
    <button
      @click="handleClick"
      class="px-4 py-2 border-green-400 border text-green-400 rounded-md"
    >
      Edit User
    </button>
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="modal-content bg-zinc-900 rounded-lg shadow-lg p-6 w-100">
        <h2 class="text-xl font-bold mb-4 text-green-400">Troll</h2>
        <div class="buttons flex justify-end">
          <button
            class="btn-update px-4 py-2 text-green-400 border border-green-400 rounded-md mr-4"
          >
            Delete
          </button>
          <button
            class="btn-update px-4 py-2 text-green-400 border border-green-400 rounded-md mr-4"
          >
            Change Picture
          </button>
          <button
            @click="closeModal"
            class="btn-cancel px-4 py-2 text-red-500 border border-red-500 rounded-md"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
