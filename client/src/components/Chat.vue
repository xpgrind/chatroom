<template>
    <div id="chat">
         <h5>Input his/her username: <input type="text" v-model="friend"></h5>
        <button @click="addFriend()">Add Friend</button>
        <h4>Your Friends:</h4>
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
            friend: '',
        }
    },
    computed: {
        friendList() {
            return this.$store.state.friends
        }
    },
    methods: {
        addFriend() {
            console.log("Adding a friend " + this.friend)
            this.$store
                .dispatch("addFriend", {
                    newFriend: this.friend,
                })
                .then(
                    (json) => {
                        if (json) {
                            this.message = "Friend Not Found"
                        } else {
                            this.message = "Friend Found"
                        }
                    }, err => {
                        this.message = "failed: " + err
                    }
                )
        }
    }
}
</script>
