import { defineProps } from 'vue';
<script setup lang="ts">
import { ref, defineProps, watchEffect } from "vue";
import { deleteUsers, updateUsersPictureURL } from "../../services/apiClient";

const isModalOpen = ref(false);
const selectedRows = ref([]);
const newPictureURL = ref("");

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
    await props.fetchPeople();
  } catch (error) {
    console.error("Error deleting users:", error);
  }
};

const updatePictureURLsOfSelectedUsers = async () => {
  const userIDs = selectedRows.value.map((user) => user.original.id);
  try {
    await updateUsersPictureURL(userIDs, newPictureURL.value);
    closeModal();
    await props.fetchPeople();
  } catch (error) {
    console.error("Error updating picture URLs:", error);
  }
};

const props = defineProps({
  user: Array,
  fetchPeople: Function,
});

const grabCreatorUserId = (users) => {
  const creatorIds = users.map((user) => user.original.creator_user_id);
  console.log("Creator User IDs:", creatorIds);
};

watchEffect(() => {
  console.log("User object updated:", props.user);
  selectedRows.value = Array.isArray(props.user) ? props.user : [props.user];
  console.log("Selected rows:", selectedRows.value);
  grabCreatorUserId(selectedRows.value);
});
</script>

<template>
  <div>
    <button
      @click="handleClick"
      class="px-4 py-2 border-green-400 border text-green-400 rounded-md"
    >
      Edit {{ selectedRows.length }} User
    </button>
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div
        class="modal-content bg-zinc-900 rounded-lg shadow-lg p-6 w-100 max-h-80 overflow-y-auto"
      >
        <h2 class="text-xl font-bold mb-4 text-green-400">Troll</h2>
        <div v-if="selectedRows.length !== 0" class="my-5">
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
          <input
            v-model="newPictureURL"
            class="input flex-auto border rounded-md"
            placeholder="New Picture URL"
          />
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
            @click="updatePictureURLsOfSelectedUsers"
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
