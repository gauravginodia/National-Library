<template>
	<div>
		<NavBar />
		<div class="container">
			<div class="screen">
				<div class="screen__content">
					<div class="error" v-if="errorMessage">{{ errorMessage }}</div>
					<form class="login" @submit.prevent="login">
						<div class="login__field">
							<!-- User icon -->
							<i class="bi bi-person-circle login__icon"></i> <!-- Bootstrap icon for user -->
							<input type="text" class="login__input" placeholder="Email" v-model="email">
						</div>
						<div class="login__field">
							<!-- Password icon -->
							<i class="bi bi-lock-fill login__icon"></i> <!-- Bootstrap icon for lock -->
							<input type="password" class="login__input" placeholder="Password" v-model="password">
						</div>
						<button class="button login__submit">
							<span class="button__text">Log In Now</span>
							<i class="bi bi-chevron-right button__icon"></i> <!-- Bootstrap icon for chevron right -->
						</button>
					</form>
					
					<div class="social-login" >
						<h5 style="margin-top: 1% ;padding-top: 1%;">New User ? </h5>
						<div class="social-icons">
							<router-link to="/RegisterUser" style="color:white">Signup</router-link>
						</div>
					</div>
				</div>

				<div class="screen__background">
					<span class="screen__background__shape screen__background__shape4"></span>
					<span class="screen__background__shape screen__background__shape3"></span>
					<span class="screen__background__shape screen__background__shape2"></span>
					<span class="screen__background__shape screen__background__shape1"></span>
				</div>
			</div>
		</div>
		
	</div>
</template>


<script>
import axios from "axios";
import NavBar from "@/components/NavBar.vue";

export default {
	name: "UserAuthentication",
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
		async login() {
			try {
				const response = await axios.post("http://127.0.0.1:5000/api/login", {
					email: this.email,
					password: this.password,
				});

				if (response.status === 200 && response.data.access_token) {
					localStorage.setItem('accessToken', response.data.access_token);
					localStorage.setItem('userType', "user")
					localStorage.setItem('user', JSON.stringify(response.data.userName));
					this.$router.push('/user/dashboard');
					console.log("Login successful. Redirecting to dashboard...");
				} else {
					console.error("Error: Unexpected response from server");
					this.errorMessage = "Unexpected response from server";
				}
			} catch (error) {
				console.error("Error logging in:", error);
				this.errorMessage = error.response ? error.response.data.error : "Unknown error occurred";
			}
		},
	},
};
</script>



<style scoped>
@import url('https://fonts.googleapis.com/css?family=Raleway:400,700');

* {
	box-sizing: border-box;
	margin: 0;
	padding: 0;
	font-family: Raleway, sans-serif;
}

body {
	background: linear-gradient(90deg, #C7C5F4, #776BCC);
}

.container {
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 100vh;
	-ms-flex-align: center;
	margin-left: 2%;
}

.screen {
	background: #333;
	position:relative;
	justify-content: center;
	height: 570px;
	width: 360px;
	box-shadow: 0px 0px 24px #5C5696;
}

.screen__content {
	z-index: 1;
	position: relative;
	height: 100%;
}

.screen__background {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	z-index: 0;
	-webkit-clip-path: inset(0 0 0 0);
	clip-path: inset(0 0 0 0);
}

.screen__background__shape {
	transform: rotate(45deg);
	position: absolute;
}

.screen__background__shape1 {
	height: 520px;
	width: 520px;
	background: #FFF;
	top: -50px;
	right: 120px;
	border-radius: 0 72px 0 0;
}

.screen__background__shape2 {
	height: 220px;
	width: 220px;
	background: #333;
	top: -172px;
	right: 0;
	border-radius: 32px;
}

.screen__background__shape3 {
	height: 540px;
	width: 190px;
	background: #333;
	top: -24px;
	right: 0;
	border-radius: 32px;
}

.screen__background__shape4 {
	height: 400px;
	width: 200px;
	background: #333;
	top: 420px;
	right: 50px;
	border-radius: 60px;
}

.login {
	width: 320px;
	padding: 30px;
	padding-top: 156px;
}

.login__field {
	padding: 20px 0px;
	position: relative;
}

.login__icon {
	position: absolute;
	top: 30px;
	color: black;
}

.login__input {
	border: none;
	border-bottom: 2px solid #D1D1D4;
	background: none;
	padding: 10px;
	padding-left: 24px;
	font-weight: 700;
	width: 75%;
	transition: .2s;
}

.login__input:active,
.login__input:focus,
.login__input:hover {
	outline: none;
	border-bottom-color: black;
}

.login__submit {
	background: #fff;
	font-size: 14px;
	margin-top: 30px;
	padding: 16px 20px;
	border-radius: 26px;
	border: 1px solid #D4D3E8;
	text-transform: uppercase;
	font-weight: 700;
	display: flex;
	align-items: center;
	width: 100%;
	color: rgba(26, 24, 24, 0.615);
	box-shadow: 0px 2px 2px rgba(128, 128, 128, 0.253);
	cursor: pointer;
	transition: .2s;
}

.login__submit:active,
.login__submit:focus,
.login__submit:hover {
	border-color: black;
	border-width: 0.5cap;
	outline: none;
}

.button__icon {
	font-size: 24px;
	margin-left: auto;
	color: #333;
}

.social-login {
	position: absolute;
	height: 140px;
	width: 160px;
	text-align: center;
	bottom: 0px;
	right: 0px;
	color: #fff;
	text-size-adjust: 17;
}

.social-icons {
	display: flex;
	align-items: center;
	justify-content: center;

}



.error {
	color: red;
	text-align: center;
	margin-top: 10px;
}
</style>
