<template>
    <div id="room" class="container">

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
            imgNum: 3
        }
    },
    computed: {
    },
    methods: {
    }
}
</script>

<style scooped>
span{
    margin-left: 30px;
}
.container {
  width: 600px;
  height: 500px;
}
</style>
