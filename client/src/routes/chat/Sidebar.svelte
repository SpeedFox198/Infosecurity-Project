<script>
import { room_id, allRooms } from "$lib/stores/room";
import { count } from "$lib/stores/count";
import { selectedMsgs } from "$lib/stores/select";

import Group from "$lib/chat/group/Group.svelte"
import ProfileBar from "$lib/settings/ProfileBar.svelte"
import Nav from "./Nav.svelte";
import Settings from "$lib/settings/Settings.svelte";

// SocketIO instance
export let getRoomMsgs;

let displaySettings = false;


async function selectGrp(new_room) {
  // Set selected room_id
  room_id.set(new_room);

  // Clear any selected messages in previous room
  selectedMsgs.clear();

  // Get room messages via socket if n is 0
  if (!($count[$room_id] || {}).n) {
    const { n, extra } = count.nextN($room_id);
    getRoomMsgs($room_id, n, extra);
  }
}

async function toggleSettings() {
  displaySettings = !displaySettings;
}
</script>


<!-- Left Sidebar -->
<div class="d-flex flex-column flex-shrink-0 sidebar">

  <!-- Settings Display Section -->
  <Settings display={displaySettings} toggleSettings={toggleSettings}/>

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

  <ProfileBar toggleSettings={toggleSettings}/>
</div>


<style>
.sidebar {
  position: relative;
  width: var(--left-bar-length);
  background-color: var(--primary-light);
  overflow-x: hidden;
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
