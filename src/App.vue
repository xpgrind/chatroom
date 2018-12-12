<template>
  <div id="app">
    <p v-if="seen">now you see me. Seen = {{seen}}</p>
    <li v-for="todo in todos" :key="todo.text">
      {{ todo.text }}
    </li>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      seen: true,
      todos: [
        {text: 'dizhu'},
        {text: 'colby'},
        {text: 'chrisTOPHER'}
      ]
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

</style>
