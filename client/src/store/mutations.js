import Vue from "vue"
import { Logger } from "@/common"

const logger = Logger.get("mutations.js")

export default {
    setLogin(state, { username, token }) {
        logger.debug("Set Username:", username, "token", token)
        state.username = username
        state.token = token
        if (window.localStorage) {
            window.localStorage.setItem("chatroom_username", username)
            window.localStorage.setItem("chatroom_token", token)
        }
    },

    clearLogin(state) {
        logger.debug("Clear Username")
        state.username = null
        state.token = null
        state.friends = null
        if (window.localStorage) {
            window.localStorage.removeItem("chatroom_username")
            window.localStorage.removeItem("chatroom_token")
        }
    },

    setFriendList(state, { friends }) {
        logger.debug("Set Friends:", friends)
        state.friends = friends
    },
}
