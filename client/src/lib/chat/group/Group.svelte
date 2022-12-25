<script>
export let grp;
export let selectGrp;
</script>


<div class="group d-flex py-2 user-select-none"
  on:click={() => selectGrp(grp.room_id)}
  on:keydown>
  <div class="icon p-2">
    <div class="img-wrapper img-1-1">
      <img class="rounded-circle" src={grp.icon} alt="Group Icon">
    </div>
  </div>
  <div class="d-flex align-items-center">
    <span>{grp.name}</span>
  </div>
</div>


<style>
.group {
  border-bottom: 0.1rem solid var(--primary-light-shadow);
}

.group:hover {
  cursor: pointer;
  background-color: var(--primary-light-shadow);
}

.icon {
  height: 4.5rem;
  width: 4.5rem;
}
</style>
