<script>
import { beforeUpdate } from "svelte";
import { io } from "socket.io-client";

import Sidebar from "./Sidebar.svelte";
import RightSection from "./RightSection.svelte";
import ChatDetails from "$lib/chat/info/ChatDetails.svelte";
import E2EE, { encryption } from "$lib/e2ee/E2EE.svelte";
import { page } from "$app/stores";
import { globalUser, user_id } from "$lib/stores/user";
import { deviceStore } from "$lib/stores/device";
import { twoFACheckStore } from "$lib/stores/twofa-check.js";
import { friends } from "$lib/stores/friend";
import { friendRequestsStore } from "$lib/stores/friend-requests";
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
let animateHideChatDetails = false

// Get and set user_id and device_id according to cookie data
globalUser.set($page.data.user);
user_id.set($page.data.user.user_id);
$: friends.set(data.friends.friendsList);
$: friendRequestsStore.set(data.friendRequests.friendRequestsList)
$: deviceStore.set(data.devices);
$: twoFACheckStore.set(data.twoFAEnabled.twoFAEnabledCheck);

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
const openChatDetails = () => {
  displayChatDetails = true;
  animateHideChatDetails = true;
};
</script>


<svelte:head>
  <title>Bubbles | {activity}</title>
</svelte:head>


<main class="d-flex flex-nowrap h-100 overflow-hidden" class:d-none={!appLoaded}>
  <Sidebar {socket} {getRoomMsgs} {encryption}/>
  <RightSection
    {socket} {getRoomMsgs} {encryption}
    {displayChatDetails} {openChatDetails} {animateHideChatDetails}
    on:load={() => appLoaded = true}
  />
  <ChatDetails
    {socket} {displayChatDetails} {encryption}
    {closeChatDetails} {animateHideChatDetails}
  />
</main>

<!-- Enable end-to-end-encryption if user has public key (meaning e2ee is enabled) -->
{#if $globalUser.e2ee}
  <E2EE/>
{/if}


<style>
main {
  position: relative;
  background-color: var(--white);
  -webkit-animation-name: display-app;
  -webkit-animation-duration: 1s;
  animation-name: display-app;
  animation-duration: 1s;
}

@-webkit-keyframes display-app {
  from {
    top: -4rem;
    opacity:0;
  }
  to {
    top: 0;
    opacity:1;
  }
}

@keyframes display-app {
  from {
    top: -4rem;
    opacity:0;
  }
  to{
    top: 0;
    opacity:1;
  }
}
</style>
