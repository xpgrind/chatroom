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

    addFriend({ state, commit, dispatch }, {newFriend}) {
        logger.debug("addFriend, state.user_id = ", state.userID)
        const url = API_URL + "/friends/add"
        return new Promise((resolve, reject) => {
            axios
                .post(url, { user_id: state.userID, token: state.token, new_friend: newFriend })
                .then(
                    (response) => { return response.data },
                    (error) => { console.log("Error!", error) }
                )
                .then(
                    json => {
                        logger.debug("Json data is:", json)
                        if (!json.success) {
                            reject(new Error(json.message))
                        } else {
                            logger.debug("Friend request sent")
                            console.log("Adding friend succeeded")
                            dispatch("loadFriendList")
                            resolve(json)
                        }
                    })
                .catch(error => {
                    logger.warn("Adding failed", error)
                    reject(error)
                })
        })
    },

    clearLogin({ commit }) {
        Vue.cookie.delete("token")
        commit("clearLogin")
    },

    clearFriends({ commit }) {
        Vue.cookie.delete("friend")
        commit("clearFriends")
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
                    resolve(json)
                })
                .catch(error => {
                    logger.warn("Check username failed", error)
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
    // uploadFile({ state, commit }, { path }) {
    //     const url = API_URL + "/check_path"
    //     return new Promise((resolve, reject) => {
    //         axios
    //             .post(url, { path })
    //             .then(
    //                 (reponse) => { return response.data },
    //             )
    //             .then(json => {
    //                 if (!json) {
    //                     reject(new Error("No reply from server"))
    //                 }
    //                 resolve(json)
    //             })
    //             .catch(error => {
    //                 logger.warn("Picture Path failed", error)
    //                 reject(error)
    //             })
    //     })
    // }
}
