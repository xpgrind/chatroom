<template>
    <div id="chat">
        <h2>Welcome,   {{ username }}   !</h2>
            <div class="container">
            <!-- <img class="a" :src="picture" width="100px" height="100px"> -->
            <button @click="loadFriends()">Load Friendslist</button>
            <p>Friends: </p>
            <span v-show="see" v-for="friend in friendList" :key="friend">
               <router-link to="/room">
                    <a>{{ friend }} </a>
                </router-link>
            </span>
            <h5>Input his/her username: <input type="text" v-model="friend1"></h5>
            <button @click="addFriend()" >Add Friend</button>
            <p :style="color1">{{ message1 }}</p>
            <h5>Delete this person: <input type="text" v-model="friend2"></h5>
            <button @click="clearFriend()">Delete Friend</button>
            <p :style="color2">{{ message2 }}</p>
            <div>
            <button>Log Out</button>
            </div>
        </div>
    </div>
</template>

<script>
import { Logger } from "@/common"

const logger = Logger.get("actions.js")

export default {
    name: 'Chat',

    data () {
        return {
            title: 'Chat',
            friend1: '',
            friend2: '',
            message1: '',
            message2: '',
            color1: '',
            color2: '',
            see: false,
        }
    },
    computed: {
        friendList() {
            return this.$store.state.friends
        },

        username() {
            return this.$store.state.username
        },

        picture() {
            return this.$store.state.photo
        }
    },
    methods: {
        clearFriend() {
            console.log("Adding a friend " + this.friend2)
            this.$store
                .dispatch("deleteFriend", {
                    friend: this.friend2,
                })
                .then(
                    (json) => {
                        logger.debug("deleteFriend success, got json:", json)
                        this.color2 = "color:purple"
                        this.message2 = "Deleting Friend Succeeded !"
                    },
                    (error) => {
                        logger.warn("addFriend Failed", error, "response", error.response)
                        this.message2 = '' + error.response.data.message
                        this.color2 = "color:red"
                    }
                )
        },

        addFriend() {
            console.log("Adding a friend " + this.friend1)
            this.$store
                .dispatch("addFriend", {
                    newFriend: this.friend1,
                })
                .then(
                    (json) => {
                        logger.debug("addFriend success, got json:", json)
                        this.color1 = "color:purple"
                        this.message1 = "Adding Friend Succeeded !"
                    },
                    (error) => {
                        logger.warn("addFriend Failed", error, "response", error.response)
                        this.message1 = '' + error.response.data.message
                        this.color1 = "color:red"
                    }
                )
        },

        loadFriends() {
            console.log("Loading friends List ")
            this.see = true
            this.$store
                .dispatch("loadFriendList")
        },
    }
}
</script>

<style scooped>
img{
    position: absolute;
    left: 450px;
    top:0px;
}
span{
    margin-left: 30px;
}

.a {
    position: relative;
    left: 600px;
    top:100px;
}
.c{
    position: absolute;
    left: 600px;
    top:180px;
}

.e{
    position: absolute;
    bottom: 100px;
    left: 580px;
}

h2, h5{
    color:rgb(53, 255, 255);
}

div{
    margin-top: 15px;
}

.container{
    width: 600px;
    height: 300px;
}
</style>
