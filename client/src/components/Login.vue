<template>
    <div id="login">
        <form class="container">
         <img src="/static/1.jpg" width="200px" height="180px">
        <h1>{{title}}</h1>
        <label for="inputEmail" >Email:</label><br>
        <input v-model="username" type="email" id="inputEmail" placeholder="...@..com" required autocomplete="on" autofocus>
        <br><br><label for="inputPassword" >Password:</label>
        <br><input type="password" v-model="password" id="inputPassword" placeholder="pwd" required autofocus>
        <input type="checkbox" style = "font-size: 12px" value="remember-me"> remember me
         &nbsp; &nbsp; <a href="" style="color:blue">Forget Password?</a>
         <br><br>
        <button class="btn btn-lg btn-primary btn-block" @click="login" type="submit">Login</button>
        &nbsp;&nbsp;<router-link to="/"><a>Home Page</a></router-link>
      </form>
    </div>
</template>

<script>
// import {socket} from "@/api/socket"

import { Logger } from "@/common"
const logger = Logger.get("Login")

export default {
  name: 'Login',
  data () {
    const prevQuery = this.$route.query
    return {
      title: 'Login',
      username: null,
      password: null,
      redirect: prevQuery.redirect ? prevQuery.redirect : "/chat",
    }
  },
  methods: {
    login() {
      logger.log("Logging in...")
      this.$store.dispatch("attemptLogin", {
        username: this.username,
        password: this.password,
      }).then(() => {
        this.message = "ok!"
        // socket.connect()
        this.$router.push({ path: this.redirect })
      }, (err) => {
        this.message = "failed: " + err.error
      })
    },
  }
}
</script>
