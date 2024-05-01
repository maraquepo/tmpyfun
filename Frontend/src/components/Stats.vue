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

    const { month_year, verified, unverified } = splitData(statsData.value);
    chartData.value = {
      labels: month_year,
      datasets: [
        {
          ...chartData.value.datasets[0], // Spread the existing dataset properties
          label: "Verified",
          data: verified, // Update the data property with the new total
        },
        {
          ...chartData.value.datasets[0], // Spread the existing dataset properties
          label: "Unverified",
          backgroundColor: "rgb(152, 255, 152)",
          data: unverified, // Update the data property with the new total
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
  const verifiedArray: number[] = [];
  const unverifiedArray: number[] = [];

  data.forEach((item) => {
    const currentMonthYear = new Date(item.month_year);
    const nextMonthYear = new Date(
      currentMonthYear.getFullYear(),
      currentMonthYear.getMonth() + 1
    );
    const monthYear = nextMonthYear.toLocaleString("en-us", {
      month: "short",
      year: "numeric",
    });
    monthYearArray.push(monthYear);
    console.log(monthYearArray);
    verifiedArray.push(item.verified_accounts);
    unverifiedArray.push(item.unverified_accounts);
  });

  return {
    month_year: monthYearArray,
    verified: verifiedArray,
    unverified: unverifiedArray,
  };
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  scales: {
    x: {
      stacked: true,
    },
    y: {
      stacked: true,
    },
  },
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
