<template>
  <div id="login">
    <img src="/static/pig4.png" width="200px" height="180px">
    <form class="container" @submit.prevent="login">
      <h1>{{title}}</h1>Email:
      <br>
      <input
        v-model="email"
        type="text"
        name="email"
        autocomplete="on"
        autofocus
        @change="checkEmail"
      >
      <span :style="c1"> {{ message }}</span>
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
      <button type="submit" >Login</button>
      <span :style="c2"> {{ message1 }} </span>
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
            c1: "color: green",
            c2: "color: green",
            message1: "",
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
                        this.$router.push({ path: this.redirect })
                    }, error => {
                        this.c2 = "color: tomato"
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
            console.log("Login.vue: Email is " + this.email)
            this.$store
                .dispatch("checkEmail", {
                    newEmail: this.email
                })
                .then(
                    (json) => {
                        if (json.available) {
                            this.c1 = "color: tomato"
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

<style scooped>
img{
    position: absolute;
    left: 450px;
    top:0px;
    z-index: -1;
}
</style>
