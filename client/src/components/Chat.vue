<template>
    <div id="chat">
         <h5>Input his/her username: <input type="text" v-model="name"></h5>
        <button @click="addFriend">Add Friend</button>
        <h4>Your Friends:</h4>
        <button @click="loadFriendList">Load FriendsList</button>
        <div v-for="friend in friendList" :key="friend">{{friend}}</div>
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
            name: '',
        }
    },

    methods: {
        addFriend() {
        this.$store.state.friends.push(name)
        this.friendList.push(this.name)

        this.$store
            .dispatch("setFriendsList", {
                friendList: this.friendList,
            })
            .then(
                () => {
                }, error => {
                    logger.warn("Login.Vue Login Failed", error.response)
                    if (error.response && error.response.data) {
                        this.message1 = "failed: " + error.response.data.message
                    } else {
                        this.message1 = "No reason given"
                    }
                }
            )
        }
    },

    computed: {
        friendList() {
            return this.$store.state.friends
        }
    }
}
</script>
