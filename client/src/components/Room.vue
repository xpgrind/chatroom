<template>
    <div id="room" class="container">
        <input v-model="message">
        <p>To: </p>
        <input v-model="friend">
        <button @click="send()">Send</button>

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
            friend: '',
            clientTime: ''
        }
    },
    computed: {
    },
    methods: {
        send() {
            console.log("Sending a message " + this.message)
            this.$store
                .dispatch("sendMsg", {newMsg: this.message, receiver: this.friend})
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
