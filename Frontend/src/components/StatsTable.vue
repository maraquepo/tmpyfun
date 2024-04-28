<script setup lang="ts">
import { defineProps, ref, onMounted } from "vue";
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
  data: { type: Object },
});

const chartData = ref(null);

onMounted(() => {
  const labels = props.data?.month_year || [];
  const data = props.data?.total || [];

  chartData.value = {
    labels: labels,
    datasets: [
      { data: data, backgroundColor: "rgb(52 211 153)", label: "Sign ups" },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
};
</script>
<template>
  <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>
