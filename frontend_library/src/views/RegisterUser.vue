<template>
  <div>
    <NavBar />
    <div class="container">
      <h1 class="heading">Sign Up</h1>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label for="inputName">Username</label>
          <input
            type="text"
            class="form-control"
            id="inputName"
            v-model="name"
          />  
        </div>
        <div class="form-group">
          <label for="inputEmail">Email address</label>
          <input
            type="email"
            class="form-control"
            id="inputEmail"
            aria-describedby="emailHelp"
            v-model="email"
          />
    
        </div>
        <div class="form-group">
          <label for="inputPassword">Password</label>
          <input
            type="password"
            class="form-control"
            id="inputPassword"
            v-model="password"
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            class="form-control"
            id="confirmPassword"
            v-model="confirmPassword"
          />
        </div>
        <div class="form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="agreeTerms"
            v-model="agreedToTerms"
          />
          <label class="form-check-label" for="agreeTerms">
            I agree to Terms and Conditions
          </label>
        </div>
        <div class="button">
          <button type="submit" class="btn btn-primary">Register</button>
        </div>
        <div class="have-account">
          <small class="mt-3">
            Already have an account?
            <router-link to="/">Login</router-link>
          </small>
        </div>
      </form>
    </div>
  </div>

</template>

<script>
import NavBar from "../components/NavBar.vue";
import axios from "axios";
export default {
  name: "RegisterUser",
  components: {
    NavBar,
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      agreedToTerms: false,
    };
  },
  methods: {
    registerUser() {
      if (!this.validateData()) {
        return;
      }

      axios.post("http://127.0.0.1:5000/api/signup", {
          name: this.name,
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          console.log("Response from backend:", response.data.message);
          this.$router.push('/');
        })
        .catch((error) => {
          if (error.response && error.response.status === 400) {
            alert(error.response.data.error);
          } else {
            alert("Unexpected Error Ocurred.Try Again Later");
            console.error("Error:", error);
          }
        });
    },
    // validation
    validateData() {
      if (
        this.name === "" ||
        this.email === "" ||
        this.password === "" ||
        this.confirmPassword === ""
      ) {
        alert("Please fill in all fields");
        return false;
      }
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match");
        return false;
      }
      if (!this.agreedToTerms) {
        alert("Please agree to terms and conditions");
        return false;
      }
      return true;
    },
  },
};
</script>

<style scoped>
.container {
  width: 40%;
  margin-top: 50px;
  border: 1px solid #000;
  border-radius: 10px;
  padding: 20px;
  font-family: Raleway, sans-serif;
  background-color: #333;
  color:white;
}

.heading {
  text-align: center;
  margin-bottom: 20px;
}

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-top: 15px;
  width: 30%;
  padding: 10px;
  border-radius: 10px;
  background-color: #000;
  border: none;
  color: #fff;
  font-size: 20px;
  cursor: pointer;
}

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.have-account {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
</style>
