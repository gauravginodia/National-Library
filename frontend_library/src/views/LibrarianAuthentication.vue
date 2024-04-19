<template>
  <div>
    <NavBar />
    <div class="dark-container">
      <div class="dark-form-container">
        <h1 class="dark-header">Librarian Login</h1>
        <form @submit.prevent="darkLogin">
          <div class="dark-mb-3">
            <label for="darkEmailInput" class="dark-form-label">Email address</label>
            <input
              v-model="email"
              type="email"
              class="dark-form-control"
              id="darkEmailInput"
            />
          </div>
          <div class="dark-mb-3">
            <label for="darkPasswordInput" class="dark-form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="dark-form-control"
              id="darkPasswordInput"
            />
          </div>
          <div class="dark-button">
            <button type="submit" class="dark-btn dark-btn-primary">Submit</button>
          </div>
          <div class="dark-error-message" v-if="errorMessage">{{ errorMessage }}</div>
        </form>
      </div>
    </div>
  </div>

</template>

<script>
import NavBar from "../components/NavBar.vue";

import axios from "axios";

export default {
  name: "LibrarianAuthentication",
  components: {
    NavBar,
  },
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    darkLogin() {
      axios
        .post("http://127.0.0.1:5000/api/librarian/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          const { access_token } = response.data;
          localStorage.setItem("accessToken", access_token);
          localStorage.setItem("userType", "librarian");
          console.log(
            "Login successful."
          );
          // Redirect or perform any other actions upon successful login
          this.$router.push("/librarian/dashboard");
        })
        .catch((error) => {
          this.errorMessage = "Invalid email or password. Please try again.";
          console.error(
            "An error occurred while logging in:",
            error.response.data.error
          );
        });
    },
  },
};
</script>

<style scoped>
.dark-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  
  
}

.dark-form-container {
  width: 60%; /* Adjust maximum width as needed */
  background-color: #333;
  padding: 10%;
}

.dark-header {
  text-align: center;
  margin-bottom: 20px;
  color: #ecf0f1;
}

.dark-form-label {
  color: #ecf0f1;
  margin-bottom: 8px;
  display: block;
}

.dark-form-control {
  background-color: #34495e;
  color: #ecf0f1;
  border-color: #2c3e50;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  box-sizing: border-box;
}

.dark-btn-primary {
  display: block;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  background-color: #2980b9;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  margin-top: 20px;
}

.dark-error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
