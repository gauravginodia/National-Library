<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import ChartJs from 'chart.js/auto';
  
  export default {
    name: 'ChartBar',
    props: {
      chartData: {
        type: Object,
        required: true,
      },
      chartType: {
        type: String,
        default: 'bar',
      },
      options: {
        type: Object,
        default: () => ({}),
      },
    },
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        console.log("hello");
        const ctx = this.$refs.chartCanvas.getContext('2d');
        new ChartJs(ctx, {
          type: this.chartType,
          data: this.chartData,
          options: this.options,
        });
      },
    },
  };
  </script>
  