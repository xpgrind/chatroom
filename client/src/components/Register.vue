<template>
  <div id="register">
    <span :style="c2">Register Message: {{ registerStatus }}</span>
    <img id="a" src="/static/1.png" width="200px" height="180px">
    <form class="container" @submit.prevent="registerUser">
      <h1>{{title}}</h1>
      Name:
      <br>
      <input
        v-model="username"
        type="text"
        name="name"
        autocomplete="on"
        autofocus
        @change="checkUsername"
      >
      <span :style="c">{{ message }}</span>
      <br><br>Email Address:
      <br>
      <input
        v-model="email"
        type="email"
        name="email"
        autocomplete="on"
        autofocus
        @change="checkEmail"
      >
      <span :style="c1">{{ message2 }}</span>
      <br>
      <br>Password:
      <br>
      <input v-model="password" type="password" name="password">
      <br>
      <br>
      <button type="submit" value="Submit">Register</button>
      <span>
      <router-link style="text-align:center" to="/">
        <a>Home Page</a>
      </router-link>
      </span>
    </form>
  </div>
</template>

<script>
export default {
    name: "Register",

    data() {
        const prevQuery = this.$route.query
        return {
            title: "Register",
            username: "",
            email: "",
            password: "",
            message: "",
            message2: "",
            registerStatus: "",
            c: "",
            c1: "",
            c2: "color:white",
            redirect: prevQuery.redirect ? prevQuery.redirect : "/profile",
        }
    },
    methods: {
        checkUsername() {
            console.log("Username is " + this.username)
            this.$store
                .dispatch("checkUsername", {
                    newUsername: this.username
                })
                .then(
                    (json) => {
                        if (json.available) {
                            this.c = "color:green"
                            this.message = "UserName Available"
                        } else {
                            this.c = "color:tomato"
                            this.message = "UserName Isn't Available"
                        }
                    }, err => {
                        this.c = "color:tomato"
                        this.message = " failed: " + err
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
                            this.c1 = "color:green"
                            this.message2 = "Email Available"
                        } else {
                            this.c1 = "color:tomato"
                            this.message2 = "Email Isn't Available"
                        }
                    }, err => {
                        this.c1 = "color:tomato"
                        this.message2 = "failed: " + err
                    }
                )
        },

        registerUser() {
            console.log("registerUser")
            this.$store
                .dispatch("registerUser", {
                    newUsername: this.username,
                    newEmail: this.email,
                    newPassword: this.password
                })
                .then(
                    () => {
                        this.c2 = "color:white"
                        this.registerStatus = "Register Succeeded, Go To Set Your Profile"
                        setTimeout(() => {
                            this.$router.push({ path: this.redirect })
                        }, 3000)
                    },
                    err => {
                        this.c2 = "color:tomato"
                        this.registerStatus = "" + err
                    }
                )
        }
    }
}
</script>

<style scoped>
#a{
    position: absolute;
    top: 35px;
    left:550px;
    z-index: -1;
}

div{
    margin-bottom: 10px;
}

#c{
    position: absolute;
    left: 580px;
    top: 220px;
}

span{
    margin-left:50px;
}

</style>
