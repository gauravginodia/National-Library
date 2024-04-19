<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
      <!-- Brand link -->
      <router-link :to="brandLink" class="navbar-brand">
        <img :src="require('@/assets/library_logo.png')" alt="National Library Logo" style="width: 300px; height: 50px;">
      </router-link>

      <!-- Toggle button -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <!-- Navigation links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li v-for="link in navLinks" :key="link.name" class="nav-item">
            <router-link :to="link.to" class="nav-link" :active-class="'active'">{{ link.label }}</router-link>
          </li>
        </ul>
      </div>

      <!-- Logout button and date-time display -->
      <div class="navbar-right">
        <button v-if="isLoggedIn" class="btn btn-outline-danger" @click="logout" style="width:fit-content;padding:1.5%;margin-left: 0%;">Logout</button>
        <div class="date-time">
          <div class="date-time-box">
            {{ currentDate }}
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      isLoggedIn: false,
      userType: '',
      currentDate: ''
    };
  },
  computed: {
    brandLink() {
      if (this.isLoggedIn && this.userType === 'librarian') {
        return '/librarian/dashboard';
      } else if (this.isLoggedIn && this.userType === 'user') {
        return '/user/dashboard';
      } else {
        return '/';
      }
    },
    navLinks() {
      const links = [];
      if (this.isLoggedIn) {
        if (this.userType === 'librarian') {
          links.push(
            { name: 'Dashboard', to: '/librarian/dashboard', label: 'Dashboard' },
            { name: 'SectionManagement', to: '/librarian/dashboard/sections', label: 'Sections' },
            { name: 'RequestedBooks', to: '/librarian/dashboard/requestedbooks', label: 'Requests' },
            { name: 'AssignedBooks', to: '/librarian/dashboard/assignedbooks', label: 'Allocated' },
            { name: 'StatusBooks', to: '/librarian/dashboard/bookstatus', label: 'Available' },
            
          );
        } else {
          links.push(
            { name: 'Dashboard', to: '/user/dashboard', label: 'Home' },
            { name: 'IssuedBooks', to: '/user/dashboard/issuedbooks', label: 'Issued Books' },
            { name: 'AllBooks', to: '/user/dashboard/history', label: 'Your History' },
          );
        } 
      } else {
        links.push(
          { name: 'UserAuthentication', to: '/', label: 'User Login' },
          { name: 'LibrarianAuthentication', to: '/librarian/login', label: 'Librarian Login' },
        );
      }
      return links;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userType');
      this.isLoggedIn = false;
      this.userType = '';
      this.$router.push('/');
    },
    updateDateTime() {
      const now = new Date();
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
      this.currentDate = now.toLocaleDateString('en-IN', options);
    }
  },
  created() {
    this.isLoggedIn = localStorage.getItem('accessToken') !== null;
    this.userType = localStorage.getItem('userType');
    this.updateDateTime(); // Update date-time initially
    setInterval(() => {
      this.updateDateTime(); // Update date-time every second
    }, 1000);
  }
};
</script>

<style scoped>
/* Add your CSS styles here */
.navbar {
  background-color: #333; /* Dark grey background */
}

.navbar-brand,
.nav-link {
  color: #fff; 
  font-family: 'Open Sans', sans-serif;
  font-size:medium;/* White text color */
}

.nav-link:hover {
  color: #1ee2e7; /* Text color on hover */
}

.active { /* Apply styling to the active link directly */
  background-color: #1ee2e7; /* Background color for active link */
}

.active:hover {
  background-color: #17d0d5; /* Hover color for active link */
}

.navbar-right {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.date-time {
  margin-left: 20px;
}

.date-time-box {
  border: 2px solid #fff;
  padding: 5px 10px;
  color: #fff;
  font-family: 'Open Sans', sans-serif;
}
</style>
