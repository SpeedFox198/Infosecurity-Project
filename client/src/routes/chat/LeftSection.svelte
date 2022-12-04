<script>
import Nav from "./Nav.svelte";
import Group from "$lib/chat/group/Group.svelte"

let grpList = [
  {icon:"/default.png", name:"Grp Chat"},
  {icon:"/default.png", name:"Grp Chat"},
  {icon:"/galaxy.jpg", name:"Grp Chat"},
  {icon:"/favicon.svg", name:"Grp Chat"}
];

async function selectGrp() {

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
