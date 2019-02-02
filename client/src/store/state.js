// tslint:disable:max-line-length
export default {
    username: window.localStorage.getItem("chatroom_username") || null,
    token: window.localStorage.getItem("chatroom_token") || null,
    friends: window.localStorage.getItem("chatroom_friends") || null,
    email: window.localStorage.getItem("chatroom_email") || null,
}
