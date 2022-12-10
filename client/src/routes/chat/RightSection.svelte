<script>
import { onMount } from "svelte";

import { msgStorage, allMsgs, getTempId } from "$lib/stores/message";
import { room_id, allRooms } from "$lib/stores/room";
import { user_id, allUsers } from "$lib/stores/user";
import { count } from "$lib/stores/count";

import MessageDisplay from "$lib/chat/message/MessageDisplay.svelte";
import MessageInput from "$lib/chat/message/MessageInput.svelte";


// SocketIO instance
export let socket;
export let getRoomMsgs;


onMount(async () => {
  // Receive from server list of rooms that client belongs to
  socket.on("rooms_joined", async data => {
    allRooms.set(data);  // Set list of rooms
    allMsgs.initRooms(data)  // Initialise empty arrays for rooms
  });


  socket.on("receive_message", async data => {
    count.nextExtra(data.room_id);  // Increase count of received messages
    addMsg(data);                   // Add message to storage
  });


  socket.on("sent_success", async data => {
    const { message_id, temp_id, time, room_id } = data;  // Unpack data

    count.nextExtra(room_id);  // Increase count of sent messages

    // Update time and temp_id to message_id for both msgStorage and allMsgs
    await msgStorage.changeId(temp_id, message_id, time);
    await allMsgs.changeId(temp_id, message_id, room_id);
  });


  socket.on("receive_room_messages", addMsgBatch);
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
  await addMsg(msg);
  socket.emit("send_message", msg);
}


async function getUser(user_id) {
  const url = `https://localhost:8443/api/user/${user_id}`;
  let user;

  try {
    const response = await fetch(url);
    const { username, avatar, message } = await response.json();
    
    if (!response.ok) {
      throw new Error(message);
    }
  
    user = { username, avatar };
    allUsers.addUser(user, user_id);

  } catch (error) {
    console.error(error);
    // TODO(SpeedFox198): if default not there anymore change the default pic to something else
    user = { username:"<error>", avatar:"/default.png" };
  }

  return user;
}


async function addMsg(data) {
  const { message_id, msg, room_id } = await formatMsg(data);

  await msgStorage.updateMsg(msg, message_id);
  await allMsgs.addMsg(message_id, room_id);
}


async function addMsgBatch(data) {
  let message_ids = [];
  let room_messages = {};
  let msg, message_id;

  // Go through messages and format them for display in JavaScript
  for (let i=0; i < data.room_messages.length; i++) {
    // Get message and message_id
    ({ msg, message_id } = await formatMsg(data.room_messages[i]));
    message_ids.push(message_id);         // Add message_id to list
    delete msg.message_id;        // Remove message_id property from message
    room_messages[message_id] = msg;      // Add message to object
  }

  // Store the messages in stores
  await msgStorage.updateMsg(room_messages);
  await allMsgs.addMsg(message_ids, data.room_id, true);
}


async function formatMsg(data) {
  const { message_id, room_id, time, content, reply_to, type } = data;
  const user_id_ = data.user_id;
  const sent = user_id_ === $user_id;
  let user = $allUsers[user_id_];
  if (!user) user = await getUser(user_id_);
  const avatar = user.avatar;
  const username = user.username;
  const msg = { sent, username, avatar, time, content, reply_to, type };

  return { message_id, msg, room_id };
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
    <MessageDisplay/>

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
</style>
