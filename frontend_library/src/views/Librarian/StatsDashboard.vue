<template>
  <NavBar/>
  <div class="librarian-dashboard">
    <h1 class="dashboard-title">Librarian Dashboard</h1>
    <div class="chart-container" >
      <!-- Row 1 -->
      <div class="" v-if="distributionData.labels && distributionData.labels.length">
        <div class="chart-card" style="margin-bottom:5%;">
          <h2>Book Distribution by Section</h2>
          <ChartBar :chart-data="distributionData" chart-type="pie" :options="options"/>
        </div>
      </div>
      <div class="" v-if="issuancesData.labels && issuancesData.labels.length">
        <div class="chart-card">
          <h2>Book Issuances Trend Over Time</h2>
          <ChartBar :chart-data="issuancesData" chart-type="line" :options="options"/>
        </div>
      </div>
      <div class="" v-if="issuedData.labels && issuedData.labels.length">
        <div class="chart-card">
          <h2 >Books Issued per Section</h2>
          <ChartBar :chart-data="issuedData" chart-type="doughnut" :options="options" />
        </div>
      </div>
    </div>
      <!-- Row 2 -->
      <div class="chart-item" v-if="ratingsData.labels && ratingsData.labels.length">
        <div class="chart-card">
          <h2>Books by Ratings</h2>
          <ChartBar :chart-data="ratingsData" chart-type="bar" :options="{
            scales: {
              x: {
                beginAtZero: false,
                suggestedMin: 0,
                suggestedMax: 10,
                ticks: {
                  stepSize: 1,
                },
              },
              y: {
                beginAtZero: true,
                suggestedMin: 0,
                suggestedMax: 5,
                ticks: {
                  stepSize: 1,
                },
              },
            }
          }" />
        </div>
      </div>
   
  </div>
</template>

<style scoped>
.librarian-dashboard {
  padding: 20px;
}

.dashboard-title {
  margin-top: 20px;
  margin-bottom: 30px;
  text-align: center;
  color: #333;
}

.chart-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.chart-item {
  width: 100%; /* Adjust the width as needed */
  margin-bottom: 20px;
}

.chart-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

canvas {
  width: 100%;
  height: 300px; /* Set the height as per your requirement */
}
</style>

<script>
import axios from 'axios';
import ChartBar from '@/components/ChartBar.vue';
import { getRandomColorArray } from '@/utils/colors'; // Import color utility
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'StatsDashboard',
  components: {
    ChartBar,
    NavBar
  },
  data() {
    return {
      distributionData: {},
      issuancesData: {},
      issuedData: {},
      ratingsData: {},
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };
  },
  async mounted() {
  try {
    await this.fetchDistributionData();
    await this.fetchIssuancesData();
    await this.fetchIssuedData();
    await this.fetchRatingsData();
  } catch (error) {
    console.error('Error fetching data:', error.message);
  }
},

  methods: {

    async fetchDistributionData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/section/books/distribution', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.distributionData = {
          labels: response.data.labels,
          datasets: [{
            label: 'Books',
            backgroundColor: getRandomColorArray(response.data.labels.length),
            data: response.data.data,
          }],
        };
      } catch (error) {
        console.error('Error fetching book distribution data:', error.message);
      }
    },
    async fetchIssuancesData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/book/issuances/trend', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.issuancesData = {
          labels: response.data.labels,
          datasets: [{
            label: 'Issuances',
            backgroundColor: getRandomColorArray(response.data.labels.length),
            data: response.data.data,
          }],
        };
      } catch (error) {
        console.error('Error fetching book issuances trend data:', error.message);
      }
    },
    async fetchIssuedData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/section/books/issued', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.issuedData = {
          labels: response.data.labels,
          datasets: [{
            label: 'Books Issued',
            backgroundColor: getRandomColorArray(response.data.labels.length),
            data: response.data.data,
          }],
        };
      } catch (error) {
        console.error('Error fetching books issued per section data:', error.message);
      }
    },
    async fetchRatingsData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/books/ratings', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.ratingsData = {
          labels: response.data.labels,
          datasets: [{
            label: 'Ratings',
            backgroundColor:'dodgerblue',
            data: response.data.data,
          }],
        };
        console.log(this.ratingsData);
      } catch (error) {
        console.error('Error fetching books by ratings data:', error.message);
      }
    },
  },
};
</script>

