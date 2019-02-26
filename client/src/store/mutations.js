import Vue from "vue"
import { Logger } from "@/common"
import { stat } from "fs"

const logger = Logger.get("mutations.js")

export default {
    setLogin(state, { userID, token }) {
        logger.debug("Set userID:", userID, "token:", token)
        state.userID = userID
        state.token = token
        if (window.localStorage) {
            window.localStorage.setItem("chatroom_user_id", userID)
            window.localStorage.setItem("chatroom_token", token)
        }
    },

    clearLogin(state) {
        logger.debug("Clear Username")
        state.email = null
        state.token = null
        state.friends = null
        if (window.localStorage) {
            window.localStorage.removeItem("chatroom_user_id")
            window.localStorage.removeItem("chatroom_token")
        }
    },

    setFriendList(state, { friends }) {
        logger.debug("Set Friends:", friends)
        state.friends = friends
    },

    setInfo(state, { username }) {
        logger.debug("Get Person Info", name)
        state.username = username
    },

    setMsg(state, { messages }) {
        logger.debug("Set Message:", messages)
        state.messages = messages
    }
}
