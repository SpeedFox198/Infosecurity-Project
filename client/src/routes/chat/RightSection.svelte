<script>
import MessageDisplay from "./MessageDisplay.svelte";
import MessageInput from "./MessageInput.svelte";
import { onMount } from "svelte";
import { io } from "socket.io-client";


const namespace = "localhost:5000";
const transports = {transports: ["websocket"]}
let allMsgs = [];
let socket;


onMount(async () => {
  // SocketIO instance
  socket = io(namespace, transports);

  socket.on("connect", () => {
    socket.emit("test", {data: "connected to the SocketServer..."});
  })

  socket.on("response", (msg, cb) => {
    allMsgs.push("from socketio server: " + msg.data);
    allMsgs = allMsgs;
    if (cb) cb();
  });
});

async function sendMsg(event) {
  let content = event.detail;
  socket.emit("test", {data: content});
  allMsgs.push("Sent via socketio: " + content);
  allMsgs = allMsgs;
}

</script>


<!-- Right Section -->
<div class="d-flex flex-column flex-grow-1 right-section">

  <!-- Room Info Section -->
  <div class="d-flex top-right">

  </div>

  <div class="d-flex flex-column bottom-right">

    <!-- Messages Display Section -->
    <MessageDisplay allMsgs={allMsgs}/>

    <!-- Messages Display Section -->
    <MessageInput on:message={sendMsg}/>

  </div>
</div>


<style>
.top-right {
  height: 4rem;
  border-top: 0.1rem solid var(--primary-shadow);
  border-right: 0.1rem solid var(--primary-shadow);
  background-color: var(--primary);
}

.bottom-right {
  height: 100%;
  border-right: 0.1rem solid var(--grey);
}
</style>
    