<script>
import { beforeUpdate } from "svelte";
import { io } from "socket.io-client";

import Sidebar from "./Sidebar.svelte";
import RightSection from "./RightSection.svelte";
import { page } from "$app/stores";
import { user_id } from "$lib/stores/user";
import { deviceStore } from "$lib/stores/device"
import { friends } from "$lib/stores/friend"
import { friendRequestsStore } from "$lib/stores/friend-requests"

export let data;

const namespace = "https://localhost:8443";
const options = {
  transports: ["websocket"],
  auth: {  // TODO(low)(SpeedFox198): remove if unused
    token: "abcd"
  }
};

let activity = "Chat"; // TODO(UI)(SpeedFox198): make this change according to chat u are at :)
let appLoaded = false;
let displayChatDetails = false;

// Get and set user_id and device_id according to cookie data
user_id.set($page.data.user.user_id);
$: friends.set(data.friends.friendsList);
$: friendRequestsStore.set(data.friendRequests.friendRequestsList)
$: deviceStore.set(data.devices);

let socket;  // Forward declare socket :)


let _ran = false;  // Flag to prevent multiple connections
// Using beforeUpdate instead as a hacky method to connect before onMount
// TODO(low)(SpeedFox198): consider using `if (browser)` to run this
beforeUpdate(async () => {

  // Set flag to allow only running once
  if (_ran) return;
  _ran = true;

  // SocketIO instance
  socket = io(namespace, options);

  // TODO(medium)(SpeedFox198): remove this later lmao
  socket.on("connect", async () => {
    console.log("connected to SocketIO server");
  });
});

// Get latest 20n+1 to 20n+20 messages from room
async function getRoomMsgs(room_id, n, extra) {
  socket.emit("get_room_messages", { room_id, n, extra });
}


const closeChatDetails = () => displayChatDetails = false;
const toggleChatDetails = () => displayChatDetails = !displayChatDetails;

</script>


<svelte:head>
  <title>Bubbles | {activity}</title>
</svelte:head>


<main class="d-flex flex-nowrap h-100" class:d-none={!appLoaded}>
  <Sidebar {socket} {getRoomMsgs} {closeChatDetails}/>
  <RightSection
    {socket} {getRoomMsgs}
    {displayChatDetails} {toggleChatDetails} {closeChatDetails}
    on:load={() => appLoaded = true}
  />
</main>


<style>
main {
  position: relative;
  background-color: var(--white);
  -webkit-animation-name: display-app;
  -webkit-animation-duration: 0.4s;
  animation-name: display-app;
  animation-duration: 0.4s;
}

@-webkit-keyframes display-app {
  from {
    top: -2rem;
    opacity:0;
  }
  to {
    top: 0;
    opacity:1;
  }
}

@keyframes display-app {
  from {
    top: -2rem;
    opacity:0;
  }
  to{
    top: 0;
    opacity:1;
  }
}
</style>
