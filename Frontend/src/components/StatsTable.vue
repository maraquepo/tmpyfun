<template>
  <div class="container">
    <Bar v-if="loaded" :data="chartData" />
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

const props = defineProps({
  data: { type: Object, required: true },
});

const loaded = ref(false);
const chartData = ref(null);

const fetchData = async () => {
  try {
    console.log(props.data);
    chartData.value = props.data.userlist;
    loaded.value = true;
  } catch (error) {
    console.error(error);
  }
};

fetchData();
</script>
