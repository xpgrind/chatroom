<template>
    <div id="login">
        <form class="container">
         <img src="/static/1.jpg" width="200px" height="180px">
        <h1>{{title}}</h1>
        <label for="inputEmail" >Email:</label><br>
        <input type="email" id="inputEmail" placeholder="email add" required autocomplete="on" autofocus>
        <br><br><label for="inputPassword" >Password:</label>
        <br><input type="password" id="inputPassword" placeholder="password" required autofocus>
        <input type="checkbox" style = "font-size: 12px" value="remember-me"> remember me
         &nbsp; &nbsp; <a href="" style="color:blue">Forget Password?</a>
         <br><br>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Login</button>
        &nbsp;&nbsp;<router-link to="/"><a>Home Page</a></router-link>
      </form>
    </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      title: 'Login'
    }
  }
}
</script>
