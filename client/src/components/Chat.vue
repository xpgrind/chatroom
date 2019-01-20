<template>
    <div id="chat">
        <button @click="loadFriendList">Hello</button>
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
            title: 'Chat'
        }
    },
    methods: {
        loadFriendList() {
            logger.debug("Getting user list")
            this.$store.dispatch("loadFriendList")
        }
    },
    computed: {
        friendList() {
            return this.$store.state.friends
        }
    }
}
</script>
