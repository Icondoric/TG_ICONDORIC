<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { computed } from 'vue';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chartData = computed(() => ({
  labels: props.data.labels,
  datasets: [
    {
      label: 'Nuevos Usuarios',
      backgroundColor: '#3B82F633', // Blue with opacity
      borderColor: '#3B82F6',
      pointBackgroundColor: '#3B82F6',
      borderWidth: 2,
      fill: true,
      tension: 0.4, // Curva suave
      data: props.data.data
    }
  ]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
        display: false
    }
  },
  scales: {
    y: {
        beginAtZero: true,
        ticks: {
            precision: 0
        }
    }
  }
}
</script>

<template>
  <div class="h-64">
    <Line :data="chartData" :options="options" />
  </div>
</template>
