import { defineProps } from 'vue';
<script setup lang="ts">
import { ref, defineProps, watch } from "vue";
import { deleteUsers } from "../../services/apiClient";

const isModalOpen = ref(false);
const selectedRows = ref([]);

const openModal = () => {
  isModalOpen.value = true;
};

const handleClick = () => {
  openModal();
};

const closeModal = () => {
  isModalOpen.value = false;
};

const deleteMultiUsers = async () => {
  const userIDs = selectedRows.value.map((user) => user.original.id);
  try {
    await deleteUsers(userIDs);
    closeModal();
  } catch (error) {
    console.error("Error deleting users:", error);
  }
};

const props = defineProps({
  user: Object,
});

watch(
  () => props.user,
  (newValue) => {
    console.log("User object updated:", newValue);
    selectedRows.value = newValue;
    grabCreatorUserId(newValue);
  }
);

const grabCreatorUserId = (users) => {
  const creatorIds = users.map((user) => user.original.creator_user_id);
  console.log("Creator User IDs:", creatorIds);
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
        <div v-if="selectedRows.length > 0" class="my-5">
          <ul>
            <li
              v-for="(user, index) in selectedRows"
              :key="index"
              class="text-green-400"
            >
              {{ user.original.fullname }}
            </li>
          </ul>
        </div>
        <div class="input-group flex mb-4">
          <input class="input flex-auto border rounded-md" />
        </div>
        <div class="buttons flex justify-end">
          <button
            class="btn-update px-4 py-2 text-green-400 border border-green-400 rounded-md mr-4"
            @click="deleteMultiUsers"
          >
            Delete {{ selectedRows.length }}
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
