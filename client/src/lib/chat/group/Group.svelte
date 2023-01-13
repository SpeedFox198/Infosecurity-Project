<script>
export let grp;
export let selectGrp;

// TODO Change to bucket in the future if possible
const group_icon = `https://localhost:8443/api/${grp.icon}`
</script>


<div class="group d-flex py-2 user-select-none"
  on:click={() => selectGrp(grp.room_id)}
  on:keydown>
  <div class="icon p-2">
    <div class="img-wrapper img-1-1">
      {#if !grp.icon.startsWith("media/")}
        <img class="rounded-circle" src={grp.icon} alt="Group Icon">
      {:else}
        <img class="rounded-circle" src={ group_icon } alt="Group Icon">
      {/if}
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
