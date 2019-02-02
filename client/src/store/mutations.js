import Vue from "vue"
import { Logger } from "@/common"

const logger = Logger.get("mutations.js")

export default {
    setLogin(state, { useremail, token }) {
        logger.debug("Set Email:", useremail, "token", token)
        state.email = useremail
        state.token = token
        if (window.localStorage) {
            window.localStorage.setItem("chatroom_email", useremail)
            window.localStorage.setItem("chatroom_token", token)
        }
    },

    clearLogin(state) {
        logger.debug("Clear Username")
        state.email = null
        state.token = null
        state.friends = null
        if (window.localStorage) {
            window.localStorage.removeItem("chatroom_email")
            window.localStorage.removeItem("chatroom_token")
        }
    },

    setFriendList(state, { friends }) {
        logger.debug("Set Friends:", friends)
        state.friends = friends
        if (window.localStorage) {
            window.localStorage.setItem("chatroom_friends", friends)
        }
    },

    clearFriendList(state) {
        logger.debug("Clear Friends")
        state.friends = null
        if (window.localStorage) {
            window.localStorage.removeItem("chatroom_friends")
        }
    },
}
