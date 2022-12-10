<script>
import { room_id, allRooms } from "$lib/stores/room";
import { count } from "$lib/stores/count";

import Group from "$lib/chat/group/Group.svelte"
import Nav from "./Nav.svelte";
import ProfileArea from "./ProfileArea.svelte";

// SocketIO instance
export let getRoomMsgs;


async function selectGrp(new_room) {
  // Set selected room_id
  room_id.set(new_room);

  // Get room messages via socket if n is 0
  if (!$count[$room_id]) {
    const { n, extra } = count.nextN($room_id);
    getRoomMsgs($room_id, n, extra);
  }
}
</script>


<!-- Left Section -->
<div class="d-flex flex-column flex-shrink-0 left-section">
  
  <!-- Profile & Settings Section -->
  <div class="d-flex top-left">
    <Nav/>
  </div>

  <!-- Chat List Section -->
  <div class="d-flex flex-column bottom-left">
    {#each $allRooms as grp}
      <Group grp={grp} selectGrp={selectGrp}/>
    {/each}
  </div>
</div>

<footer>
</footer>

<style>
.left-section {
  width: var(--left-bar-length);
  background-color: var(--primary-light);
}

.top-left {
  /* position: absolute;
  top: 0; */
  height: 4rem;
  width: var(--left-bar-length);
  background-color: var(--primary);
}

.bottom-left {
  height: 100%;
  overflow-y: scroll;
}
</style>
