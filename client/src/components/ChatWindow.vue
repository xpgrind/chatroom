<template>
    <div id="chatwindow">
        <button @click="loadFriendList">Hello World</button>
        <div v-for="friend in friendList" :key="friend">{{friend}}</div>
    </div>
</template>

<script>
import { Logger } from "@/common"

const logger = Logger.get("actions.js")

export default {
    name: 'ChatWindow',
    data () {
        return {
            title: 'ChatWindow'
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
