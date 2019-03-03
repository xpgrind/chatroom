import io from "socket.io-client"
import { API_URL } from "@/api/server"

var socket = io(API_URL, {transports: ['websocket']})

export default socket
