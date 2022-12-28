<script>
import { onMount } from "svelte";
import { page } from "$app/stores"

import { msgStorage, allMsgs, getTempId } from "$lib/stores/message";
import { room_id, roomStorage, roomList } from "$lib/stores/room";
import { user_id, allUsers } from "$lib/stores/user";
import { count } from "$lib/stores/count";
import { lockScroll } from "$lib/stores/scroll";
import { selectMode } from "$lib/stores/select";
import { cleanSensitiveMessage } from "$lib/chat/message/data-masking";

import MessageDisplay from "$lib/chat/message/MessageDisplay.svelte";
import MessageInput from "$lib/chat/message/MessageInput.svelte";
import SelectMenu from "$lib/chat/message/SelectMenu.svelte";


// SocketIO instance
export let socket;
export let getRoomMsgs;

let currentUser = $page.data.user

onMount(async () => {
  // Receive from server list of rooms that client belongs to
  socket.on("rooms_joined", async data => {

    let room, room_id;
    let newRoomList = [];
    let newroomStorage = {};

    for (let i=0; i < data.length; i++) {
      room = data[i];
      room_id = room.room_id;
      newRoomList.push(room_id);
      newroomStorage[room_id] = room;
    }

    // Initialise rooms
    roomList.set(newRoomList);           // Set list of room_id
    roomStorage.set(newroomStorage);     // Set collection of rooms
    allMsgs.initRooms(newRoomList)       // Initialise empty arrays for rooms
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


  socket.on("message_deleted", async data => {
    const room_id = data.room_id;
    let roomCount = $count[room_id];

    // If room is not laoded yet, end deletion (no message for deleting)
    if (!roomCount || roomCount.n === 0) return;

    // Delete every message in list
    let message_id;
    let countRemoved = 0;
    for (let i=0; i < data.messages.length; i++) {
      message_id = data.messages[i];
      
      // Remove message from storage
      countRemoved += await removeMsg(message_id, room_id);
    }

    count.decreaseExtra(room_id, countRemoved);
  });
});


// Send message to room via SocketIO
async function sendMsg(event) {
  let content = event.detail;
  let messageChanged = false;

  if (currentUser.censor) {
    ({ content, messageChanged } = await cleanSensitiveMessage(content));
  }

  const message_id = getTempId();  // Temporary id for referencing message
  const msg = {
    message_id,
    user_id: $user_id,
    room_id: $room_id,
    time: Math.floor(Date.now()/1000),
    content,
    // TODO(low)(SpeedFox198): will we be doing "reply"? (rmb to search and replace all occurences)
    reply_to: null,
    type: "text" // <type> ENUM(image, document, video, text)
  };

  // TODO(high)(SpeedFox198): implement ui for message is masked
  if (messageChanged) {
    console.log("YOUR SENSITIVE DATA HAS BEEN LEAKED BOZO");
  }

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
    // TODO(low)(SpeedFox198): if default not there anymore change the default pic to something else
    user = { username:"<error>", avatar:"/default.png" };
  }

  return user;
}


async function addMsg(data) {
  const roomMsgs = $allMsgs[data.room_id] || [];
  let prevInfo, prev_id;
  if (roomMsgs.length) {
    prevInfo = roomMsgs[roomMsgs.length - 1];
    prev_id = prevInfo.user_id;
  }

  const { user_id_, message_id, msg, room_id } = await formatMsg(data, prev_id);

  if (prev_id === user_id_) {
    let prevMsg = $msgStorage[prevInfo.message_id];
    delete prevMsg.corner;
    await msgStorage.updateMsg(prevMsg, prevInfo.message_id);
  }

  await msgStorage.updateMsg(msg, message_id);
  await allMsgs.addMsg({ user_id: user_id_, message_id }, room_id);
}


async function addMsgBatch(data) {
  let messageInfoList = [];
  let room_messages = {};
  let msg, message_id, user_id_, prevMsg, prev_id;

  // Go through messages and format them for display in JavaScript
  for (let i=0; i < data.room_messages.length; i++) {
    // Get message and message_id
    ({ msg, message_id, user_id_ } = await formatMsg(data.room_messages[i], prev_id));
    messageInfoList.push({user_id: user_id_, message_id});   // Add message_id to list
    delete msg.message_id;                          // Remove message_id property from message
    room_messages[message_id] = msg;                // Add message to object
    if (prev_id === user_id_) delete prevMsg.corner;// Delete corner if not consecutive message 
    prevMsg = msg;
    prev_id = user_id_;
  }

  // Update current most top message accordingly
  let msgInfo = ($allMsgs[data.room_id] || [])[0];
  if (msgInfo && msgInfo.user_id == prev_id) {
    msg = $msgStorage[msgInfo.message_id];
    delete msg.username;
    delete msg.avatar;
    delete prevMsg.corner;
    msgStorage.updateMsg(msg, msgInfo.message_id);
  }

  // Store the messages in stores
  await msgStorage.updateMsg(room_messages);
  lockScroll.unlock();
  await allMsgs.addMsg(messageInfoList, data.room_id, true);
  lockScroll.lock();
}


async function formatMsg(data, prev_id) {
  const { message_id, room_id, time, content, reply_to, type } = data;
  const user_id_ = data.user_id;
  const sent = user_id_ === $user_id;
  const corner = true;  // For styling corner of last consecutive message
  let msg;

  // Check if previous message is sent by same user
  if (prev_id && prev_id === user_id_){
    
    // Continuous messages have no avatar
    msg = { sent, time, content, reply_to, type, corner };

  } else {
    
    // New message from user has avatar and username
    let user = $allUsers[user_id_];
    if (!user) user = await getUser(user_id_);
    const avatar = user.avatar;
    const username = user.username;
 
    msg = { sent, username, avatar, time, content, reply_to, type, corner };

  }

  return { user_id_, message_id, msg, room_id };
}


async function deleteMsgs(event) {
  const data = event.detail;
  socket.emit("delete_messages", data);
}

// Removes message from storage and updates messages for UI, returns true if message removed
async function removeMsg(message_id, room_id) {
    // Delete and retrieve message from msgStorage
    const msg = await msgStorage.deleteMsg(message_id);

    // If message not in storage, skip deletion (nothing to delete)
    if (!msg) return 0;

    // Delete and retrieve message index in list
    const { index, user_id } = await allMsgs.deleteMsg(room_id, message_id);

    // Only continue deletion if message was found (a check just in case)
    if (index <= -1) return 0;


    // Get info of previous and next messages
    const roomMsgs = $allMsgs[room_id];
    const nextInfo = roomMsgs[index];
    const prevInfo = roomMsgs[index-1];

    // If message has avatar, add avatar to next message
    if (msg.avatar) {

      // If next message is sent by same user
      if (nextInfo && nextInfo.user_id == user_id) {
        let nextMsg = $msgStorage[nextInfo.message_id];
        nextMsg.username = msg.username;
        nextMsg.avatar = msg.avatar;
        msgStorage.updateMsg(nextMsg, nextInfo.message_id);
      }
    }

    // If message is last of continuos, add rounded corner to previous message
    if (msg.corner) {

      // If previous message is sent by same user
      if (prevInfo && prevInfo.user_id == user_id) {
        let prevMsg = $msgStorage[prevInfo.message_id];
        prevMsg.corner = true;
        msgStorage.updateMsg(prevMsg, prevInfo.message_id);
      }
    }

    // If previous and next messages are sent by same person merge formats
    if (msg.corner) {

      // If previous message is sent by same user
      if (prevInfo && nextInfo && prevInfo.user_id == nextInfo.user_id) {
        let prevMsg = $msgStorage[prevInfo.message_id];
        let nextMsg = $msgStorage[nextInfo.message_id];
        delete prevMsg.corner
        delete nextMsg.username
        delete nextMsg.avatar
        msgStorage.updateMsg(prevMsg, prevInfo.message_id);
        msgStorage.updateMsg(nextMsg, nextInfo.message_id);
      }
    }

    return 1;
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
    <MessageDisplay {getRoomMsgs}/>

    {#if $selectMode}
      <!-- Select Menu -->
      <SelectMenu on:delete={deleteMsgs}/>
    {:else}
      <!-- Messages Display Section -->
      <MessageInput on:message={sendMsg}/>
    {/if}
  {:else}
    <div class="">
      <!-- TODO(UI)(SpeedFox198): add welcome page? lol -->
    </div>
  {/if}
</div>


<style>
.temp {  /*TODO(UI)(SpeedFox198): remove this extra temp style when not needed */
  height: 4rem;
}

.top-right {
  height: 4rem;
  width: calc(100vw - var(--left-bar-length));
  background-color: var(--primary);
  border-left: 0.1rem solid var(--primary-shadow);
}
</style>
