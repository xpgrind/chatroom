<template>
    <div class="hello">
        <h2>Essential Links</h2>
        <router-link to="/login"><a class="hover">Login</a></router-link>
        &nbsp;&nbsp;
        <router-link to="/register"><a class="hover">Register</a></router-link>
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
