<template>
    <div id="room" class="container">
        <input v-model="message">
        <button @click="send()">Send</button>
        <p>To: </p>
        <input v-bind="friend">
        <p>{{ message }}</p>

    </div>
</template>

<script>
import { Logger } from "@/common"

const logger = Logger.get("actions.js")

export default {
    name: 'Room',

    data () {
        return {
            title: 'Room',
            message: '',
            friend: ''
        }
    },
    computed: {
    },
    methods: {
        send() {
            console.log("Sending a message " + this.message)
            this.$store
                .dispatch("sendMsg", {
                    newMsg: this.message,
                    receiver_id: this.friend
                })
                .then(
                    (json) => {
                        logger.debug("success, got json:", json)
                    },
                    (error) => {
                        logger.warn("Failed", error, "response", error.response)
                    }
                )
        }

    }
}
</script>

<style scooped>
.container {
    width: 600px;
    height: 500px;
}
</style>
