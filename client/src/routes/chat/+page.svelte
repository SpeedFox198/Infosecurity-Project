<svelte:head>
  <title>Bubbles | {activity}</title>
</svelte:head>


<script>
import { beforeUpdate } from "svelte";
import { io } from "socket.io-client";

import Sidebar from "./Sidebar.svelte";
import RightSection from "./RightSection.svelte";
import { page } from "$app/stores";
import { user_id } from "$lib/stores/user";


const namespace = "https://localhost:8443";
const options = {
  transports: ["websocket"],
  auth: {  // @TODO(SpeedFox198): remove if unused
    token: "abcd"
  }
};

let activity = "Chat"; // TODO(SpeedFox198): make this change according to chat u are at :)

// Get and set user_id and device_id according to cookie data
user_id.set($page.data.user.user_id);


let socket;  // Forward declare socket :)


let _ran = false;  // Flag to prevent multiple connections
// Using beforeUpdate instead as a hacky method to connect before onMount
beforeUpdate(async () => {

  // Set flag to allow only running once
  if (_ran) return;
  _ran = true;

  // SocketIO instance
  socket = io(namespace, options);

  // TODO(SpeedFox198): remove this later lmao
  socket.on("connect", async () => {
    console.log("connected to SocketIO server");
  });
});

// Get latest 20n+1 to 20n+20 messages from room
async function getRoomMsgs(room_id, n, extra) {
  socket.emit("get_room_messages", { room_id, n, extra });
}
</script>


<main class="d-flex flex-nowrap h-100">
  <Sidebar {getRoomMsgs}/>
  <RightSection {socket} {getRoomMsgs}/>
</main>


<style>
main {
  background-color: var(--white);
}
</style>
