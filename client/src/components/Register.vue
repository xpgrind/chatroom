<template>
    <div id="register">
        <form class="container">
            <img src="/static/2.jpg" width="190px" height="160px">
            <h1>{{title}}</h1>
            Name:<br>
            <input v-model="username" type="text" name="name" autocomplete="on" autofocus @change="checkUsername">{{ message }}
            <br><br>
            Email Address:<br>
            <input v-model="email" type="email" name="email" autocomplete="on" autofocus @change="checkEmail">{{ message2 }}
            <br><br>
            Password:<br>
            <input v-model="password" type="password" name="password" >
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
            title: 'Register',
            username: '',
            email: '',
            password: '',
            message: '',
            message2: ''
        }
    },
    methods: {
        checkUsername() {
            console.log("Username is " + this.username)
            this.$store.dispatch("checkUsername", {
                newUsername: this.username,
            }).then(() => {
                this.message = "Username Available"
            }, (err) => {
                this.message = "failed: " + err
            })
        },
        checkEmail() {
            console.log("Email is " + this.email)
            this.$store.dispatch("checkEmail", {
                newEmail: this.email,
            }).then(() => {
                this.message2 = "Email Available"
            }, (err) => {
                this.message2 = "failed: " + err
            })
        }
    },
}
</script>
