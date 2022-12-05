<script>
import { onMount } from "svelte";
import { io } from "socket.io-client";

import { allMsgs, room_id, roomMsgs } from "$lib/stores/messages.js";
import { user_id, allUsers } from "$lib/stores/users.js";

import Message from "$lib/chat/message/Message.svelte";
import MessageInput from "./MessageInput.svelte";

const namespace = "https://localhost:8443";
const transports = {transports: ["websocket"]}
let socket;  // Forward declare socket :)
let rooms;

onMount(async () => {
  // SocketIO instance
  socket = io(namespace, transports);

  socket.on("connect", async () => {
    console.log("connected to SocketIO server"); // TODO(SpeedFox198): remove this later lmao
  })

  // Receive from server list of rooms that client belongs to
  socket.on("rooms_joined", async data => {
    rooms = data;
    console.log(rooms);
  })

  socket.on("receive_message", async (data, cb) => {
    await addMsg(data.room_id, "<user_id>", data.username, data.avatar, data.time, data.content);
    if (cb) await cb();
  });
});


async function sendMsg(event) {
  let content = event.detail;
  await socket.emit("send_message", {
    room_id: $room_id,
    user_id: $user_id,
    time: "99:99PM", // prob use unix time here
    content,
    reply_to: null, // reply_to
    type: "text" // <type> ENUM(image, document, video, text)
  });
  await addMsg($room_id, "<user_id>", "Me", "/galaxy.jpg", "99:99PM", content);
}

async function addMsg(room_id, user_id, username, avatar, time, content) {
  let msg = {user_id, username, avatar, time, content};
  await allMsgs.addMsg(msg, room_id);
}
</script>


<!-- Right Section -->
<div class="d-flex flex-column flex-grow-1 right-section">

  <!-- Room Info Section -->
  <div class="top-right">
    <div class="temp">

    </div>
  </div>

    <!-- Messages Display Section -->
    {#if $room_id}
      <div class="chat">
        <div class="my-2"></div>
        {#each $roomMsgs as msg}
          <Message msg={msg} sent={msg.user_id === $user_id}/>
        {/each}
        <div id="anchor"></div>
      </div>

      <!-- Messages Display Section -->
      <MessageInput on:message={sendMsg}/>
    {:else}
      <div class="">
        <!-- TODO(SpeedFox198): add welcome page? lol -->
      </div>
    {/if}
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

.chat {
  height: calc(100vh - 8rem);
  overflow-y: scroll;
  border-top: 0.1rem solid var(--grey-shadow);
  border-left: 0.1rem solid var(--grey-shadow);
}

#anchor {
  overflow-anchor: auto;
  height: 1rem;
}
</style>
