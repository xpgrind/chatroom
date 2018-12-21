<template>
  <div id="app">
    <router-view></router-view>
    <login-form></login-form>
    <register-form :v-for="item in sites" v-bind:todo="item"></register-form>
  </div>
</template>

<script>
import LoginForm from '@/components/LoginForm'
import registerForm from '@/components/registerForm'
// import Vue from "@/main"
// const imgFolder = "/static/"

export default {
  name: "App",

  components: {
    LoginForm,
    registerForm
  },

  data () {
    return {
    }
  }
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  background-color: lightblue;
  font-family: Verdana, sans-serif;
}

h1 {
  background-color: rgb(141, 218, 141);
}

p {
  background-color: yellow;
}

.color{
  font-size: large;
  color: red;
}

</style>
