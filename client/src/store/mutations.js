import Vue from "vue"

export default {
  setConnected(state, { connected }) {
    state.socketConnected = connected
  },

  setLogin(state, { token, info }) {
    state.loginSession.token = token
    state.loginSession.info = info
    if (window.localStorage && token) {
      window.localStorage.setItem('token', token)
    }
  },

  clearLogin(state) {
    state.loginSession.token = null
    state.loginSession.info = null
    if (window.localStorage) {
      window.localStorage.removeItem("token")
    }
  },
}
