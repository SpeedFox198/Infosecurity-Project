<script>
import { onMount } from "svelte";
import { io } from "socket.io-client";

import { allMsgs, roomMsgs } from "$lib/stores/messages";
import { room_id, allRooms } from "$lib/stores/rooms";
import { user_id, allUsers } from "$lib/stores/users";

import Message from "$lib/chat/message/Message.svelte";
import MessageInput from "$lib/chat/message/MessageInput.svelte";

const namespace = "https://localhost:8443";
const transports = { transports: ["websocket"] }
let socket;  // Forward declare socket :)

onMount(async () => {
  // TODO(SpeedFox198): remove this temp function lmao (and the alert is annoying lol)
  (async () => {
    const x = prompt("Enter username:", "bob");
    if (x == "bob") {
      user_id.set("2a3f14df-ef17-4410-baf9-ed6693ac8c5a");
    }
    else {
      user_id.set("ac4528d0-98f3-41a3-9516-03381f76c374");
    }
  })();

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
    addMsg(data.room_id, data.user_id, data.time, data.content);
  });

  socket.on("receive_room_messages", async data => {
    allMsgs.addMsg(data.room_messages, data.room_id, true);
  });
});


// Send message to room via SocketIO
async function sendMsg(event) {
  let content = event.detail;
  socket.emit("send_message", {
    room_id: $room_id,
    user_id: $user_id,
    time: "99:99PM", // TODO(SpeedFox198): prob use unix time here
    content,
    reply_to: null, // reply_to
    type: "text" // <type> ENUM(image, document, video, text)
  });
  addMsg($room_id, $user_id, "99:99PM", content);
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
  const url = `https://localhost:8443/api/user?user_id=${user_id}`;
  const response = await fetch(url);
  const { username, avatar, message } = await response.json();

  let user = { username, avatar };

  if (response.ok) {
    allUsers.addUser(user, user_id);
  }
  else {
    throw new Error(message);
  }

  return user;
}

async function addMsg(room_id, user_id_, time, content) {
  const sent = user_id_ === $user_id;
  let user = $allUsers[user_id_];
  if (!user) user = await getUser(user_id_);
  const avatar = user.avatar;
  const username = user.username;
  const msg = {sent, username, avatar, time, content};
  allMsgs.addMsg(msg, room_id);
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
      {#each $roomMsgs as msg}
        <Message msg={msg}/>
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
