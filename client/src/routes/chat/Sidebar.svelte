<script>
import { room_id, allRooms } from '$lib/stores/room';
import { count } from '$lib/stores/count';
import { selectedMsgs } from '$lib/stores/select';

import Group from '$lib/chat/group/Group.svelte';
import ProfileBar from '$lib/settings/ProfileBar.svelte';
import Nav from './Nav.svelte';
import Settings from '$lib/settings/Settings.svelte';

// SocketIO instance
export let getRoomMsgs;

let displaySettings = false;
let roomSearchInput = "" 
$: sanitizedRoomInput = roomSearchInput
                        .toLowerCase()
                        .replace(/[/\-\\^$*+?.()|[\]{}]/g, '\\$&')
$: roomSearchRegex = new RegExp(`.*${sanitizedRoomInput}.*`, "g")
$: currentRooms = $allRooms.filter(room => room.name
                                          .toLowerCase()
                                          .match(roomSearchRegex))

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
  <Settings {displaySettings} {toggleSettings}/>

  <!-- Profile & Settings Section -->
  <Nav bind:roomSearchInput={roomSearchInput}/>

  <!-- Chat List Section -->
  <div class="d-flex flex-column bottom-left">
    {#each currentRooms as grp} 
      <Group {grp} {selectGrp}/>
    {/each}
  </div>

  <ProfileBar {toggleSettings}/>
</div>

<style>
.sidebar {
  position: relative;
  width: var(--left-bar-length);
  background-color: var(--primary-light);
  overflow-x: hidden;
}

.bottom-left {
  height: 100%;
  overflow-y: scroll;
}
</style>
