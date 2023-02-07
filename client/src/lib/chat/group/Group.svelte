<script context="module">
let current;
</script>


<script>
export let grp;
export let selectGrp;

// TODO Change to bucket in the future if possible
const group_icon = `https://localhost:8443/api/${grp.icon}`;

let selected;

const deselect = () => selected = false;


const selectCurrentGroup = () => {
  if (current && current.deselect === deselect) return;
  if (current) current.deselect();
  current = { deselect };
  selected = true;
  selectGrp(grp.room_id);
};
</script>


<div class="group d-flex py-2 user-select-none"
  class:selected
  class:unselected={!selected}
  on:click={selectCurrentGroup}
  on:keydown
>
  <div class="icon p-2">
    <div class="img-wrapper img-1-1">
      {#if !grp.icon.startsWith("media/")}
        <img class="rounded-circle" src={grp.icon} alt="Group Icon">
      {:else}
        <img class="rounded-circle" src={group_icon} alt="Group Icon">
      {/if}
    </div>
    {#if grp.type === "direct"}
      <div class="d-block status rounded-circle" class:offline={!grp.online}></div>
    {/if}
  </div>
  <div class="d-flex align-items-center">
    <span>{grp.name}</span>
  </div>
</div>


<style>
.group {
  background-color: var(--white);
  border-bottom: 0.1rem solid var(--white-shadow);
}

.group.unselected:hover {
  cursor: pointer;
  background-color: var(--grey-light);
}

.group.selected {
  background-color: var(--grey-light-shadow);
}

.icon {
  position: relative;
  height: 4.5rem;
  width: 4.5rem;
}

.status {
  position: absolute;
  bottom: calc(0.5rem - 4px);
  right: calc(0.5rem - 4px);
  width: 18px;
  height: 18px;
  background-color: var(--primary);
  border: 3px solid var(--white);
}

.group.unselected:hover .status {
  border-color: var(--grey-light);
}

.group.selected .status {
  border-color: var(--grey-light-shadow);
}

.offline {
  background-color: var(--grey-dark);
}

.offline::after {
  content: "";
  display: block;
  margin: auto;
  margin-top: 5px;
  width: 8px;
  height: 2px;
  background-color: var(--white);
  border-radius: 50rem;
}

.group.unselected:hover .offline {
  border-color: var(--grey-light);
}

.group.selected .offline {
  border-color: var(--grey-light-shadow);
}
</style>
