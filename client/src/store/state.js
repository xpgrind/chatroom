// tslint:disable:max-line-length
export default {
    username: window.localStorage.getItem("chatroom_username") || null,
    token: window.localStorage.getItem("chatroom_token") || null,
    friends: null,
    email: window.localStorage.getItem("chatroom_email") || null,
    // user_id: window.localStorage.getItem("chatroom_id") || null
}
