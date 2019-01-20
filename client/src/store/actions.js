import Vue from "vue"
import axios from "axios"
import {API_URL} from "@/api/server"
import { Logger } from "@/common"

const logger = Logger.get("actions.js")

export default {
    attemptLogin({ commit }, { username, password }) {
        logger.debug("Logging in with username", username, "password", password)
        const url = API_URL + "/login"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { username, password }, { withCredentials: true })
                .then(response => {
                    return response.data
                })
                .then(json => {
                    logger.debug("Successfully logged in")
                    commit("setLogin", { username, token: json.token }) // commit goes to mutations.js
                    resolve()
                })
                .catch(error => {
                    logger.warn("Login Failed", error)
                    commit("clearLogin")
                    reject(error.response.data)
                })
        })
    },

    loadFriendList({ state, commit }) {
        const url = API_URL + "/friends"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { username: state.username, token: state.token })
                .then(
                    (response) => { return response.data },
                    (error) => { console.log("Error!", error) },
                )
                .then(json => {
                    logger.debug("loadFriendList succeeded")
                    commit("setFriendList", {friends: json.friends})
                    resolve()
                })
                .catch(error => {
                    logger.warn("loadFriendList failed", error)
                    reject(error.response.data)
                })
        })
    },

    clearLogin({ commit }) {
        Vue.cookie.delete("token")
        commit("clearLogin")
    },

    registerUser({ state, commit }, { newEmail, newUsername, newPassword }) {
        const url = API_URL + "/register_submit"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { newEmail, newUsername, newPassword })
                .then(
                    (response) => {
                        console.log("Register Response: ", response)
                        return response.data
                    },
                    (error) => {
                        console.log("Register Error!", error)
                    },
                )
                .then(json => {
                    if (!json) {
                        reject(new Error("No reply from server"))
                    }
                    if (json.available) {
                        console.log("Register connection succeeded")
                        resolve(json)
                    } else {
                        reject(new Error("Registration failed"))
                    }
                })
                .catch(error => {
                    logger.warn("registration connection failed", error)
                    reject(error)
                })
        })
    },

    checkUsername({ state, commit }, { newUsername }) {
        const url = API_URL + "/check_username"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { newUsername })
                .then(
                    (response) => { return response.data },
                    (error) => { console.log("Error!", error) },
                )
                .then(json => {
                    if (!json) {
                        reject(new Error("No reply from server"))
                    }
                    if (json.available) {
                        resolve()
                    } else {
                        reject(new Error("Username not available"))
                    }
                })
                .catch(error => {
                    logger.warn("check username failed", error)
                    reject(error)
                })
        })
    },

    checkEmail({ state, commit }, { newEmail }) {
        const url = API_URL + "/check_email"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { newEmail })
                .then(
                    (response) => { return response.data },
                    (error) => { console.log("Error!", error) },
                )
                .then(json => {
                    if (!json) {
                        reject(new Error("No reply from server"))
                    }
                    if (json.available) {
                        resolve()
                    } else {
                        reject(new Error("Email not available"))
                    }
                })
                .catch(error => {
                    logger.warn("Check email failed", error)
                    reject(error)
                })
        })
    }
}
