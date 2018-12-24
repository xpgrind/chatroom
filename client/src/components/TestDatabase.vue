<template>
    <div id="test-database">
        Command: <input type="text" v-model="command">
        Username: <input type="text" v-model="username">
        <button @click="sendCommand">Send Request</button>
    </div>
</template>

<script>
export default {
  name: 'TestDatabase',
  data () {
    return {
      command: null,
      username: null
    }
  },
  methods: {
    sendCommand () {
      console.log('Sending request: command', this.command, 'username', this.username)
      this.$store.dispatch('testCommand', {
        command: this.command,
        username: this.username,
      })
    }
  }
}
</script>
