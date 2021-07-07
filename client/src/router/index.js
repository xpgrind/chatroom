import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/Login'
import Chat from '@/components/Chat'
import Register from '@/components/Register'
import Room from '@/components/Room'
import Profile from '@/components/Profile'
import TestDatabase from '@/components/TestDatabase'

Vue.use(Router) // register router

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
        {
            path: '/room',
            name: 'Room',
            component: Room
        },
        {
            path: '/profile',
            name: 'Profile',
            component: Profile
        },
    ]
})
