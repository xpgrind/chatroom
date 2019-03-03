import Vue from "vue"
import axios from "axios"
import { API_URL } from "@/api/server"
import { Logger } from "@/common"

const logger = Logger.get("actions.js")

export default {
    attemptLogin({ commit }, { email, password }) {
        logger.debug("Logging in with email", email, "password", password)
        const url = API_URL + "/login"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { email, password }, { withCredentials: true })
                .then(
                    (response) => {
                        // logger.debug("Login Response: ", response)
                        return response.data
                    }
                )
                .then(json => {
                    logger.debug("Successfully logged in", json)
                    commit("setLogin", { userID: json.user_id, token: json.token })
                    resolve()
                })
                .catch(error => {
                    // logger.warn("Error 1: Login Failed", error.response)
                    commit("clearLogin")
                    reject(error)
                })
        })
    },

    loadFriendList({ state, commit }) {
        logger.debug("Loading friend list")
        const url = API_URL + "/friends/list"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { user_id: state.userID, token: state.token })
                .then(
                    (response) => { return response.data },
                    (error) => { console.log("Error!", error) }
                )
                .then(
                    json => {
                        console.log("Loading friend succeeded")
                        commit("setFriendList", {friends: json.friends})
                        resolve(json)
                    })
        })
    },

    loadUserInfo({ state, commit }) {
        logger.debug("Loading User Info")
        const url = API_URL + "/get_info"
        axios
            .post(url, { user_id: state.userID, token: state.token })
            .then(
                (response) => { return response.data },
            )
            .then(
                json => {
                    console.log("Getting Info succeeded")
                    commit("setInfo", {username: json.username, photo: json.photo})
                }
            // eslint-disable-next-line
            ).catch(error => {
                logger.debug("loadUserInfo failed")
            })
    },

    addFriend({ state, dispatch }, {newFriend}) {
        logger.debug("addFriend, state.user_id = ", state.userID)
        const url = API_URL + "/friends/add"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { user_id: state.userID, token: state.token, new_friend: newFriend })
                .then(
                    (response) => { return response.data },
                    (error) => {
                        console.log("Error!", error.response)
                        logger.debug("addFriend returning error:", error, "reponse is", error.response)
                        reject(error)
                    }
                )
                .then(
                    json => {
                        logger.debug("addFriend returning success:, json is", json)
                        dispatch("loadFriendList")
                        resolve(json)
                    }
                )
        })
    },

    clearLogin({ commit }) {
        commit("clearLogin")
    },

    deleteFriend({ state, commit, dispatch }, {friend}) {
        logger.debug("deleteFriend, state.user_id = ", state.userID)
        const url = API_URL + "/friends/delete"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { user_id: state.userID, token: state.token, friend: friend })
                .then(
                    (response) => { return response.data },
                    (error) => {
                        console.log("Error!", error.response)
                        logger.debug("deleteFriend returning error:", error, "reponse is", error.response)
                        reject(error)
                    }
                )
                .then(
                    json => {
                        logger.debug("deleteFriend returning success:, json is", json)
                        dispatch("loadFriendList")
                        resolve(json)
                    }
                )
        })
    },

    sendMsg ({ state, commit, dispatch }, { newMsg, receiver, clientTime }) {
        logger.debug("send message ", state.userID)
        const url = API_URL + "/send_msg"
        axios
            .post(url, { user_id: state.userID, token: state.token, message: newMsg, receiver: receiver, client_time: clientTime })
            .then(
                (response) => { return response.data },
                (error) => {
                    console.log("Error!", error.response)
                    logger.debug("Sending Message returning error:", error, "reponse is", error.response)
                }
            )
            .then(
                json => {
                    logger.debug("sending message returning success:, json is", json)
                }
            )
    },

    registerUser(vueParams, { newEmail, newUsername, newPassword }) {
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
                        reject(error)
                    }
                )
                .then(
                    json => {
                        if (!json) {
                            reject(new Error("No Reply from server"))
                        }
                        if (json.success) {
                            console.log("Register connection succeeded")
                            resolve()
                        } else {
                            reject(new Error(json.message))
                        }
                    })
                .catch(error => {
                    logger.warn("Registration connection failed", error)
                    reject(error)
                })
        })
    },

    checkUsername(vueArgs, { newUsername }) {
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
                    resolve(json)
                })
                .catch(error => {
                    logger.warn("Check username failed", error)
                    reject(error)
                })
        })
    },

    checkEmail(vueArgs, { newEmail }) {
        console.log("actions.js: Email is " + newEmail)
        const url = API_URL + "/check_email"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { newEmail })
                .then(
                    (response) => { return response.data },
                )
                .then(json => {
                    if (!json) {
                        reject(new Error("No reply from server"))
                    }
                    resolve(json)
                })
                .catch(error => {
                    logger.warn("Check email failed", error)
                    reject(error)
                })
        })
    },
    uploadPhoto({ state, commit }, { path }) {
        const url = API_URL + "/upload_photo"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { user_id: state.userID, token: state.token, path })
                .then(
                    (response) => { return response.data },
                )
                .then(json => {
                    if (!json) {
                        reject(new Error("No reply from server"))
                    }
                    resolve(json)
                })
                .catch(error => {
                    logger.warn("Picture Path failed", error)
                    reject(error)
                })
        })
    }
}
