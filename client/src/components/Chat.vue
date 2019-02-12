<template>
    <div id="chat" class="container">
        <h2>Friendship</h2>
        <img src="/static/pig5.png" width="200px" height="180px">
         <h5>Input his/her username: <input type="text" v-model="friend"></h5>
         <img class="c" src="/static/profile.png" width="100px" height="100px">
          <button type="button" class="d">Upload profile picture</button>
        <button @click="addFriend()">Add Friend</button>
        <p :style="color1">{{ message1 }}</p>
        <button @click="loadFriends()">Load Friendslist</button>
        <h4>Your Friends: </h4>
        <div v-show="see" v-for="friend in friendList" :key="friend">{{friend}}</div>
        <button class="e">Open Chat Room</button>
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
            friend: '',
            message1: '',
            color1: '',
            see: false
        }
    },
    computed: {
        friendList() {
            return this.$store.state.friends
        }
    },
    methods: {
        clearFriend() {
            console.log("Clearing friends List ")
            this.$store
                .dispatch("clearFriends")
                .then(
                    (json) => {
                        if (json) {
                            this.message2 = "Loading FriendList"
                        } else {
                            this.message2 = "No Friend"
                        }
                    }, err => {
                        this.message2 = "failed: " + err
                    }
                )
        },

        addFriend() {
            console.log("Adding a friend " + this.friend)
            this.$store
                .dispatch("addFriend", {
                    newFriend: this.friend,
                })
                .then(
                    (json) => {
                        if (json) {
                            this.message1 = "Adding Friend Failed"
                        } else {
                            this.color1 = "color:purple"
                            this.message1 = "Adding Friend Succeeded !"
                        }
                    }, err => {
                        logger.warn("Failed", err)
                        this.message1 = '' + err
                        this.color1 = "color:red"
                    }
                )
        },
        loadFriends() {
            console.log("Loading friends List ")
            this.see = true
            this.$store
                .dispatch("loadFriendList")
        }
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
</style>
