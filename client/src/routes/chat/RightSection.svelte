<script>
import { onMount, createEventDispatcher } from "svelte";
import { getFlash } from "sveltekit-flash-message/client";
import { page } from "$app/stores"

import { msgStorage, allMsgs, getTempId } from "$lib/stores/message";
import { room_id, roomStorage, roomList } from "$lib/stores/room";
import { user_id, allUsers } from "$lib/stores/user";
import { count } from "$lib/stores/count";
import { lockScroll } from "$lib/stores/scroll";
import { selectedMsgs, selectMode } from "$lib/stores/select";
import { cleanSensitiveMessage, detectSensitiveImage } from "$lib/chat/message/sensitive-detection";

import Welcome from "$lib/chat/Welcome.svelte";
import ChatInfo from "$lib/chat/info/ChatInfo.svelte";
import MessageDisplay from "$lib/chat/message/MessageDisplay.svelte";
import MessageInput from "$lib/chat/message/MessageInput.svelte";
import SelectMenu from "$lib/chat/message/SelectMenu.svelte";
import E2EE, { encryption } from "$lib/e2ee/E2EE.svelte";
import OpenCV, { processImage } from "$lib/opencv/OpenCV.svelte"

// SocketIO instance
export let socket;
export let getRoomMsgs;
export let animateHideChatDetails;
export let displayChatDetails;
export let openChatDetails;

$: hideChatDetails = animateHideChatDetails && !displayChatDetails;

const SEPARATOR = ";";
const dispatch = createEventDispatcher();
const flash = getFlash(page)

