<template>
    <div id="chat" class="container">
        <button @click="loadFriends()">Load Friendslist</button>
        <p>Friends: </p>
        <div v-show="see" v-for="friend in friendList" :key="friend">{{friend}}</div>
        <h5>Input his/her username: <input type="text" v-model="friend"></h5>
        <button @click="addFriend()">Add Friend</button>
        <p :style="color1">{{ message1 }}</p>
        <button>Clear Friends</button>
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
