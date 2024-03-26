<script setup lang="ts">
import { defineProps, ref } from "vue";
import { editUser } from "../../services/apiClient.ts";

interface User {
  [key: string]: string | number;
}

// Define a type alias for Record
type RowData = Record<string, string | number | boolean | null>;

const props = defineProps({
  id: String,
  rowData: Object as () => RowData,
});

const isModalOpen = ref(false);
let userId: string | null = null;
const formValues = ref<User>({});

const openModal = (id: string) => {
  isModalOpen.value = true;
  userId = id;
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
    if (!userId) return;

    console.log("Submitting form with userId:", userId);
    console.log("Form values:", formValues.value);

    // Call editUser function directly
    await editUser(userId, formValues.value);

    console.log("Form submitted successfully.");
    closeModal();
  } catch (error) {
    console.error("Error submitting form:", error);
  }
};
</script>

Got it! We can achieve a two-column layout using flexbox. Here's the updated
code to display the form inputs in two columns: html Copy code
<template>
  <div>
    <button @click="handleClick">Edit</button>
    <div v-if="isModalOpen" class="modal-wrapper">
      <div class="modal-content">
        <h2>Edit {{ props.rowData.fullname }}</h2>
        <div
          class="form-group"
          v-for="(value, key) in props.rowData"
          :key="key"
        >
          <div class="input-group">
            <label class="label" :for="key">{{ key }}:</label>
            <input
              v-model="formValues[key]"
              :id="key"
              :name="key"
              class="input"
            />
          </div>
        </div>
        <div class="buttons">
          <button @click="submitForm" class="btn-update">Update</button>
          <button @click="closeModal" class="btn-cancel">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: darkgrey;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
}

.form-group {
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  align-items: center;
}

.label {
  flex: 1;
  font-weight: bold;
  margin-right: 10px;
}

.input {
  flex: 2;
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.buttons {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.btn-update,
.btn-cancel {
  padding: 8px 16px;
  margin-left: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-update {
  background-color: #4caf50;
  color: white;
}

.btn-cancel {
  background-color: #f44336;
  color: white;
}
</style>
