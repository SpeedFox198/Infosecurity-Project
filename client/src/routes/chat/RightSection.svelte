<script>
import { onMount } from "svelte";

import { msgStorage, allMsgs, getTempId } from "$lib/stores/message";
import { room_id, allRooms } from "$lib/stores/room";
import { user_id, allUsers } from "$lib/stores/user";
import { count } from "$lib/stores/count";
import { lockScroll } from "$lib/stores/scroll";
import { selectMode } from "$lib/stores/select";

import MessageDisplay from "$lib/chat/message/MessageDisplay.svelte";
import MessageInput from "$lib/chat/message/MessageInput.svelte";
import SelectMenu from "$lib/chat/message/SelectMenu.svelte";


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

// TODO(SpeedFox198): continue here
  socket.on("message_deleted", async data => {
    // Decrease extra counter for room by number of messages deleted
    // If n was 0 stop proccess (cuz no msg loaded, no nid delete)
    // TODO(SpeedFox198): consider reverting count minusExtra function's weird syntax
    // Remove message_id from msgStorage
    // Remove messsage from allMsgs in room_id
      // consider diff function
      // for every msg
        // get message index in list
        // if message is head message, change next message to head
    // TODO(SpeedFox198): consider doing the UI first before doing these

    // Just gonan write here cuz why not:
    // When adding new messages: (func1)
      // If prev diff user_id, add msg as head message
      // else, add msg is smol msg
    // When adding old msgs:
      // for each message
        // perform *func1 on list of old msg
        // check last old msg in list, compare with existing first msg
        // if same user_id
          // old -> head
          // first -> smol
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
  const roomMsgs = $allMsgs[data.room_id] || [];
  let prev_id;
  if (roomMsgs.length) prev_id = roomMsgs[roomMsgs.length - 1].user_id_;
  const { user_id_, message_id, msg, room_id } = await formatMsg(data, prev_id);

  await msgStorage.updateMsg(msg, message_id);
  await allMsgs.addMsg({ user_id_, message_id }, room_id);
}


async function addMsgBatch(data) {
  let messageInfoList = [];
  let room_messages = {};
  let msg, message_id, user_id_, prev_id;

  // Go through messages and format them for display in JavaScript
  for (let i=0; i < data.room_messages.length; i++) {
    // Get message and message_id
    ({ msg, message_id, user_id_ } = await formatMsg(data.room_messages[i], prev_id));
    messageInfoList.push({user_id_, message_id});// Add message_id to list
    delete msg.message_id;                       // Remove message_id property from message
    room_messages[message_id] = msg;             // Add message to object
    prev_id = user_id_;
  }

  // Update current most top message accordingly
  let msgInfo = ($allMsgs[data.room_id] || [])[0];
  if (msgInfo && msgInfo.user_id_ == prev_id) {
    console.log(msgInfo.message_id)
    msg = $msgStorage[msgInfo.message_id];
    delete msg.username;
    delete msg.avatar;
    msgStorage.updateMsg(msg, msgInfo.message_id);
  }

  // Store the messages in stores
  await msgStorage.updateMsg(room_messages);
  lockScroll.unlock();
  await allMsgs.addMsg(messageInfoList, data.room_id, true);
  lockScroll.lock();
  console.log($msgStorage)
}


async function formatMsg(data, prev_id) {
  const { message_id, room_id, time, content, reply_to, type } = data;
  const user_id_ = data.user_id;
  const sent = user_id_ === $user_id;
  let msg;

  // Check if previous message is sent by same user
  if (prev_id && prev_id === user_id_){
    
    // Continuous messages have no avatar
    msg = { sent, time, content, reply_to, type };
    
  } else {
    
    // New message from user has avatar and username
    let user = $allUsers[user_id_];
    if (!user) user = await getUser(user_id_);
    const avatar = user.avatar;
    const username = user.username;
 
    msg = { sent, username, avatar, time, content, reply_to, type };

  }

  return { user_id_, message_id, msg, room_id };
}


async function deleteMsgs(event) {
  const data = event.detail;
  socket.emit("delete_messages", data);
}

async function removeMsgs(data) {

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
    <MessageDisplay getRoomMsgs={getRoomMsgs}/>

    {#if $selectMode}
      <!-- Select Menu -->
      <SelectMenu on:delete={deleteMsgs}/>
    {:else}
      <!-- Messages Display Section -->
      <MessageInput on:message={sendMsg}/>
    {/if}
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
