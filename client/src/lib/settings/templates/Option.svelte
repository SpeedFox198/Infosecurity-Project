<script>
export let icon;
export let name;
</script>


<div
  class="option d-flex flex-row user-select-none"
  on:click
  on:keydown>
  <div class="icon d-flex align-items-center justify-content-center">
    <i class="fa-solid fa-{icon} fs-4"></i>
  </div>
  <div class="d-flex align-items-center">
    <span class="fs-5">{name}</span>
  </div>
  <slot />
</div>


<style>
.option {
  height: 4.5rem;
  /* TODO(UI)(SpeedFox198): removed if unused */
  /* border-bottom: 0.1rem solid var(--primary-light-shadow); */
}

.option:hover {
  cursor: pointer;
  background-color: var(--grey-light);
}

.option:focus {
  background-color: var(--grey-light-shadow);
}

.icon {
  width: 4.5rem;
  height: 4.5rem;
  color: var(--grey-dark);
}
</style>
