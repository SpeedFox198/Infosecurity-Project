<script>
import { room_id } from "$lib/stores/messages";

import Group from "$lib/chat/group/Group.svelte"
import Nav from "./Nav.svelte";

// TODO(SpeedFox198): remove temp values
let grpList = [
  {icon:"/default.png", name:"Grp Chat", room_id:"room_1"},
  {icon:"/default.png", name:"Grp Chat", room_id:"room_2"},
  {icon:"/galaxy.jpg", name:"Grp Chat", room_id:"room_3"},
  {icon:"/favicon.svg", name:"Grp Chat", room_id:"room_4"}
];

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
    {#each grpList as grp}
      <Group grp={grp} selectGrp={selectGrp}/>
    {/each}
  </div>
</div>


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
