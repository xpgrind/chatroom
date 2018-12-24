import {socket} from "../api/socket"
import { Logger } from "@/common"
const logger = Logger.get("store/plugins")

// tslint:disable-next-line:no-shadowed-variable
function createBasePlugin(socket) {
  return store => {
    socket.on("connect_info", message => {
      logger.debug("connect_info", {message})
      store.dispatch("restoreLoginFull", { token: message.token, info: message.info })
    })

    socket.on("connect", message => {
      logger.debug("connect", {message})
      store.dispatch("socketConnected", { connected: true, message })
    })

    socket.on("disconnect", message => {
      logger.debug("disconnect", {message})
      store.dispatch("socketConnected", { connected: false, message })
    })
  }
}

const basePlugin = createBasePlugin(socket)

export default [ basePlugin ]
