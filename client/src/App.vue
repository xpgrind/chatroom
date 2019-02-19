<template>
    <div id="app">
        <h1 class="page-title">Pig's Chatroom</h1>
        <router-view></router-view>
    </div>
</template>

<script>
import Login from '@/components/Login'
import Register from '@/components/Register'
import store from "@/store/index"
// import Vue from "@/main"
// const imgFolder = "/static/"
export default {
    name: 'App',

    components: {
        Login,
        Register,
    },

    data () {
        return {
        }
    },

    created:
        function() {
            console.log("Loading Perosnal Info ")
            this.$store.dispatch("loadUserInfo")
        }
}
</script>

<style>
*{
  color:rgb(107, 224, 84);
  font-family: Verdana, sans-serif;
}

body{
    background-color: rgb(95, 128, 201);
}

form{
  margin-bottom: 100px;
  margin-left: 300px;
}
 a:hover{
  background-color: purple;
  text-decoration: underline;
 }

span{
    margin-left: 30px;
}
.container {
  border-style: dotted;
  background-color: ivory;
  width: 650px;
  padding-top: 30px;
  padding-left: 30px;
  padding-bottom: 30px;
  border: 6px solid grey;
  margin: 80px;
  border-radius: 12px;
}

</style>
