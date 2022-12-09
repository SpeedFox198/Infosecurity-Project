<script>
import { onMount } from "svelte";
import { io } from "socket.io-client";

import { msgStorage, allMsgs, getTempId } from "$lib/stores/messages";
import { room_id, allRooms } from "$lib/stores/rooms";
import { user_id, allUsers } from "$lib/stores/users";

import Message from "$lib/chat/message/Message.svelte";
import MessageInput from "$lib/chat/message/MessageInput.svelte";

$: roomMsgs = $allMsgs[$room_id] || [];

const namespace = "https://localhost:8443";
const transports = { transports: ["websocket"] };
let socket;  // Forward declare socket :)

onMount(async () => {
  // SocketIO instance
  socket = io(namespace, transports);

  socket.on("connect", async () => {
    console.log("connected to SocketIO server"); // TODO(SpeedFox198): remove this later lmao
  });

  // Receive from server list of rooms that client belongs to
  socket.on("rooms_joined", async data => {
    allRooms.set(data);  // Set list of rooms
  });

  socket.on("receive_message", async data => {
    addMsg(data);
  });

  socket.on("receive_room_messages", async data => {
    msgStorage.updateMsg(data.message_id, data.room_messages);
    allMsgs.addMsg(data.message_id, data.room_id, true);
  });
});


// Send message to room via SocketIO
async function sendMsg(event) {
  const content = event.detail;
  const message_id = getTempId();  // Temporary id for referencing message
  const msg = {
    message_id,
    room_id: $room_id,
    user_id: $user_id,
    time: Math.floor(Date.now()/1000),
    content,
    // TODO(SpeedFox198): will we be doing "reply"? (rmb to search and replace all occurences)
    reply_to: null,
    type: "text" // <type> ENUM(image, document, video, text)
  };

  // Emit message to server and add message to client stores
  socket.emit("send_message", msg);
  addMsg(msg);
}

// Get latest 20n+1 to 20n+20 messages from room
async function getRoomMsgs(n) {
  socket.emit("get_room_messages", {
    room_id: $room_id,
    start: 20*n + 1,
    end: 20*n + 20
  });
}

async function getUser(user_id) {
  const url = `https://localhost:8443/api/user/${user_id}`;
  const response = await fetch(url);
  const { username, avatar, message } = await response.json();
  
  if (!response.ok) {
    throw new Error(message);
  }

  let user = { username, avatar };
  allUsers.addUser(user, user_id);

  return user;
}

async function addMsg(data) {
  // Unpacking values
  const { message_id, room_id, time, content, reply_to, type } = data;
  const user_id_ = data.user_id;
  const sent = user_id_ === $user_id;
  let user = $allUsers[user_id_];
  if (!user) user = await getUser(user_id_);
  const avatar = user.avatar;
  const username = user.username;
  const msg = { sent, username, avatar, time, content, reply_to, type };
  msgStorage.updateMsg(message_id, msg);
  allMsgs.addMsg(message_id, room_id);
}
</script>


<!-- Right Section -->
<div class="d-flex flex-column flex-grow-1 right-section">

  <!-- Room Info Section -->
  <div class="top-right">
    <div class="temp">

    </div>
  </div>

  {#if $room_id}
    <!-- Messages Display Section -->
    <div class="chat" on:scroll={()=>null}>
      <div class="my-2"></div>
      {#each roomMsgs as message_id}
        <Message msg={$msgStorage[message_id]}/>
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
.temp {  /*TODO(SpeedFox198): remove this extra temp style when not needed */
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
