<script setup>
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale
} from 'chart.js'
import { computed } from 'vue';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chartData = computed(() => ({
  labels: ['Estudiantes', 'Titulados', 'Administradores'],
  datasets: [
    {
      backgroundColor: ['#3B82F6', '#6366F1', '#8B5CF6'],
      data: [
        props.data.roles.estudiante,
        props.data.roles.titulado,
        props.data.roles.administrador
      ]
    }
  ]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
        position: 'bottom'
    },
    tooltip: {
        callbacks: {
            label: function(context) {
                let label = context.label || '';
                if (label) {
                    label += ': ';
                }
                let value = context.parsed;
                let total = context.chart._metasets[context.datasetIndex].total;
                let percentage = Math.round(value / total * 100) + '%';
                return label + value + ' (' + percentage + ')';
            }
        }
    }
  }
}
</script>

<template>
  <div class="h-64">
    <Doughnut :data="chartData" :options="options" />
  </div>
</template>