let currentUser = $page.data.user
let roomsLoaded = false;
let ocrLoading = false;
/** @type {HTMLImageElement} */
let openCvImage;
/** @type {HTMLCanvasElement} */
let openCvCanvas;

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
    allMsgs.initRooms(newRoomList);      // Initialise empty arrays for rooms

    if (!roomsLoaded) {
      dispatch("load");
      roomsLoaded = true;
    }
  });


  socket.on("receive_message", async data => {
    count.nextExtra(data.room_id);  // Increase count of received messages
    addMsg(data);                   // Add message to storage
  });


  socket.on("sent_success", async data => {
    const { message_id, temp_id, time, room_id, filename, height, width } = data;  // Unpack data

    count.nextExtra(room_id);  // Increase count of sent messages

    // Update time and temp_id to message_id for both msgStorage and allMsgs
    await msgStorage.changeId(temp_id, message_id, room_id, time, filename, height, width);
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

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Send message to room via SocketIO
async function sendMsg(event) {
  let { content, file, type } = event.detail;
  let messageChanged = false;
  let isSensitiveImage = false;

  if (currentUser.censor) {
    ({ content, messageChanged } = await cleanSensitiveMessage(content));

    if (type === "image") {
      // TODO show message loading animation or something while sending
      ocrLoading = true
      const imageUrl = URL.createObjectURL(file)
      openCvImage.src = imageUrl
      
      await sleep(200) // Hacky way to let the image src set before processImage bc race condition
      
      await processImage(openCvImage, openCvCanvas)
      isSensitiveImage = await detectSensitiveImage(openCvCanvas);
      URL.revokeObjectURL(imageUrl)
      ocrLoading = false
    }
  }
  
  if (messageChanged) {
    $flash = {type: 'warning', message: `Your message has been masked as it contains sensitive data!`}
  }
  
  if (isSensitiveImage) {
    $flash = {type: 'failure', message: 'Your message was not sent as your image contains sensitive data!'}
    return
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
    type // <type> ENUM(image, document, video, text)
  };


  // Emit message to server and add message to client stores
  let filename = (file || {}).name;
  await addMsg(msg, filename);

  // Encrypt message before sending
  if ($roomStorage[$room_id].encrypted) {
    const encryptedContent = await encryption.encryptMessage(content);
    if (encryptedContent === undefined) {
      $flash = { type: "failure", message: "Please sign in to google to access end-to-end-encrypted chats!" };
      return;
    }
    msg.content = encryptedContent;

    // Encrypt file if exists
    if (file) {
      const { encrypted: encryptedFile, iv } = await encryption.encryptFile(file);
      file = encryptedFile;
      msg.content += SEPARATOR + iv;
    }
  }
  socket.emit("send_message", { message: msg, file, filename });
}

async function getUser(user_id) {
  const url = `https://localhost:8443/api/user/details/${user_id}`;
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


async function getMediaPath(room_id, message_id) {

  const url = `https://localhost:8443/api/media/filename/${message_id}`;
  const init = {
    method: "GET",
    credentials: "include",
  }
  let path, filename, height, width, message;

  try {
    const response = await fetch(url, init);
    ({ filename, height, width, message } = await response.json());

    if (!response.ok) {
      path = ""
      throw new Error(message);
    }

    path = `https://localhost:8443/api/media/attachments/${room_id}/${message_id}/${filename}`

  } catch (error) {
    console.error(error);
    // TODO(low)(SpeedFox198): if default not there anymore change the default pic to something else
    path = "";  // TODO(medium)(SpeedFox198): display default image if image not found
  }

  return { path, height, width };
}


async function addMsg(data, filename) {
  const roomMsgs = $allMsgs[data.room_id] || [];
  let prevInfo, prev_id;
  if (roomMsgs.length) {
    prevInfo = roomMsgs[roomMsgs.length - 1];
    prev_id = prevInfo.user_id;
  }

  if (filename) data.filename = filename;

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
    ({ msg, message_id, user_id_ } = await formatMsg(data.room_messages[i], prev_id, data.room_id));
    messageInfoList.push({ user_id: user_id_, message_id });   // Add message_id to list
    delete msg.message_id;                            // Remove message_id property from message
    room_messages[message_id] = msg;                  // Add message to object
    if (prev_id === user_id_) delete prevMsg.corner;  // Delete corner if not consecutive message 
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


async function formatMsg(data, prev_id, room_id_) {
  // parameter `room_id_` is optional, used when room_id is not in data
  const { message_id, room_id: room_id__, time, content, reply_to, type, filename, encrypted } = data;
  const room_id = room_id__ || room_id_
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

  if (encrypted) {
    msg.content = await encryption.decryptMessage(content);
  }

  // If message contains media, get media path
  if (type !== "text") {
    if (filename) {  // If filename is defined, means sent by user, display loading.gif
      msg.path = "/loading.gif";
    } else {
      ({ path: msg.path, height: msg.height, width: msg.width } = await getMediaPath(room_id, message_id));
      if (encrypted) {
        const iv = content.split(SEPARATOR)[2];
        if (type === "image") {
          getEncryptedImage(msg.path, message_id, iv);
          // msg.path = "/loading.gif";
        } else if (type === "document") {
          // TODO(high)(SpeedFox198): decrypt document?
        }
      }
    }
  }

  return { user_id_, message_id, msg, room_id };
}


async function getEncryptedImage(path, message_id, iv) {
  const file = await _getEncryptedFile(path, encryption.decryptImage, iv);
  const msg = $msgStorage[message_id];
  msg.path = URL.createObjectURL(file);
  msgStorage.updateMsg(msg, message_id);
}


async function _getEncryptedFile(path, decryptFunction, iv) {
  let content;
  try {
    const response = await fetch(path, { method: "POST", credentials: "include" });
    if (!response.ok) throw new Error(message);
    content = await response.blob();
  } catch (error) {
    console.error(error);
  }
  return await decryptFunction(content, iv);
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
    const { index, user_id: user_id_ } = await allMsgs.deleteMsg(room_id, message_id);

    // Only continue deletion if message was found (a check just in case)
    if (index <= -1) return 0;

    // Remove message from selected messages if message is selected
    selectedMsgs.remove(message_id, user_id_ === $user_id);

    // Get info of previous and next messages
    const roomMsgs = $allMsgs[room_id];
    const nextInfo = roomMsgs[index];
    const prevInfo = roomMsgs[index-1];

    // If message has avatar, add avatar to next message
    if (msg.avatar) {

      // If next message is sent by same user
      if (nextInfo && nextInfo.user_id == user_id_) {
        let nextMsg = $msgStorage[nextInfo.message_id];
        nextMsg.username = msg.username;
        nextMsg.avatar = msg.avatar;
        msgStorage.updateMsg(nextMsg, nextInfo.message_id);
      }
    }

    // If message is last of continuos, add rounded corner to previous message
    if (msg.corner) {

      // If previous message is sent by same user
      if (prevInfo && prevInfo.user_id == user_id_) {
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
<div class="d-flex flex-column right-section" class:displayChatDetails class:hideChatDetails>

  <!-- Chat Info Section -->
  <ChatInfo on:click={openChatDetails}/>

  <!-- Enable end-to-end-encryption if user has public key (meaning e2ee is enabled) -->
  {#if currentUser.public_key && currentUser.public_key.length > 0}
    <E2EE/>
  {/if}

  {#if $room_id}
    <!-- Messages Display Section -->
    <MessageDisplay {getRoomMsgs} {ocrLoading}/>

    {#if $selectMode}
      <!-- Select Menu -->
      <SelectMenu on:delete={deleteMsgs}/>
    {:else}
      <!-- Messages Display Section -->
      <MessageInput on:message={sendMsg}/>
    {/if}
  {:else}
    <!-- Welcome page -->
    <Welcome {currentUser}/>
  {/if}
  <OpenCV bind:openCv={openCvImage} bind:canvas={openCvCanvas} />
</div>


<style>
.right-section {
  width: calc(100vw - var(--side-bar-length));
  position: relative;
  overflow-y: hidden;
}

.displayChatDetails {
  width: calc(100vw - var(--side-bar-length)*2);
  -webkit-animation-name: display-chat-details;
  -webkit-animation-duration: 0.15s;
  animation-name: display-chat-details;
  animation-duration: 0.15s;
}

.hideChatDetails {
  width: calc(100vw - var(--side-bar-length));
  -webkit-animation-name: hide-chat-details;
  -webkit-animation-duration: 0.15s;
  animation-name: hide-chat-details;
  animation-duration: 0.15s;
}


/* Animations */
@-webkit-keyframes display-chat-details {
  from {
    width: calc(100vw - var(--side-bar-length));
  }
  to {
    width: calc(100vw - var(--side-bar-length)*2);
  }
}

@keyframes display-chat-details {
  from {
    width: calc(100vw - var(--side-bar-length));
  }
  to{
    width: calc(100vw - var(--side-bar-length)*2);
  }
}

@-webkit-keyframes hide-chat-details {
  from {
    width: calc(100vw - var(--side-bar-length)*2);
  }
  to {
    width: calc(100vw - var(--side-bar-length));
  }
}

@keyframes hide-chat-details {
  from {
    width: calc(100vw - var(--side-bar-length)*2);
  }
  to{
    width: calc(100vw - var(--side-bar-length));
  }
}
</style>
