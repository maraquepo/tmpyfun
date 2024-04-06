import { defineProps } from 'vue';
<script setup lang="ts">
import { ref, defineProps, watchEffect } from "vue";
import { updateTeamsPictureURL } from "../../services/apiClient";

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

const updatePictureURLsOfSelectedTeams = async () => {
  const teamIDs = selectedRows.value.map((team) => team.original.id);
  try {
    await updateTeamsPictureURL(teamIDs, newPictureURL.value);
    closeModal();
    await props.fetchTeams();
  } catch (error) {
    console.error("Error updating picture URLs:", error);
  }
};

const props = defineProps({
  teams: Array,
  fetchTeams: Function,
});

const grabTeamName = (teams) => {
  const teamName = teams.map((team) => team.original.title);
  console.log("Creator User IDs:", teamName);
};

watchEffect(() => {
  console.log("User object updated:", props.teams);
  selectedRows.value = Array.isArray(props.teams) ? props.teams : [props.teams];
  console.log("Selected rows:", selectedRows.value);
  grabTeamName(selectedRows.value);
});
</script>

<template>
  <div>
    <button
      @click="handleClick"
      class="px-4 py-2 border-green-400 border text-green-400 rounded-md"
    >
      Edit {{ selectedRows.length }} Team
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
              v-for="(team, index) in selectedRows"
              :key="index"
              class="text-green-400"
            >
              {{ team.original.title }}
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
            @click="updatePictureURLsOfSelectedTeams"
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
