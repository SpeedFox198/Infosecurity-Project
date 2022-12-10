<svelte:head>
  <title>Bubbles | {activity}</title>
</svelte:head>


<script>
import { beforeUpdate } from "svelte";
import { io } from "socket.io-client";

import LeftSection from "./LeftSection.svelte";
import RightSection from "./RightSection.svelte";
import { page } from "$app/stores";
import { user_id } from "$lib/stores/user";


const namespace = "https://localhost:8443";
const transports = { transports: ["websocket"] };

let activity = "Chat"; // TODO(SpeedFox198): make this change according to chat u are at :)

// Get and set user_id and device_id according to cookie data
user_id.set($page.data.user.user_id);
// TODO(SpeedFox198): remove if unused
// const device_id = $page.data.user.device_id;


let socket;  // Forward declare socket :)


let _count = 0;  // Count to prevent multiple connections
// Using beforeUpdate instead as a hacky method to connect before onMount
beforeUpdate(async () => {

  // Increase count to prevent multiple connections
  if (_count) return;
  _count++;

  // SocketIO instance
  socket = io(namespace, transports);

  // TODO(SpeedFox198): remove this later lmao
  socket.on("connect", async () => {
    console.log("connected to SocketIO server");
  });
});
</script>


<main class="d-flex flex-nowrap h-100">
  <LeftSection socket={socket}/>
  <RightSection socket={socket}/>
</main>


<style>
main {
  background-color: var(--white);
}
</style>
