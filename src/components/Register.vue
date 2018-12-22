<template>
    <div id="register">
        <form class="container">
        <img src="/static/2.jpg" width="190px" height="160px">
        <h1>{{title}}</h1>
        Name:<br>
        <input type="text" name="name" autocomplete="on" autofocus>
        <br><br>
        Email Address:<br>
        <input type="email" name="email" autocomplete="on" autofocus><br>
        <br>
        Password:<br>
        <input type="password" name="password" >
        <br><br>
        <button type="submit" value="Submit">Register</button>
        &nbsp;&nbsp;<router-link styel="text-align:center" to="/"><a>Home Page</a></router-link>
      </form>
    </div>
</template>

<script>
export default {
  name: 'Register',
  data () {
    return {
      title: 'Register'
    }
  }
}
</script>
