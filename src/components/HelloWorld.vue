<template>
  <div class="hello">
    <h1 style="text-align:center;background-color:purple">{{ msg }}</h1>
    <h2>Essential Links</h2>
    <router-link to="/login"><a>Login</a></router-link>
    &nbsp;&nbsp;
    <router-link to="/register"><a>Register</a></router-link>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Dizhu Chatroom'
    }
  }
}
</script>
