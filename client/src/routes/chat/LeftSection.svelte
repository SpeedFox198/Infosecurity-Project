<script>
import { room_id, allRooms } from "$lib/stores/rooms";

import Group from "$lib/chat/group/Group.svelte"
import Nav from "./Nav.svelte";
import ProfileArea from "./ProfileArea.svelte";

async function selectGrp(new_room) {
  room_id.set(new_room);
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
