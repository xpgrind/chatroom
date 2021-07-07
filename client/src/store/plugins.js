import socket from "@/socket"
import { Logger } from "@/common"
const logger = Logger.get("Store/Plugins")

// tslint:disable-next-line:no-shadowed-variable
function createBasePlugin(socket) {
    return store => {
        socket.on("connect_info", message => {
            logger.debug("connect_info", {message})
        })

        socket.on("connect", message => {
            logger.debug("connect", {message})
        })

        socket.on("disconnect", message => {
            logger.debug("disconnect", {message})
        })

        socket.on("message/new", message => {
            logger.debug("got message/new", {message})
        })
    }
}

const basePlugin = createBasePlugin(socket)

export default [ basePlugin ]
