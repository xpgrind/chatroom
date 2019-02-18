// tslint:disable:max-line-length
function loadUserID() {
    const userIDStr = window.localStorage.getItem("chatroom_user_id")
    if (userIDStr === null || userIDStr === undefined) {
        return null
    }
    const parsedUserID = parseInt(userIDStr)
    if (isNaN(parseInt(parsedUserID))) {
        return null
    }
    return parsedUserID
}

export default {
    username: '',
    friends: [],
    token: window.localStorage.getItem("chatroom_token") || null,
    userID: loadUserID(),
    photo: ''
}
