<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import Login from '@/components/Login'
import Register from '@/components/Register'
// import Vue from "@/main"
// const imgFolder = "/static/"

export default {
  name: 'App',

  components: {
    Login,
    Register
  },

  data () {
    return {
    }
  }
}
</script>

<style>
*{
  color:rgb(28, 160, 28);
  font-family: Verdana, sans-serif;
}

body {
  background-color: lightblue;
}

form{
  margin-bottom: 100px;
  margin-left: 300px;
}
 a:hover{
  background-color: yellow;
  text-decoration: underline;
 }

.container {
  border-style: dotted;
  background-color: aliceblue;
  width: 600px;
  padding-top: 20px;
  padding-left: 30px;
  padding-bottom: 30px;
  border: 2px solid grey;
  margin: 50px;
}

</style>
