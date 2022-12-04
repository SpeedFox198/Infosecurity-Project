<script>
export let grp;
export let selectGrp;
</script>

<div class="group d-flex py-2"
  on:click={() => selectGrp(grp.room_id)}
  on:keydown>
  <div class="icon">
    <img class="rounded-circle px-2" src={grp.icon} alt="Grop Icon">
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
  width: 4.5rem;
}
</style>