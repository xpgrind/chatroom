<template>
  <div id="app">
    <div v-show="seen">
      <li v-for="pic in pics" v-bind:key="pic.name">
        <img :src="pic.src">
      </li>
    </div>

    <div>
      <h1>Hello, Slideshow !</h1>
      <br>
      <br>

      <p>How Do You Want To Play It ?</p>
      <select v-model="selected1" id="play">
        <option v-for="option in optionList1" v-bind:key="option.value">{{ option.key }}</option>
      </select>

      <p>What Effect Do You Want ?</p>
      <select v-model="selected2" id="effect">
        <option v-for="option in optionList2" v-bind:key="option.value">{{ option.key }}</option>
      </select>

      <br>
      <div>Your choice is: {{ selected1 +" and " + selected2 }}</div>

      <br>
      <div :class = "{ color: show_error_message }" v-if="show_error_message">
          You must select both options!
      </div>

      <button @click="show()">Start</button>
    </div>
  </div>
</template>

<script>
const imgFolder = "/static/"

export default {
  name: "App",
  data () {
    return {
      seen: false,
      show_error_message: false,

      pics: [
        { src: imgFolder + "1.jpg", name: "Caption 1" },
        { src: imgFolder + "2.jpg", name: "Caption 2" },
        { src: imgFolder + "3.jpg", name: "Caption 3" },
        { src: imgFolder + "4.jpg", name: "Caption 4" },
        { src: imgFolder + "5.jpg", name: "Caption 5" },
        { src: imgFolder + "6.jpg", name: "Caption 6" },
        { src: imgFolder + "7.jpg", name: "Caption 7" }
      ],

      optionList1: [
        { key: "Random", value: "Random" },
        { key: "Sequential", value: "Sequential" }
      ],
      selected1: "",

      optionList2: [
        { key: "Transformation", value: "Transformation" },
        { key: "Transition", value: "Transition" },
        { key: "None", value: "None" }
      ],

      selected2: "",

      free: true
    }
  },
  methods: {

    show () {
      if (this.selected1 && this.selected2) {
        this.show_error_message = false
      } else {
        this.show_error_message = true
      }
    }
  }
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  background-color: lightblue;
  font-family: Verdana, sans-serif;
}

h1 {
  background-color: rgb(141, 218, 141);
}

p {
  background-color: yellow;
}

.color{
  font-size: large;
  color: red;
}

.prev,
.next,
.start,
.stop {
  cursor: pointer;
  position: absolute;
  top: 50%;
  width: auto;
  padding: 16px;
  margin-top: -22px;
  color: rgb(223, 73, 178);
  font-weight: bold;
  font-size: 36px;
  transition: 0.6s ease;
  border-radius: 0 4px 4px 0;
  user-select: none;
}

/* Position the "next button" to the right */
.next {
  right: 0;
  border-radius: 4px 0 0 4px;
}

/* Position the "start button" to the right */
.start {
  right: 500px;
  border-radius: 4px 4px 4px 4px;
}

/* Position the "next button" to the middle */
.stop {
  right: 300px;
  border-radius: 4px 4px 4px 4px;
}

.prev:hover,
.next:hover,
.start:hover,
.stop:hover {
  background-color: rgb(78, 209, 89);
}
</style>
