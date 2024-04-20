<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getUserStats } from "../../services/apiClient";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, BarElement, CategoryScale, LinearScale);

const statsData = ref([]);
const chartData = ref({
  labels: [],
  datasets: [
    { label: "Sign ups", backgroundColor: "rgb(52 211 153)", data: [] },
  ],
});
const loaded = ref(false);

const fetchStats = async () => {
  try {
    const response = await getUserStats();
    statsData.value = response.data;

    const { month_year, total } = splitData(statsData.value);
    chartData.value = {
      labels: month_year,
      datasets: [
        {
          ...chartData.value.datasets[0], // Spread the existing dataset properties
          data: total, // Update the data property with the new total
        },
      ],
    };
    loaded.value = true;
    console.log(chartData.value);
  } catch (err) {
    console.error("Error fetching stats", err);
  }
};

const splitData = (data) => {
  const monthYearArray: string[] = [];
  const totalArray: number[] = [];
  data.forEach((item) => {
    const monthYear = new Date(item.month_year).toLocaleString("en-us", {
      month: "short",
      year: "numeric",
    });
    monthYearArray.push(monthYear);
    totalArray.push(item.total_accounts_created);
  });

  return { month_year: monthYearArray, total: totalArray };
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
};

onMounted(fetchStats);
</script>

<template>
  <div
    class="flex justify-center items-center flex-col text-green-400 p-5 font-bold"
  >
    <div class="pb-1">Current Users</div>
    <Bar v-if="loaded" :options="chartOptions" :data="chartData" />
  </div>
</template>
