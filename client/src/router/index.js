import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/Login'
import Chat from '@/components/Chat'
import Register from '@/components/Register'
import TestDatabase from '@/components/TestDatabase'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/chat',
            name: 'Chat',
            component: Chat
        },

        {
            path: '/',
            name: 'HelloWorld',
            component: HelloWorld
        },
        {
            path: '/register',
            name: 'Register',
            component: Register
        },
        {
            path: '/test',
            name: 'TestDatabase',
            component: TestDatabase
        },
    ]
})
