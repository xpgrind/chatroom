import Vue from "vue"
import axios from "axios"
import {API_URL} from "../api/socket"
// socket

import { Logger } from "@/common"
const logger = Logger.get("actions.js")

export default {
  testCommand({ commit }, { command, username }) {
    const requestBody = {username}
    console.log("Sending request to the server", command, requestBody)
    // socket.emit("users/" + command, requestBody)
  },

  socketConnected({ commit }, { connected }) {
    commit("setConnected", { connected })
  },

  attemptLogin({ commit }, { username, password }) {
    const url = API_URL + "/login"
    return new Promise((resolve, reject) => {
      axios
        .post(url, { username, password }, { withCredentials: true })
        .then(response => {
          return response.data
        })
        .then(json => {
          commit("setLogin", {
            token: json.token,
            info: {
              username: json.info.username,
            },
          })
          resolve()
        })
        .catch(error => {
          commit("clearLogin")
          logger.warn("Failed to log in ", error)
          reject(error.response.data)
        })
    })
  },

  clearLogin({ commit }) {
    // socket.disconnect()
    Vue.cookie.delete("token")
    commit("clearLogin")
  },
}
