// tslint:disable:max-line-length
export default {
    username: null,
    friends: [],

    token: window.localStorage.getItem("chatroom_token") || null,
    userID: window.localStorage.getItem("chatroom_user_id") || null,
}
