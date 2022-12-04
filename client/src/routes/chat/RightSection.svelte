<script>
import { onMount } from "svelte";
import { io } from "socket.io-client";

import { allMsgs, room_id, roomMsgs, user_id } from "$lib/stores";

import Message from "./Message.svelte";
import MessageInput from "./MessageInput.svelte";

const namespace = "localhost:5000";
const transports = {transports: ["websocket"]}
let socket;  // Forward declare socket :)


onMount(async () => {
  // SocketIO instance
  socket = io(namespace, transports);

  socket.on("connect", async () => {
    console.log("connected to SocketIO server"); // TODO(SpeedFox198): remove this later lmao
    await joinRoom(); // TODO(SpeedFox198): remove this later lmao
  })

  socket.on("receive_message", async (data, cb) => {
    await addMsg(data.room_id, true, data.username, data.avatar, data.time, data.content);
    if (cb) await cb();
  });
});


async function sendMsg(event) {
  let content = event.detail;
  await socket.emit("send_message", {
    $room_id,
    $user_id,
    time: "99:99PM", // prob use unix time here
    content,
    reply_to: null, // reply_to
    type: "text" // <type> ENUM(image, document, video, text)
  });
  await addMsg(false, $room_id, "Me", "/galaxy.jpg", "99:99PM", content);
}

async function addMsg(received, room_id, username, avatar, time, content) {
  let msg = {received, username, avatar, time, content};
  await allMsgs.addMsg(msg, room_id);
}

async function joinRoom() {
  await socket.emit("begin_chat", $room_id); // TODO(SpeedFox198): room_id? really?
  console.log(`Joined room ${$room_id}`); // TODO(SpeedFox198): remove this later lol
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
    <div class="chat">
      <div class="my-2"></div>
      {#each $roomMsgs as msg}
        <Message msg={msg}/>
      {/each}
      <div id="anchor"></div>
    </div>

    <!-- Messages Display Section -->
    <MessageInput on:message={sendMsg}/>

  </div>
</div>


<style>
.temp { /*TODO(SpeedFox198): remove this extra temp style when not needed */
  height: 4rem;
}

.top-right {
  height: 4rem;
  width: calc(100vw - var(--left-bar-length));
  background-color: var(--primary);
  border-left: 0.1rem solid var(--primary-shadow);
}

/* .bottom-right {
} */

.chat {
  height: calc(100vh - 8rem);
  overflow-y: scroll;
  border-left: 0.1rem solid var(--grey);
}

#anchor {
  overflow-anchor: auto;
  height: 1rem;
}
</style>
