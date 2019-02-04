<template>
  <div id="login">
    <form class="container" @submit.prevent="login">
      <!-- <img src="/static/1.jpg" width="200px" height="180px"> -->
      <h1>{{title}}</h1>Name:
      <br>
      <input
        v-model="email"
        type="text"
        name="email"
        autocomplete="on"
        autofocus
        @change="checkEmail"
      >
      {{ message }}
      <br>
      <br>
      <label for="inputPassword">Password:</label>
      <br>
      <input
        type="password"
        v-model="password"
        id="inputPassword"
        placeholder="pwd"
        required
        autofocus
      >
      <input type="checkbox" style="font-size: 12px" value="remember-me"> remember me
      &nbsp; &nbsp;
      <a href style="color:blue">Forget Password?</a>
      <br>
      <br>
      <button class="btn btn-lg btn-primary btn-block" type="submit">Login</button>
      {{ message1 }}
      &nbsp;&nbsp;
      <router-link to="/">
        <a>Home Page</a>
      </router-link>
    </form>
  </div>
</template>

<script>
import { Logger } from "@/common"

const logger = Logger.get("Login")

export default {
    name: "Login",
    data() {
        const prevQuery = this.$route.query
        return {
            title: "Login",
            email: null,
            password: null,
            redirect: prevQuery.redirect ? prevQuery.redirect : "/chat",
            message: "",
            message1: ""
        }
    },
    methods: {
        login() {
            logger.log("Logging in...")
            this.$store
                .dispatch("attemptLogin", {
                    email: this.email,
                    password: this.password
                })
                .then(
                    (response) => {
                        this.message1 = "Succeeded:  Your User ID is" // + response.data.ID
                        setTimeout(() => {
                            this.$router.push({ path: this.redirect })
                        }, 3000)
                    }, error => {
                        logger.warn("Login.Vue Login Failed", error.response)
                        if (error.response && error.response.data) {
                            this.message1 = "failed: " + error.response.data.message
                        } else {
                            this.message1 = "No reason given"
                        }
                    }
                )
        },
        checkEmail() {
            console.log("Email is " + this.email)
            this.$store
                .dispatch("checkEmail", {
                    newEmail: this.email
                })
                .then(
                    (json) => {
                        if (json.available) {
                            this.message = "Email Not Found"
                        } else {
                            this.message = "Email Found"
                        }
                    }, err => {
                        this.message = "failed: " + err
                    }
                )
        }
    }
}
</script>
