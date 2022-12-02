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

  socket.on("response", async (msg, cb) => {
    await addMsg(true, "Someone", "/default.png", "99:99PM", msg.data);
    if (cb) cb();
  });
});

async function sendMsg(event) {
  let content = event.detail;
  socket.emit("test", {data: content});
  await addMsg(false, "Me", "/galaxy.jpg", "99:99PM", content);
}

async function addMsg(received, username, avatar, time, content) {
  allMsgs.push({
    received: received,
    username: username,
    avatar: avatar,
    time: time,
    content: content,
  });
  allMsgs = allMsgs;
}

</script>


<!-- Right Section -->
<div class="d-flex flex-column flex-grow-1 right-section">

  <!-- Room Info Section -->
  <div class="top-right">
    <div class="temp">

    </div>
  </div>

  <div class="d-flex flex-column bottom-right">

    <!-- Messages Display Section -->
    <MessageDisplay allMsgs={allMsgs}/>

    <!-- Messages Display Section -->
    <MessageInput on:message={sendMsg}/>

  </div>
</div>


<style>

.temp {
  height: 4rem;
}

.top-right {
  /* position: absolute;
  top: 0; */
  height: 4rem;
  width: calc(100vw - var(--left-bar-length));
  background-color: var(--primary);
  border-left: 0.1rem solid var(--primary-shadow);
}

/* .bottom-right {
} */
</style>
