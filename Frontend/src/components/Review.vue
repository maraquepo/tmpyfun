<script setup>
import {
  FwbRating,
  FwbTextarea,
  FwbSelect,
  FwbCard,
  FwbButton,
} from "flowbite-vue";
import { ref, onMounted } from "vue";
import { getUsers } from "../../services/apiClient";

const selectedFrom = ref("");
const selectedTo = ref("");
const review = ref("");
const users = ref([]);

onMounted(async () => {
  try {
    const res = await getUsers();
    users.value = res.data.map((user) => ({
      value: user.id,
      name: user.fullname,
    }));
  } catch (err) {
    console.error("Error fetching users data: ", error);
  }
});
</script>

<template>
  <div class="my-20">
    <div
      class="flex flex-col justify-center items-center border rounded-md w-auto h-auto bg-white"
    >
      <div class="flex my-5 mx-5 gap-10">
        <fwb-select
          v-model="selectedFrom"
          :options="users"
          label="Review From"
        />
        <fwb-select v-model="selectedTo" :options="users" label="Review To" />
      </div>
      <div class="py-5 flex gap-10">
        <div>
          <p>Skill Rating</p>
          <fwb-rating :rating="4" label="Skill Rating" />
        </div>
        <div>
          <p>Teamplayer Rating</p>
          <fwb-rating :rating="4" label="Teamplayer Rating" />
        </div>
      </div>
      <div class="py-5 w-full px-5">
        <fwb-textarea
          v-model="message"
          :rows="4"
          label="Add Written Review (optional)"
          placeholder="Write your message..."
        />
        <button
          type="submit"
          class="inline-flex items-center px-5 mt-3 py-2.5 text-sm font-medium text-center text-white bg-green-400 rounded-md"
        >
          Submit
        </button>
      </div>
    </div>
  </div>
</template>
