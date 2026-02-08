<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { computed } from 'vue';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  color: {
    type: String,
    default: '#3B82F6' // Blue default
  },
  label: {
      type: String,
      default: 'Frecuencia'
  }
})

const chartData = computed(() => ({
  labels: props.data.map(item => item.name),
  datasets: [
    {
      label: props.label,
      backgroundColor: props.color,
      data: props.data.map(item => item.count),
      borderRadius: 4
    }
  ]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y', // Horizontal bars
  plugins: {
    legend: {
        display: false
    }
  },
  scales: {
      x: {
          beginAtZero: true
      }
  }
}
</script>

<template>
  <div class="h-80">
    <Bar :data="chartData" :options="options" />
  </div>
</template>
