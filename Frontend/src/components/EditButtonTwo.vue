<script setup lang="ts">
import { defineProps, ref } from "vue";
import { editTeam } from "../../services/apiClient.ts";

interface Team {
  [key: string]: string | number;
}

// Define a type alias for Record
type RowData = Record<string, string | number | boolean | null>;

const props = defineProps({
  id: String,
  rowData: Object as () => RowData,
  fetchItems: Function,
});

const isModalOpen = ref(false);
let teamId: string | null = null;
const formValues = ref<Team>({});

const openModal = (id: string) => {
  isModalOpen.value = true;
  teamId = id;
  // Reset formValues when opening modal
  formValues.value = { ...props.rowData };
};

const handleClick = () => {
  openModal(props.id);
};

const closeModal = () => {
  isModalOpen.value = false;
  // Reset formValues when closing modal
  formValues.value = {};
};

const submitForm = async () => {
  try {
    if (!teamId) return;

    console.log("Submitting form with teamId:", teamId);
    console.log("Form values:", formValues.value);

    // Call editUser function directly
    await editTeam(teamId, formValues.value);

    console.log("Form submitted successfully.");
    closeModal();
    await props.fetchItems();
  } catch (error) {
    console.error("Error submitting form:", error);
  }
};
</script>

<template>
  <div>
    <button
      @click="handleClick"
      class="px-4 py-2 border-green-400 border text-green-400 rounded-md"
    >
      Edit
    </button>
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="modal-content bg-white rounded-lg shadow-lg p-6 w-96">
        <h2 class="text-xl font-bold mb-4">Edit {{ props.rowData.title }}</h2>
        <div
          class="form-group"
          v-for="(value, key) in props.rowData"
          :key="key"
        >
          <div class="input-group flex mb-4">
            <label class="label flex-none w-28">{{ key }}:</label>
            <input
              v-model="formValues[key]"
              :id="key"
              :name="key"
              class="input flex-auto border rounded-md p-2"
            />
          </div>
        </div>
        <div class="buttons flex justify-end">
          <button
            @click="submitForm"
            class="btn-update px-4 py-2 bg-green-500 text-white rounded-md mr-4"
          >
            Update
          </button>
          <button
            @click="closeModal"
            class="btn-cancel px-4 py-2 bg-red-500 text-white rounded-md"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
